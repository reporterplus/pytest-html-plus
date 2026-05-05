from pytest_html_plus.generate_html_report import JSONReporter


def test_copy_all_screenshots_copies_png_files(tmp_path):
    screenshots_src = tmp_path / "screenshots"
    output_dir = tmp_path / "output"
    screenshots_src.mkdir()
    output_dir.mkdir()

    (screenshots_src / "test_login_failure.png").write_bytes(b"fake-png")
    (screenshots_src / "test_checkout_failure.png").write_bytes(b"fake-png")

    reporter = JSONReporter(
        screenshots_dir=str(screenshots_src),
        output_dir=str(output_dir),
    )
    reporter.copy_all_screenshots()

    screenshots_out = output_dir / "screenshots"
    assert (screenshots_out / "test_login_failure.png").exists()
    assert (screenshots_out / "test_checkout_failure.png").exists()


def test_copy_all_screenshots_ignores_non_png_files(tmp_path):
    screenshots_src = tmp_path / "screenshots"
    output_dir = tmp_path / "output"
    screenshots_src.mkdir()
    output_dir.mkdir()

    (screenshots_src / "test_login_failure.png").write_bytes(b"fake-png")
    (screenshots_src / "notes.txt").write_text("not an image")

    reporter = JSONReporter(
        screenshots_dir=str(screenshots_src),
        output_dir=str(output_dir),
    )
    reporter.copy_all_screenshots()

    screenshots_out = output_dir / "screenshots"
    assert (screenshots_out / "test_login_failure.png").exists()
    assert not (screenshots_out / "notes.txt").exists()


def test_copy_all_screenshots_does_not_overwrite_existing(tmp_path):
    screenshots_src = tmp_path / "screenshots"
    output_dir = tmp_path / "output"
    screenshots_out = output_dir / "screenshots"
    screenshots_src.mkdir()
    screenshots_out.mkdir(parents=True)

    (screenshots_src / "test_a_failure.png").write_bytes(b"new-content")
    existing = screenshots_out / "test_a_failure.png"
    existing.write_bytes(b"original-content")

    reporter = JSONReporter(
        screenshots_dir=str(screenshots_src),
        output_dir=str(output_dir),
    )
    reporter.copy_all_screenshots()

    assert existing.read_bytes() == b"original-content"


def test_copy_all_screenshots_empty_source_dir(tmp_path):
    screenshots_src = tmp_path / "screenshots"
    output_dir = tmp_path / "output"
    screenshots_src.mkdir()
    output_dir.mkdir()

    reporter = JSONReporter(
        screenshots_dir=str(screenshots_src),
        output_dir=str(output_dir),
    )
    reporter.copy_all_screenshots()

    screenshots_out = output_dir / "screenshots"
    assert screenshots_out.exists()
    assert list(screenshots_out.iterdir()) == []


def test_copy_all_screenshots_creates_output_dir_if_missing(tmp_path):
    screenshots_src = tmp_path / "screenshots"
    output_dir = tmp_path / "output"
    screenshots_src.mkdir()

    (screenshots_src / "test_failure.png").write_bytes(b"fake-png")

    reporter = JSONReporter(
        screenshots_dir=str(screenshots_src),
        output_dir=str(output_dir),
    )
    reporter.copy_all_screenshots()

    assert (output_dir / "screenshots" / "test_failure.png").exists()


def test_copy_all_screenshots_handles_nested_subdirectories(tmp_path):
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
    reporter.copy_all_screenshots()

    assert (output_dir / "screenshots" / "test_nested_failure.png").exists()


def test_copy_all_screenshots_preserves_file_content(tmp_path):
    screenshots_src = tmp_path / "screenshots"
    output_dir = tmp_path / "output"
    screenshots_src.mkdir()
    output_dir.mkdir()

    original_content = b"\x89PNG\r\nactual-png-bytes"
    (screenshots_src / "test_visual_failure.png").write_bytes(original_content)

    reporter = JSONReporter(
        screenshots_dir=str(screenshots_src),
        output_dir=str(output_dir),
    )
    reporter.copy_all_screenshots()

    copied = (output_dir / "screenshots" / "test_visual_failure.png").read_bytes()
    assert copied == original_content
