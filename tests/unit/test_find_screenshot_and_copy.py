from pytest_html_plus.generate_html_report import JSONReporter


def test_find_screenshot_returns_relative_path(tmp_path):
    screenshots_src = tmp_path / "screenshots"
    output_dir = tmp_path / "output"
    screenshots_src.mkdir()
    output_dir.mkdir()

    (screenshots_src / "test_something_failure.png").write_bytes(b"fake-png")

    reporter = JSONReporter(
        screenshots_dir=str(screenshots_src),
        output_dir=str(output_dir),
    )
    rel_path = reporter.find_screenshot_and_copy("something")

    assert rel_path is not None
    assert rel_path.replace("\\", "/") == "screenshots/test_something_failure.png"


def test_find_screenshot_copies_file_to_output(tmp_path):
    screenshots_src = tmp_path / "screenshots"
    output_dir = tmp_path / "output"
    screenshots_src.mkdir()
    output_dir.mkdir()

    (screenshots_src / "test_login_failure.png").write_bytes(b"fake-png")

    reporter = JSONReporter(
        screenshots_dir=str(screenshots_src),
        output_dir=str(output_dir),
    )
    reporter.find_screenshot_and_copy("login")

    assert (output_dir / "screenshots" / "test_login_failure.png").exists()


def test_find_screenshot_returns_none_when_no_match(tmp_path):
    screenshots_src = tmp_path / "screenshots"
    output_dir = tmp_path / "output"
    screenshots_src.mkdir()
    output_dir.mkdir()

    (screenshots_src / "test_login_failure.png").write_bytes(b"fake-png")

    reporter = JSONReporter(
        screenshots_dir=str(screenshots_src),
        output_dir=str(output_dir),
    )
    result = reporter.find_screenshot_and_copy("checkout")

    assert result is None


def test_find_screenshot_returns_none_for_empty_dir(tmp_path):
    screenshots_src = tmp_path / "screenshots"
    output_dir = tmp_path / "output"
    screenshots_src.mkdir()
    output_dir.mkdir()

    reporter = JSONReporter(
        screenshots_dir=str(screenshots_src),
        output_dir=str(output_dir),
    )
    result = reporter.find_screenshot_and_copy("anything")

    assert result is None


def test_find_screenshot_partial_name_match(tmp_path):
    screenshots_src = tmp_path / "screenshots"
    output_dir = tmp_path / "output"
    screenshots_src.mkdir()
    output_dir.mkdir()

    (screenshots_src / "test_user_profile_update_failure.png").write_bytes(b"fake-png")

    reporter = JSONReporter(
        screenshots_dir=str(screenshots_src),
        output_dir=str(output_dir),
    )
    result = reporter.find_screenshot_and_copy("profile")

    assert result is not None
    assert "profile" in result


def test_find_screenshot_ignores_non_png_files(tmp_path):
    screenshots_src = tmp_path / "screenshots"
    output_dir = tmp_path / "output"
    screenshots_src.mkdir()
    output_dir.mkdir()

    (screenshots_src / "test_login_failure.jpg").write_bytes(b"fake-jpg")
    (screenshots_src / "test_login_failure.png").write_bytes(b"fake-png")

    reporter = JSONReporter(
        screenshots_dir=str(screenshots_src),
        output_dir=str(output_dir),
    )
    result = reporter.find_screenshot_and_copy("login")

    assert result is not None
    assert result.endswith(".png")


def test_find_screenshot_finds_in_nested_subdir(tmp_path):
    screenshots_src = tmp_path / "screenshots"
    nested = screenshots_src / "subdir"
    output_dir = tmp_path / "output"
    nested.mkdir(parents=True)
    output_dir.mkdir()

    (nested / "test_nested_failure.png").write_bytes(b"fake-png")

    reporter = JSONReporter(
        screenshots_dir=str(screenshots_src),
        output_dir=str(output_dir),
    )
    result = reporter.find_screenshot_and_copy("nested")

    assert result is not None
    assert (output_dir / "screenshots" / "test_nested_failure.png").exists()


def test_find_screenshot_preserves_file_content(tmp_path):
    screenshots_src = tmp_path / "screenshots"
    output_dir = tmp_path / "output"
    screenshots_src.mkdir()
    output_dir.mkdir()

    original = b"\x89PNG\r\nreal-png-data"
    (screenshots_src / "test_visual_failure.png").write_bytes(original)

    reporter = JSONReporter(
        screenshots_dir=str(screenshots_src),
        output_dir=str(output_dir),
    )
    reporter.find_screenshot_and_copy("visual")

    copied = (output_dir / "screenshots" / "test_visual_failure.png").read_bytes()
    assert copied == original
