import subprocess
import sys

import pytest

import meeting_cost

pytestmark = pytest.mark.live


@pytest.mark.parametrize("role", meeting_cost.ROLE_URLS)
def test_levels_fyi_provides_salary_data(role):
    rates = meeting_cost.hourly_rates(meeting_cost.fetch_page(meeting_cost.ROLE_URLS[role]))

    # levels.fyi lists no L4 managers, so only L5 and above exist for every role
    assert {"L5", "L6", "L7", "L8"} <= rates.keys()
    assert all(rate > 0 for rate in rates.values())


def test_prints_meeting_cost_for_attendees():
    result = subprocess.run([sys.executable, "-m", "meeting_cost", "SDM-L7", "SDE-L5", "TPM-L6"],
                            capture_output=True, text=True, check=True)

    assert result.stderr == ""
    assert result.stdout.startswith("Getting salary data...\nMeeting cost:\n")
    assert "  -  60 min: " in result.stdout
