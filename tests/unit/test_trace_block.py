from pytest_html_plus.utils import extract_trace_block

def test_trace_block_basic():
    trace = "line 1\nline 2\nE this is an error\nline 4"
    expected = "line 1\nline 2"
    assert extract_trace_block(trace) == expected

def test_trace_block_with_leading_spaces():
    trace = "   line 1\n    line 2\n  E this is an error"
    expected = "   line 1\n    line 2"
    actual = extract_trace_block(trace)
    assert repr(expected) == repr(actual)

def test_trace_block_no_error_line():
    trace = "line 1\nline 2\nline 3"
    expected = "line 1\nline 2\nline 3"
    assert extract_trace_block(trace) == expected

def test_trace_block_empty():
    assert extract_trace_block("") == ""

def test_trace_block_none():
    assert extract_trace_block(None) == ""

def test_trace_block_only_error_line():
    trace = "E error line"
    assert extract_trace_block(trace) == ""

def test_extract_trace_block_with_invalid_input():
    # Pass a non-string input to trigger exception
    result = extract_trace_block(12345)
    assert result.startswith("[Error extracting trace block:")

    result = extract_trace_block(None)
    assert result == ""  # None is handled

    result = extract_trace_block(["this", "is", "a", "list"])
    assert result.startswith("[Error extracting trace block:")

