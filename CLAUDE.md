# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-file Python CLI (`src/meeting-cost`, no `.py` extension) that scrapes Amazon US salary data from levels.fyi with headless Chrome/Selenium and prints the cost of a meeting for a list of attendees given as `<ROLE>-<LEVEL>` (roles `SDM`, `SDE`, `TPM`; levels `L4`–`L8`).

## Commands

```
poetry install                                   # install deps (Python ^3.12)
poetry run python src/meeting-cost SDM-L7 SDE-L5  # run
poetry run pytest                                # run tests
poetry run pytest tests/test_find_chromedriver.py::test_returns_none_when_not_found  # single test
```

Running requires Chrome and network access to levels.fyi. `find_chromedriver` looks for ChromeDriver on `PATH`, then in `CHROMEDRIVER_LOCATIONS`; if neither has it, Selenium Manager locates or downloads one. No linter or formatter is configured.

Because the script has a hyphen and no `.py` extension, tests import it with `importlib.machinery.SourceFileLoader` (see `tests/test_find_chromedriver.py`).

## How it works

1. `__main__` fetches one levels.fyi page per role (`SDM_URL`, `SDE_URL`, `TPM_URL`, all with `country=254` = USA) on every run; there is no caching.
2. `extract_salaries` loads the page, waits for the salary table, clicks the "expand" button so all levels are listed, waits for the expanded rows, then parses the first HTML table with `pandas.read_html`.
3. `create_salary_dict` maps each level to an hourly rate: the "Total" column (e.g. `€250K`) is parsed to an integer and divided by 238 work days × 8 hours. Rows with `--` are skipped.
4. Attendee hourly rates are summed; unknown attendees are reported and skipped. Costs are printed for fixed lengths of 30/45/60/90/120 minutes.

## Fragility: levels.fyi selectors

The scraper depends on generated CSS class names on levels.fyi (MUI classes like `css-kge0eu`, `job-family_tableContainer__MOxEY`). When levels.fyi changes its layout, the tool fails with a Selenium timeout. The fix is to inspect the live page in a browser and update the three CSS selectors in `extract_salaries` (example: commit `ed41f47`).

## Known gaps (from README / TODO header)

No caching between runs, only Amazon/USA, only SDM/SDE/TPM roles, fixed currency (€) and meeting lengths.
