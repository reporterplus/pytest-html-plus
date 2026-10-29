"""Browser coverage for copying individual deep links from a similarity group."""

import json
from pathlib import Path

import pytest
from playwright.sync_api import expect, sync_playwright

from pytest_html_plus.generate_html_report import stable_test_anchor
from pytest_html_plus.similar_errors import annotate_similar_errors
from tests.unit.conftest import make_test_result


@pytest.fixture
def copy_report(reporter_factory):
    def build(enabled=True, duplicate_member=False):
        tests = [
            make_test_result(
                nodeid=f"tests/test_account.py::test_{name}",
                test=f"test_{name}",
                status="failed",
                error="ValueError: invalid account name",
            )
            for name in ("login", "checkout[José]", "search")
        ]
        reporter = reporter_factory(results=tests)
        if enabled:
            report = {"results": tests}
            annotate_similar_errors(report)
            reporter.similar_error_groups = report["similar_error_groups"]
            if duplicate_member:
                group = next(iter(reporter.similar_error_groups.values()))
                group["nodeids"].append(group["nodeids"][0])
        reporter.generate_html_report()
        path = Path(reporter.output_dir, "report.html")
        return path, tests

    return build


@pytest.fixture
def copy_page():
    with sync_playwright() as pw:
        if not Path(pw.chromium.executable_path).exists():
            pytest.skip("Install Chromium with python -m playwright install chromium")
        browser = pw.chromium.launch()
        page = browser.new_page()
        yield page
        browser.close()


def mock_clipboard(page, implementation):
    page.evaluate(
        """implementation => {
            window.copiedTexts = [];
            Object.defineProperty(navigator, 'clipboard', {
                configurable: true,
                value: implementation === 'missing' ? undefined : {
                    writeText: text => {
                        window.copiedTexts.push(text);
                        if (implementation === 'reject') return Promise.reject(new Error('Permission denied'));
                        return Promise.resolve();
                    }
                }
            });
        }""",
        implementation,
    )


@pytest.mark.parametrize("duplicate_member", [False, True])
def test_copy_all_links_and_open_each_destination(
    copy_report, copy_page, duplicate_member
):
    page = copy_page
    path, tests = copy_report(duplicate_member=duplicate_member)
    anchors = [stable_test_anchor(test["nodeid"]) for test in tests]
    base = "https://ci.example.test/artifacts/report.html?run=42&job=unit%20tests"
    page.route(
        "https://ci.example.test/**", lambda route: route.fulfill(path=str(path))
    )
    original_url = f"{base}#{anchors[1]}"
    page.goto(original_url)
    mock_clipboard(page, "success")
    page.locator(f"#{anchors[1]} .similar-errors-badge").click()
    panel = page.locator("#similar-errors-popover")
    copy = panel.locator(".copy-all-links")
    expect(copy.locator("svg")).to_be_visible()
    expect(copy).to_have_attribute("aria-label", "Copy all test links")
    assert (
        copy.locator("svg").inner_html()
        == page.locator(f"#{anchors[1]} .test-link-btn svg").inner_html()
    )
    assert page.evaluate("window.copiedTexts") == []
    # Keyboard access, with the current test in the middle of the ordered group.
    copy.focus()
    page.keyboard.press("Enter")
    expect(copy).to_have_text("✓")
    expected_urls = [f"{base}#{anchor}" for anchor in anchors]
    expected = "\n".join(
        f"{test['test']} — {url}" for test, url in zip(tests, expected_urls)
    )
    assert page.evaluate("window.copiedTexts") == [expected]
    assert len(set(expected_urls)) == len(tests)
    assert page.url == original_url
    expect(panel).to_be_visible()
    expect(copy.locator("svg")).to_be_visible()
    expect(copy).to_have_attribute("aria-label", "Copy all test links")
    assert "Recipients need access to this report." in panel.inner_text()

    # Every URL opens through the existing reveal handler, including the current test.
    for url, anchor in zip(expected_urls, anchors):
        page.goto(url)
        card = page.locator(f"#{anchor}")
        expect(card).to_have_class("test test-card deep-link-target")
        expect(card.locator(".details")).to_be_visible()
        assert page.locator(".deep-link-target").count() == 1
        assert page.url == url

    # Individual copy uses exactly the same URL format and retains its feedback.
    mock_clipboard(page, "success")
    individual = page.locator(f"#{anchors[0]} .test-link-btn")
    individual.click()
    expect(individual).to_have_text("✓")
    assert page.evaluate("window.copiedTexts") == [expected_urls[0]]


@pytest.mark.parametrize("failure", ["reject", "missing"])
def test_copy_failure_keeps_popover_open_and_allows_retry(
    copy_report, copy_page, failure
):
    page = copy_page
    path, _ = copy_report()
    page.goto(path.as_uri())
    original_url = page.url
    mock_clipboard(page, failure)
    page.locator(".similar-errors-badge").first.click()
    panel = page.locator("#similar-errors-popover")
    copy = panel.locator(".copy-all-links")
    expect(copy.locator("svg")).to_be_visible()
    expect(copy).to_have_attribute("aria-label", "Copy all test links")
    copy.click()
    expect(copy).to_have_text("✗")
    expect(panel).to_be_visible()
    assert page.url == original_url
    expect(copy.locator("svg")).to_be_visible()
    expect(copy).to_have_attribute("aria-label", "Copy all test links")
    mock_clipboard(page, "success")
    copy.click()
    expect(copy).to_have_text("✓")
    copied = page.evaluate("window.copiedTexts[0]")
    assert len(copied.splitlines()) == 3
    assert all(" — file://" in line for line in copied.splitlines())
    expect(panel).to_be_visible()
    assert page.url == original_url


def test_disabled_report_has_no_copy_all_ui(copy_report, copy_page):
    page = copy_page
    path, _ = copy_report(enabled=False)
    content = path.read_text(encoding="utf-8")
    assert "Copy all links" not in content
    assert 'id="similar-errors-data"' not in content
    page.goto(path.as_uri())
    assert page.locator(".copy-all-links").count() == 0
    assert page.locator("#similar-errors-popover").count() == 0
    mock_clipboard(page, "success")
    individual = page.locator(".test-link-btn").first
    individual.click()
    expect(individual).to_have_text("✓")
    assert len(page.evaluate("window.copiedTexts")) == 1


def test_copy_control_does_not_duplicate_group_payload(copy_report):
    path, tests = copy_report()
    content = path.read_text(encoding="utf-8")
    payload = content.split('id="similar-errors-data">', 1)[1].split("</script>", 1)[0]
    groups = json.loads(payload)
    assert len(groups) == 1
    assert len(next(iter(groups.values()))["tests"]) == len(tests)
    # The button is created only when opening a popover, not repeated per test.
    assert 'class="inline-copy-btn copy-all-links"' not in content
