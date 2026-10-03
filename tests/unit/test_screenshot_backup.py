import subprocess
import sys
import textwrap

HTML_OUTPUT = "report_output"


def run_pytest_in_tmp(tmp_path, test_source, extra_args=None):
    test_file = tmp_path / "test_sample.py"
    test_file.write_text(textwrap.dedent(test_source))

    conftest = tmp_path / "conftest.py"
    conftest.write_text(
        textwrap.dedent(
            """\
        import pytest

        def pytest_configure(config):
            config.addinivalue_line("markers", "smoke: smoke tests")
            config.addinivalue_line("markers", "regression: regression tests")

        class FakePage:
            def __init__(self):
                self.called = False

            def screenshot(self, path):
                self.called = True
                with open(path, "wb") as f:
                    f.write(b"fake-png-screenshot-bytes")

        @pytest.fixture
        def page():
            return FakePage()
    """
        )
    )

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(test_file),
        f"--html-output={HTML_OUTPUT}",
        # "--json-report=final_report.json",
        # "--tb=short",
        "-p",
        "no:cacheprovider",
    ]
    if extra_args:
        cmd.extend(extra_args)

    result = subprocess.run(cmd, cwd=str(tmp_path), capture_output=True, text=True)
    return result


def test_screenshot_retained_with_plus_no_html(tmp_path):
    """When --plus-no-html is set, the screenshot is directly stored in

    <html_output>/screenshots/ and not deleted.
    """
    test_code = """
        def test_ui_failure(page):
            assert False, "UI fail"
    """
    result = run_pytest_in_tmp(tmp_path, test_code, extra_args=["--plus-no-html"])
    assert result.returncode != 0

    dest_dir = tmp_path / HTML_OUTPUT / "screenshots"
    assert dest_dir.exists()

    screenshots = list(dest_dir.glob("*.png"))
    assert len(screenshots) == 1

    # report.html should not exist
    assert not (tmp_path / HTML_OUTPUT / "report.html").exists()


def test_screenshot_with_custom_screenshot(tmp_path):
    """When --plus-no-html and --screenshot is set, the screenshot shouold been copied

    the custome should been delete
    """
    test_code = """
        def test_ui_failure(page):
            assert False, "UI fail"
    """

    result = run_pytest_in_tmp(
        tmp_path, test_code, extra_args=["--screenshots=cc", "--plus-no-html"]
    )
    assert result.returncode != 0

    # 1. Screenshot should exist been copied from --screenshots
    dest_dir = tmp_path / HTML_OUTPUT / "screenshots"
    assert dest_dir.exists(), f"Destination directory {dest_dir} does not exist"
    screenshots = list(dest_dir.glob("*.png"))
    assert len(screenshots) == 1
    assert "test_ui_failure_failure.png" in screenshots[0].name
    assert screenshots[0].read_bytes() == b"fake-png-screenshot-bytes"

    # 2. Raw screenshot should been delete
    root_screenshots = tmp_path / "cc"
    assert not root_screenshots.exists(), "Root screenshots directory should delete"

    # 3. report.html should not exist
    assert not (tmp_path / HTML_OUTPUT / "report.html").exists()


def test_screenshot_same_directory(tmp_path) -> None:
    """When screeshots same as html_out shuold keep the directory"""
    test_code = """
            def test_ui_failure(page):
                assert False, "UI fail"
        """

    result = run_pytest_in_tmp(
        tmp_path,
        test_code,
        extra_args=["--screenshots=report_output/screenshot", "--plus-no-html"],
    )
    assert result.returncode != 0

    # 1. Screenshot should exist been copied from --screenshots
    dest_dir = tmp_path / HTML_OUTPUT / "screenshots"
    assert dest_dir.exists(), f"Destination directory {dest_dir} does not exist"
    screenshots = list(dest_dir.glob("*.png"))
    assert len(screenshots) == 1
    assert "test_ui_failure_failure.png" in screenshots[0].name
    assert screenshots[0].read_bytes() == b"fake-png-screenshot-bytes"
