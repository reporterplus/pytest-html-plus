import json
import pytest

from pytest_html_plus.json_merge import merge_json_reports


# Sample test inputs
basic_test_list = [
    {"nodeid": "test_1", "status": "passed", "markers": [], "links": []},
    {"nodeid": "test_2", "status": "failed", "markers": ["flaky"], "links": []},
    {"nodeid": "test_3", "status": "error", "markers": [], "links": []}
]

wrapped_test_dict = {
    "results": [
        {"nodeid": "test_3", "status": "skipped", "markers": [], "links": []},
        {"nodeid": "test_2", "status": "passed", "markers": ["flaky"], "links": []},  # Same nodeid as above
    ]
}


@pytest.fixture
def mock_json_files(tmp_path):
    file1 = tmp_path / "file1.json"
    file1.write_text(json.dumps(basic_test_list))

    file2 = tmp_path / "file2.json"
    file2.write_text(json.dumps(wrapped_test_dict))

    return tmp_path


def test_merge_json_reports_creates_merged_file(mock_json_files):
    output_file = mock_json_files / "merged.json"

    merge_json_reports(directory=str(mock_json_files), output_path=str(output_file))

    assert output_file.exists()

    with open(output_file) as f:
        data = json.load(f)

    assert "results" in data
    assert "filters" in data

    results = data["results"]
    nodeids = [t["nodeid"] for t in results]

    assert "test_2" in nodeids
    assert len(results) == 3  # test_1, test_2, test_3

    for test in results:
        if test["nodeid"] == "test_2":
            assert test["flaky"] is True
            assert "flaky_attempts" in test


def test_merge_json_reports_handles_bad_json(tmp_path):
    bad_file = tmp_path / "broken.json"
    bad_file.write_text("{ not json }")

    with pytest.raises(ValueError, match="Could not parse"):
        merge_json_reports(directory=str(tmp_path))


def test_merge_json_reports_handles_empty_directory(tmp_path):
    output = tmp_path / "result.json"
    merge_json_reports(directory=str(tmp_path), output_path=str(output))

    assert output.exists()

    with open(output) as f:
        data = json.load(f)

    assert data["results"] == []
    assert "filters" in data


def test_compute_filter_count_failed_non_flaky():
    from pytest_html_plus.compute_filter_counts import compute_filter_count

    results = [
        {
            "status": "failed",
            "flaky": False,
            "links": ["some-link"],
            "markers": ["smoke"]
        }
    ]

    filters = compute_filter_count(results)
    assert filters["failed"] == 1
    assert filters.get("flaky") is None
    assert filters.get("skipped") is None
    assert filters.get("untracked") is None
    assert filters["passed"] == 0
    assert filters["total"] == 1
    assert filters["marker_counts"]["smoke"] == 1

def test_compute_filter_count_error_non_flaky():
    from pytest_html_plus.compute_filter_counts import compute_filter_count

    results = [
        {
            "status": "error",
            "flaky": False,
            "links": ["some-link"],
            "markers": ["setup"]
        }
    ]

    filters = compute_filter_count(results)

    assert filters["error"] == 1
    assert filters.get("failed") is None
    assert filters.get("flaky") is None
    assert filters.get("skipped") is None
    assert filters["passed"] == 0
    assert filters["total"] == 1
    assert filters["marker_counts"]["setup"] == 1

