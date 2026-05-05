import json

from pytest_html_plus.compute_filter_counts import compute_filter_count
from pytest_html_plus.generate_html_report import JSONReporter

# Minimum fields required by generate_html_report() for each test result entry
REQUIRED_FIELDS = {
    "worker": "main",
    "stdout": "",
    "stderr": "",
    "error": None,
    "trace": None,
    "attempts": [],
    "links": [],
    "markers": [],
    "duration": 0.1,
}


def make_result(**kwargs):
    """Build a minimal valid test result dict, merging in any overrides."""
    base = dict(REQUIRED_FIELDS)
    base.update(kwargs)
    return base


def make_reporter(tmp_path, results):
    """Build a JSONReporter pre-loaded with the given results list."""
    (tmp_path / "screenshots").mkdir(exist_ok=True)
    (tmp_path / "output").mkdir(exist_ok=True)

    report_file = tmp_path / "report.json"
    report_file.write_text(json.dumps({"results": results, "filters": {}}))

    reporter = JSONReporter(
        report_path=str(report_file),
        screenshots_dir=str(tmp_path / "screenshots"),
        output_dir=str(tmp_path / "output"),
    )
    reporter.results = results
    reporter.filters = compute_filter_count(results)
    reporter.metadata = {}
    return reporter


def render_html(reporter):
    reporter.generate_html_report()
    from pathlib import Path

    return Path(reporter.output_dir, "report.html").read_text()


class TestFlakyBadge:
    def test_flaky_badge_shows_attempt_count(self, tmp_path):
        results = [
            make_result(
                nodeid="test_x.py::test_login",
                test="test_login",
                status="passed",
                flaky=True,
                attempt_count=3,
            )
        ]
        html = render_html(make_reporter(tmp_path, results))

        assert 'class="is-flaky"' in html
        assert "FLAKY" in html
        assert "3 attempts" in html

    def test_flaky_badge_single_attempt_has_no_count(self, tmp_path):
        results = [
            make_result(
                nodeid="test_x.py::test_signup",
                test="test_signup",
                status="passed",
                flaky=True,
                attempt_count=1,
            )
        ]
        html = render_html(make_reporter(tmp_path, results))

        assert 'class="is-flaky"' in html
        assert "FLAKY" in html
        assert "attempts" not in html

    def test_non_flaky_test_has_no_badge(self, tmp_path):
        results = [
            make_result(
                nodeid="test_x.py::test_logout",
                test="test_logout",
                status="passed",
                flaky=False,
                attempt_count=1,
            )
        ]
        html = render_html(make_reporter(tmp_path, results))

        assert 'class="is-flaky"' not in html
        assert "FLAKY" not in html

    def test_missing_flaky_key_treated_as_non_flaky(self, tmp_path):
        # No "flaky" key at all — should fall through to the else branch
        results = [
            make_result(
                nodeid="test_x.py::test_checkout",
                test="test_checkout",
                status="failed",
            )
        ]
        html = render_html(make_reporter(tmp_path, results))

        assert 'class="is-flaky"' not in html

    def test_only_flaky_tests_get_badge(self, tmp_path):
        results = [
            make_result(
                nodeid="test_x.py::test_a",
                test="test_a",
                status="passed",
                flaky=True,
                attempt_count=2,
            ),
            make_result(
                nodeid="test_x.py::test_b",
                test="test_b",
                status="passed",
                flaky=False,
                attempt_count=1,
            ),
        ]
        html = render_html(make_reporter(tmp_path, results))

        assert html.count('class="is-flaky"') == 1
        assert "2 attempts" in html
