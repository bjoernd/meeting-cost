from io import StringIO

import pandas as pd
import pytest

from test_find_chromedriver import meeting_cost

SALARY_TABLE = """
<table>
  <tr><th>Level Name</th><th>Total</th></tr>
  <tr><td>L4 SDE I</td><td>€180K</td></tr>
  <tr><td>L5 SDE II</td><td>€250K</td></tr>
  <tr><td>L6 SDE III</td><td>--</td></tr>
</table>
"""


def test_parses_salary_table_into_hourly_rates():
    df = pd.read_html(StringIO(SALARY_TABLE))[0]

    salaries = meeting_cost.create_salary_dict(df)

    assert salaries == {
        "L4": pytest.approx(180000 / 238 / 8),
        "L5": pytest.approx(250000 / 238 / 8),
    }
