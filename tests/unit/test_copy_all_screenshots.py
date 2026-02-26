import os
import shutil


def test_copy_all_screenshots(tmp_path):
    screenshots_dir = tmp_path / "screenshots_src"
    output_dir = tmp_path / "output"
    screenshots_dir.mkdir()
    output_dir.mkdir()

    file_path = screenshots_dir / "test_example_fail.png"
    file_path.write_text("fake image content")

    class FakeReporter:
        def __init__(self, src, out):
            self.screenshots_dir = str(src)
            self.output_dir = str(out)

        def copy_all_screenshots(self):
            screenshots_output_dir = os.path.join(self.output_dir, "screenshots")
            os.makedirs(screenshots_output_dir, exist_ok=True)

            for root, _, files in os.walk(self.screenshots_dir):
                for file in files:
                    if file.endswith(".png"):
                        src_path = os.path.join(root, file)
                        dest_path = os.path.join(screenshots_output_dir, file)
                        if not os.path.exists(dest_path):
                            shutil.copyfile(src_path, dest_path)

    reporter = FakeReporter(screenshots_dir, output_dir)
    reporter.copy_all_screenshots()

    assert (output_dir / "screenshots" / "test_example_fail.png").exists()
