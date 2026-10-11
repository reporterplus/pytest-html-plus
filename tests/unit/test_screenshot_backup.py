"""Screenshot backup tests"""

import textwrap

HTML_OUTPUT = "report_output"

FAKE_PAGE_CONFTEST = textwrap.dedent(
    """\
    import pytest
    from pathlib import Path

    class FakePage:
        def __init__(self):
            self.called = False

        def screenshot(self, path):
            self.called = True
            Path(path).write_bytes(b"fake-png-screenshot-bytes")

    @pytest.fixture
    def page():
        return FakePage()
    """
)


def test_screenshot_retained_with_plus_no_html(pytester):
    """When --plus-no-html is set, the screenshot is directly stored in
    <html_output>/screenshots/ and not deleted.
    """
    pytester.makepyfile(
        textwrap.dedent(
            """\
            def test_ui_failure(page):
                assert False, "html-plus-screenshot fail"
            """
        )
    )
    pytester.makeconftest(FAKE_PAGE_CONFTEST)

    result = pytester.runpytest("--html-output", HTML_OUTPUT, "--plus-no-html")
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["*AssertionError: html-plus-screenshot fail*"])

    dest_dir = pytester.path / HTML_OUTPUT / "screenshots"
    assert dest_dir.exists()

    screenshots = list(dest_dir.glob("*.png"))
    assert len(screenshots) == 1
    assert "test_ui_failure_failure.png" in screenshots[0].name
    assert screenshots[0].read_bytes() == b"fake-png-screenshot-bytes"

    assert not (pytester.path / HTML_OUTPUT / "report.html").exists()


def test_screenshot_with_custom_screenshot(pytester):
    """When --plus-no-html and --screenshot is set, the screenshot should been copied
    the custome should been delete
    """
    pytester.makepyfile(
        textwrap.dedent(
            """\
            def test_ui_failure(page):
                assert False, "html-plus-screenshot fail"
            """
        )
    )
    pytester.makeconftest(FAKE_PAGE_CONFTEST)

    result = pytester.runpytest(
        "--html-output", HTML_OUTPUT, "--screenshots=cc", "--plus-no-html"
    )
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["*AssertionError: html-plus-screenshot fail*"])

    dest_dir = pytester.path / HTML_OUTPUT / "screenshots"
    assert dest_dir.exists(), f"Destination directory {dest_dir} does not exist"
    screenshots = list(dest_dir.glob("*.png"))
    assert len(screenshots) == 1
    assert "test_ui_failure_failure.png" in screenshots[0].name
    assert screenshots[0].read_bytes() == b"fake-png-screenshot-bytes"

    root_screenshots = pytester.path / "cc"
    assert not root_screenshots.exists(), "Root screenshots directory should delete"

    assert not (pytester.path / HTML_OUTPUT / "report.html").exists()


def test_screenshot_same_directory(pytester) -> None:
    """When screeshots same as html_out shuold keep the directory"""
    pytester.makepyfile(
        textwrap.dedent(
            """\
            def test_ui_failure(page):
                assert False, "html-plus-screenshot fail"
            """
        )
    )
    pytester.makeconftest(FAKE_PAGE_CONFTEST)

    result = pytester.runpytest(
        "--html-output",
        HTML_OUTPUT,
        "--screenshots=report_output/screenshots",
        "--plus-no-html",
    )
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(["*AssertionError: html-plus-screenshot fail*"])

    dest_dir = pytester.path / HTML_OUTPUT / "screenshots"
    assert dest_dir.exists(), f"Destination directory {dest_dir} does not exist"
    screenshots = list(dest_dir.glob("*.png"))
    assert len(screenshots) == 1
    assert "test_ui_failure_failure.png" in screenshots[0].name
    assert screenshots[0].read_bytes() == b"fake-png-screenshot-bytes"
