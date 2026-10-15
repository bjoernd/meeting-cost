# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-module Python CLI (`src/meeting_cost.py`, installed as the `meeting-cost` command) that downloads Amazon US salary data from levels.fyi and prints the cost of a meeting for a list of attendees given as `<ROLE>-<LEVEL>` (roles `SDM`, `SDE`, `TPM`; levels `L4`–`L8`, case-insensitive). It uses only the Python standard library.

## Commands

```
poetry install                                   # install (Python ^3.12)
poetry run meeting-cost SDM-L7 SDE-L5            # run
poetry run pytest                                # run offline tests
poetry run pytest -m live                        # run tests against live levels.fyi data
poetry run pytest tests/test_attendees.py::test_parses_role_and_level  # single test
```

Running needs network access to levels.fyi. No linter or formatter is configured. `pyproject.toml` puts `src` on the pytest path and deselects tests marked `live` by default.

## How it works

1. `main` validates all attendees with `parse_attendee` before any download (exit code 2 on bad input or no input), then fetches one levels.fyi page per role that is actually needed (`ROLE_URLS`, all with `country=254` = USA). There is no caching.
2. `fetch_page` downloads the page with `urllib`. No browser is involved.
3. `hourly_rates` reads the JSON levels.fyi embeds for Next.js (`<script id="__NEXT_DATA__">`): `props.pageProps.averages[]` holds one entry per level with `shortestLevelName` (e.g. `L5 SDM`, the first word is the level) and `rawValues.total` (yearly total compensation in USD). Totals are divided by `WORK_DAYS_PER_YEAR` × `HOURS_PER_DAY`. Levels outside `LEVELS` (e.g. `L10`, `VP`) are dropped.
4. Attendee hourly rates are summed; attendees whose level has no data on levels.fyi (e.g. `SDM-L4`) are reported and skipped. Costs are printed in USD for fixed lengths of 30/45/60/90/120 minutes.

## Fragility: levels.fyi page data

The embedded JSON is undocumented. If its layout changes, or levels.fyi returns an empty page (this happens occasionally for a few minutes), `hourly_rates` raises `SalaryDataNotFound` and `main` exits with code 1 and a short message. `pytest -m live` checks the current live data. To find the new layout, download a page and look at `props.pageProps` in the `__NEXT_DATA__` script.

The rendered HTML table uses generated CSS class names that change often. Do not go back to scraping it.

## Known gaps (from README / TODO header)

No caching between runs, only Amazon/USA, only SDM/SDE/TPM roles, fixed currency (USD) and meeting lengths.
