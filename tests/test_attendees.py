import pytest

import meeting_cost


def test_parses_role_and_level():
    assert meeting_cost.parse_attendee("SDE-L5") == ("SDE", "L5")


def test_accepts_lowercase_attendees():
    assert meeting_cost.parse_attendee("tpm-l6") == ("TPM", "L6")


@pytest.mark.parametrize("attendee", ["SDE", "SDE-", "PM-L5", "SDE-L9", "SDE-L5-L6"])
def test_rejects_malformed_attendees(attendee):
    with pytest.raises(ValueError, match=f"invalid attendee '{attendee}'"):
        meeting_cost.parse_attendee(attendee)


def run_main(monkeypatch, *args):
    monkeypatch.setattr("sys.argv", ["meeting-cost", *args])
    with pytest.raises(SystemExit) as exit_info:
        meeting_cost.main()
    return exit_info.value.code


def refuse_to_fetch(url):
    raise AssertionError(f"fetched {url}")


def test_rejects_invalid_attendees_before_fetching(monkeypatch, capsys):
    monkeypatch.setattr(meeting_cost, "fetch_page", refuse_to_fetch)

    assert run_main(monkeypatch, "SDE-L5", "SDE") == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "invalid attendee 'SDE'" in captured.err


def test_prints_usage_without_attendees(monkeypatch, capsys):
    assert run_main(monkeypatch) == 2
    assert "ATTENDEE [ATTENDEE ...]" in capsys.readouterr().err


def test_reports_missing_salary_data(monkeypatch, capsys):
    monkeypatch.setattr(meeting_cost, "fetch_page", lambda url: "")

    assert run_main(monkeypatch, "SDE-L5") == 1
    assert "Could not read salary data from levels.fyi (no embedded page data)" in capsys.readouterr().err
