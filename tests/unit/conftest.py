"""
Shared fixtures for the pytest-html-plus unit test suite.
"""

import json

import pytest

from pytest_html_plus.compute_filter_counts import compute_filter_count
from pytest_html_plus.generate_html_report import JSONReporter

# All fields that generate_html_report() hard-accesses (no .get() fallback).
# Any test result dict passed to the HTML renderer must include these.
_RESULT_DEFAULTS = {
    "worker": "main",
    "stdout": "",
    "stderr": "",
    "error": None,
    "trace": None,
    "attempts": [],
    "links": [],
    "markers": [],
    "duration": 0.1,
    "flaky": False,
    "attempt_count": 1,
}


def make_test_result(**kwargs):
    """
    Build a valid test result dict with all required fields.
    Pass keyword arguments to override any default.

    Example:
        make_test_result(nodeid="test_x.py::test_a", status="failed", flaky=True)
    """
    result = dict(_RESULT_DEFAULTS)
    result.update(kwargs)
    return result


@pytest.fixture
def reporter_factory(tmp_path):
    """
    Returns a factory function that creates a fully initialised JSONReporter
    pointed at isolated tmp_path subdirectories, ready to call
    generate_html_report() on.

    Usage:
        def test_something(reporter_factory):
            reporter = reporter_factory()
            reporter = reporter_factory(results=[make_test_result(...)])
    """

    def _make(results=None, report_filename="report.json"):
        screenshots_dir = tmp_path / "screenshots"
        output_dir = tmp_path / "output"
        screenshots_dir.mkdir(exist_ok=True)
        output_dir.mkdir(exist_ok=True)

        results = results or []
        report_file = tmp_path / report_filename
        report_file.write_text(json.dumps({"results": results, "filters": {}}))

        reporter = JSONReporter(
            report_path=str(report_file),
            screenshots_dir=str(screenshots_dir),
            output_dir=str(output_dir),
        )
        reporter.results = results
        reporter.filters = compute_filter_count(results)
        reporter.metadata = {}
        return reporter

    return _make


@pytest.fixture
def screenshots_dir(tmp_path):
    """
    A tmp directory pre-populated with fake PNG screenshots.
    File names follow the pattern: test_<name>_failure.png
    """
    d = tmp_path / "screenshots"
    d.mkdir()
    for name in ("login", "checkout", "profile"):
        (d / f"test_{name}_failure.png").write_bytes(b"\x89PNG\r\nfake")
    return d


@pytest.fixture
def output_dir(tmp_path):
    """A clean tmp output directory."""
    d = tmp_path / "output"
    d.mkdir()
    return d


@pytest.fixture
def passing_test_result():
    """A minimal valid passing test result dict."""
    return make_test_result(
        nodeid="test_sample.py::test_passes",
        test="test_passes",
        status="passed",
    )


@pytest.fixture
def failing_test_result():
    """A minimal valid failing test result dict."""
    return make_test_result(
        nodeid="test_sample.py::test_fails",
        test="test_fails",
        status="failed",
        error="E AssertionError: something went wrong",
        trace="test_sample.py line 5\n  assert False",
    )


@pytest.fixture
def flaky_test_result():
    """A test result marked as flaky with 3 attempts."""
    return make_test_result(
        nodeid="test_sample.py::test_flaky",
        test="test_flaky",
        status="passed",
        flaky=True,
        attempt_count=3,
        flaky_attempts=["failed", "failed", "passed"],
        duration=0.5,
    )
