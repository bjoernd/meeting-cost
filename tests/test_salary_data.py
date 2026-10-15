import json

import pytest

import meeting_cost

HOURS_PER_YEAR = 238 * 8


def salary_page(page_props):
    data = json.dumps({"props": {"pageProps": page_props}})
    return f'<html><body><script id="__NEXT_DATA__" type="application/json">{data}</script></body></html>'


def average(level_name, total):
    return {"shortestLevelName": level_name, "rawValues": {"total": total}}


def test_computes_hourly_rates_from_embedded_salary_data():
    page = salary_page({
        "locationCurrency": "USD",
        "averages": [average("L4", 183319), average("L5 SDM", 309764)],
    })

    assert meeting_cost.hourly_rates(page) == {
        "L4": pytest.approx(183319 / HOURS_PER_YEAR),
        "L5": pytest.approx(309764 / HOURS_PER_YEAR),
    }


def test_ignores_unsupported_levels():
    page = salary_page({
        "locationCurrency": "USD",
        "averages": [average("L8", 1218791), average("L10", 1548000), average("VP", 1893500)],
    })

    assert meeting_cost.hourly_rates(page) == {"L8": pytest.approx(1218791 / HOURS_PER_YEAR)}


def test_rejects_page_without_embedded_data():
    with pytest.raises(meeting_cost.SalaryDataNotFound, match="no embedded page data"):
        meeting_cost.hourly_rates("")


def test_rejects_page_with_unexpected_data_layout():
    page = salary_page({"locationCurrency": "USD"})

    with pytest.raises(meeting_cost.SalaryDataNotFound, match="unexpected page data layout"):
        meeting_cost.hourly_rates(page)


def test_rejects_salaries_not_given_in_usd():
    page = salary_page({"locationCurrency": "EUR", "averages": [average("L4", 160000)]})

    with pytest.raises(meeting_cost.SalaryDataNotFound, match="expected USD, got EUR"):
        meeting_cost.hourly_rates(page)
