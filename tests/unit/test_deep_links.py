import re
from pathlib import Path

from pytest_html_plus.generate_html_report import stable_test_anchor
from tests.unit.conftest import make_test_result


def test_stable_test_anchor_is_deterministic_and_url_safe():
    nodeid = 'tests/test_api.py::TestUsers::test_lookup[user/"José"]'

    first = stable_test_anchor(nodeid)
    second = stable_test_anchor(nodeid)

    assert first == second
    assert re.fullmatch(r"test-[0-9a-f]{32}", first)


def test_stable_test_anchor_distinguishes_test_variants():
    anchors = {
        stable_test_anchor("tests/a.py::TestOne::test_same[value-a]"),
        stable_test_anchor("tests/a.py::TestTwo::test_same[value-a]"),
        stable_test_anchor("tests/b.py::TestOne::test_same[value-a]"),
        stable_test_anchor("tests/a.py::TestOne::test_same[value-b]"),
    }

    assert len(anchors) == 4


def test_report_adds_anchor_nodeid_and_copy_link(reporter_factory):
    nodeid = 'tests/test_api.py::TestUsers::test_lookup[user/"José"]'
    result = make_test_result(
        nodeid=nodeid,
        test='test_lookup[user/"José"]',
        status="failed",
    )
    reporter = reporter_factory(results=[result])
    reporter.generate_html_report()
    content = Path(reporter.output_dir, "report.html").read_text(encoding="utf-8")

    anchor = stable_test_anchor(nodeid)
    assert f'id="{anchor}" class="test test-card"' in content
    assert (
        'data-nodeid="tests/test_api.py::TestUsers::test_lookup'
        '[user/&quot;José&quot;]"'
    ) in content
    assert f"copyTestLink('{anchor}', this)" in content
    assert 'title="Copy link to test"' in content


def test_report_contains_fragment_reveal_behavior(reporter_factory):
    result = make_test_result(
        nodeid="tests/test_sample.py::test_passes",
        test="test_passes",
        status="passed",
    )
    reporter = reporter_factory(results=[result])
    reporter.generate_html_report()
    content = Path(reporter.output_dir, "report.html").read_text(encoding="utf-8")

    assert "function revealTestFromFragment()" in content
    assert "clearFiltersForDeepLink();" in content
    assert "header.classList.add('expanded');" in content
    assert "details.style.display = 'block';" in content
    assert "testCard.scrollIntoView" in content
    assert "testCard.focus" in content
    assert "window.addEventListener('hashchange', revealTestFromFragment);" in content


def test_report_uses_subtle_target_highlight_and_accessible_focus(reporter_factory):
    result = make_test_result(
        nodeid="tests/test_sample.py::test_passes",
        test="test_passes",
        status="passed",
    )
    reporter = reporter_factory(results=[result])
    reporter.generate_html_report()
    content = Path(reporter.output_dir, "report.html").read_text(encoding="utf-8")

    assert ".test:target, .test.deep-link-target" in content
    assert "outline: 2px solid rgba(160, 130, 90, 0.4);" in content
    assert "box-shadow: 0 2px 8px rgba(80, 65, 45, 0.1);" in content
    assert ".test:focus-visible { outline: 2px solid #2563eb;" in content


def test_anchor_is_derived_without_changing_json_result(reporter_factory):
    result = make_test_result(
        nodeid="tests/test_sample.py::test_passes",
        test="test_passes",
        status="passed",
    )
    reporter = reporter_factory(results=[result])
    reporter.generate_html_report()

    assert "anchor" not in result
    assert "stable_id" not in result
