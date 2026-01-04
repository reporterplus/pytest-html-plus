import pytest

class FakePage:
    def __init__(self, screenshot_dir):
        self.screenshot_dir = screenshot_dir
        self.called = False

    def screenshot(self, path):
        self.called = True
        with open(path, "wb") as f:
            f.write(b"fake-png-data")


@pytest.fixture
def failing_ui_fixture(tmp_path):
    page = FakePage(tmp_path)

    # simulate Playwright-style attachment
    yield page

    # teardown never reached, but fixture exists

@pytest.fixture
def broken_ui_fixture(failing_ui_fixture):
    raise RuntimeError("UI setup failed")

def test_ui_fixture_failure_captures_screenshot(
    tmp_path, monkeypatch
):
    from pytest_html_plus.plugin import take_screenshot_generic

    screenshots_dir = tmp_path / "screenshots"
    screenshots_dir.mkdir()

    page = FakePage(screenshots_dir)

    # simulate resolve_driver returning page
    monkeypatch.setattr(
        "pytest_html_plus.plugin.resolve_driver",
        lambda item: page
    )

    # simulate pytest item
    class FakeItem:
        name = "test_ui_failure"
        nodeid = "test_ui.py::test_ui_failure"
        location = ("test_ui.py", 10, "test_ui_failure")
        funcargs = {}

    item = FakeItem()

    screenshot_path = take_screenshot_generic(
        str(screenshots_dir),
        item,
        page
    )

    # Assertions
    assert page.called is True
    assert screenshot_path is not None
    assert screenshot_path.endswith(".png")

    assert len(list(screenshots_dir.glob("*.png"))) == 1

