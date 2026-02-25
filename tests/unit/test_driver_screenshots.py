from unittest.mock import Mock

from pytest_html_plus.resolver_driver import resolve_driver


def test_resolve_driver_prefers_page_over_others():
    mock_driver = Mock()
    mock_driver.screenshot = Mock()

    item = Mock()
    item.funcargs = {
        "page": mock_driver,
        "driver": Mock(),
        "browser": Mock()
    }

    assert resolve_driver(item) is mock_driver


def test_resolve_driver_fallback_to_driver():
    mock_driver = Mock()
    mock_driver.screenshot = Mock()

    item = Mock()
    item.funcargs = {
        "driver": mock_driver
    }

    assert resolve_driver(item) is mock_driver


def test_resolve_driver_fallback_to_browser():
    mock_driver = Mock()
    mock_driver.screenshot = Mock()

    item = Mock()
    item.funcargs = {
        "browser": mock_driver
    }

    assert resolve_driver(item) is mock_driver


def test_resolve_driver_uses_page_for_screenshot_attr():
    mock_driver = Mock()
    mock_driver.screenshot = Mock()

    item = Mock()
    item.funcargs = {}
    item.page_for_screenshot = mock_driver

    assert resolve_driver(item) is mock_driver


def test_resolve_driver_fallback_on_object_with_screenshot_method():
    mock_driver = Mock()
    mock_driver.screenshot = Mock()
    item = Mock()
    item.funcargs = {"custom": mock_driver}
    item.page_for_screenshot = None
    assert resolve_driver(item) is mock_driver


def test_resolve_driver_fallback_on_object_with_save_screenshot():
    mock_driver = Mock()
    mock_driver.save_screenshot = Mock()
    item = Mock()
    item.funcargs = {"custom": mock_driver}
    item.page_for_screenshot = None
    assert resolve_driver(item) is mock_driver


def test_resolve_driver_returns_none_when_no_match():
    item = Mock()
    item.funcargs = {"x": object()}
    item.page_for_screenshot = None
    assert resolve_driver(item) is None

import os
from unittest.mock import patch

from pytest_html_plus.resolver_driver import take_screenshot_generic


@patch("os.makedirs")
def test_take_screenshot_with_screenshot_method(mock_makedirs):
    mock_driver = Mock()
    mock_driver.screenshot = Mock()
    item = Mock()
    item.name = "test_case"

    result = take_screenshot_generic("screenshots", item, mock_driver)

    expected_path = os.path.join("screenshots", "test_case_failure.png")
    mock_makedirs.assert_called_once_with("screenshots", exist_ok=True)
    mock_driver.screenshot.assert_called_once_with(path=expected_path)
    assert result == expected_path


@patch("os.makedirs")
def test_take_screenshot_with_save_screenshot_method(mock_makedirs):
    mock_driver = Mock()
    if hasattr(mock_driver, "screenshot"):
        delattr(mock_driver, "screenshot")
    mock_driver.save_screenshot = Mock()

    item = Mock()
    item.name = "test_case"

    result = take_screenshot_generic("screenshots", item, mock_driver)

    expected_path = os.path.join("screenshots", "test_case_failure.png")
    mock_makedirs.assert_called_once_with("screenshots", exist_ok=True)
    mock_driver.save_screenshot.assert_called_once_with(expected_path)
    assert result == expected_path


@patch("os.makedirs")
def test_take_screenshot_raises_on_invalid_driver(mock_makedirs):
    mock_driver = object()  # No screenshot or save_screenshot
    item = Mock()
    item.name = "test_invalid"

    try:
        take_screenshot_generic("screenshots", item, mock_driver)
    except RuntimeError as e:
        assert "no screenshot method" in str(e).lower()
    else:
        assert False, "Expected RuntimeError was not raised"


from unittest.mock import patch

from pytest_html_plus.plugin import take_screenshot_generic


@patch("pytest_html_plus.plugin.os.makedirs")
@patch("pytest_html_plus.plugin.os.path.join", return_value="custom_dir/custom_file.png")
def test_take_screenshot_with_custom_path(mock_join, mock_makedirs):
    mock_driver = Mock()
    mock_driver.screenshot = Mock()

    item = Mock()
    item.name = "custom_test"

    path = take_screenshot_generic("custom_dir", item, mock_driver)

    mock_makedirs.assert_called_once_with("custom_dir", exist_ok=True)
    mock_join.assert_called_once_with("custom_dir", "custom_test_failure.png")
    mock_driver.screenshot.assert_called_once_with(path="custom_dir/custom_file.png")
    assert path == "custom_dir/custom_file.png"

