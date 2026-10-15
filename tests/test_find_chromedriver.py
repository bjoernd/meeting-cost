import pytest

import meeting_cost


def make_driver(directory, executable=True):
    directory.mkdir(parents=True, exist_ok=True)
    driver = directory / "chromedriver"
    driver.write_text("#!/bin/sh\n")
    driver.chmod(0o755 if executable else 0o644)
    return str(driver)


@pytest.fixture
def empty_path(monkeypatch, tmp_path):
    monkeypatch.setenv("PATH", str(tmp_path / "empty-path"))


def test_prefers_chromedriver_on_path(monkeypatch, tmp_path):
    on_path = make_driver(tmp_path / "bin")
    elsewhere = make_driver(tmp_path / "elsewhere")
    monkeypatch.setenv("PATH", str(tmp_path / "bin"))

    assert meeting_cost.find_chromedriver([elsewhere]) == on_path


def test_returns_first_existing_location(empty_path, tmp_path):
    missing = str(tmp_path / "missing" / "chromedriver")
    first = make_driver(tmp_path / "first")
    second = make_driver(tmp_path / "second")

    assert meeting_cost.find_chromedriver([missing, first, second]) == first


def test_skips_non_executable_files(empty_path, tmp_path):
    not_executable = make_driver(tmp_path / "plain", executable=False)
    executable = make_driver(tmp_path / "exec")

    assert meeting_cost.find_chromedriver([not_executable, executable]) == executable


def test_returns_none_when_not_found(empty_path, tmp_path):
    assert meeting_cost.find_chromedriver([str(tmp_path / "missing")]) is None
