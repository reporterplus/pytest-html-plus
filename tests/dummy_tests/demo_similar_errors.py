"""Basic matching-failure badge demo (manual only; disabled by default).

Enable only when manually inspecting Similar Errors badges:
1. Uncomment the entire block below, including imports, fixtures, and helpers.
2. Run:
   pytest tests/dummy_tests/demo_similar_errors.py \
       --plus-similar-errors=true --html-output=report_output_similar_errors
3. Inspect report_output_similar_errors/report.html.
4. Comment the block out again before committing or running the normal suite.

These scenarios intentionally fail and are not automated coverage tests.
Automated coverage remains active in tests/unit/test_similar_errors.py.
"""

# BEGIN MANUAL DEMO — uncomment only for manual badge inspection.
# import pytest
#
#
# @pytest.mark.parametrize("page", ["login", "checkout", "search", "profile"])
# def test_matching_account_errors(page):
#     """Four matching failures should each display '3 similar errors'."""
#     raise ValueError("Account service returned an invalid response")
#
#
# @pytest.fixture
# def unavailable_database():
#     raise RuntimeError("Database connection refused for reporting service")
#
#
# def test_database_setup_one(unavailable_database):
#     pass
#
#
# def test_database_setup_two(unavailable_database):
#     pass
#
#
# def test_unrelated_failure():
#     """This distinct failure must not have a similarity badge."""
#     raise AssertionError("Expected checkout total to include delivery")
#
#
# def test_passing_control():
#     """Passing tests must not have a similarity badge."""
#     assert 2 + 2 == 4
# END MANUAL DEMO
