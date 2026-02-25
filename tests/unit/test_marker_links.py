from unittest.mock import MagicMock

from pytest_html_plus.extract_link import extract_links_from_item


def test_extract_links_with_multiple_marker_names():
    item = MagicMock()

    marker_data = {
        "link": [MagicMock(args=["https://some.link/test1"])],
        "testcase": [MagicMock(args=["TC-123"])],
        "jira": [],
        "issue": [MagicMock(args=["ISSUE-999"])],
        "ticket": [MagicMock(args=[])],
    }

    def iter_markers_side_effect(name):
        return marker_data.get(name, [])

    item.iter_markers.side_effect = iter_markers_side_effect

    result = extract_links_from_item(item)

    assert result == ["https://some.link/test1", "TC-123", "ISSUE-999"]


def test_extract_links_with_no_markers():
    item = MagicMock()
    item.iter_markers.return_value = []
    result = extract_links_from_item(item)
    assert result == []


def test_extract_links_with_non_string_args():
    item = MagicMock()
    item.iter_markers.side_effect = lambda name: [MagicMock(args=[123, True])] if name == "link" else []
    result = extract_links_from_item(item)
    assert result == ["123", "True"]
