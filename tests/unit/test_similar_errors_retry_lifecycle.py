"""Setup, call, and teardown retry badge demo (manual only; disabled by default).

Enable only when manually inspecting Similar Errors badges:
1. Uncomment the entire block below, including imports, fixtures, and helpers.
2. Run:
   pytest tests/unit/test_similar_errors_retry_lifecycle.py \
       --plus-similar-errors=true --html-output=report_output_retry_lifecycle
3. Inspect report_output_retry_lifecycle/report.html.
4. Comment the block out again before committing or running the normal suite.

These scenarios intentionally fail and are not automated coverage tests.
Automated coverage remains active in tests/unit/test_similar_errors.py.
"""

# BEGIN MANUAL DEMO — uncomment only for manual badge inspection.
# import pytest
#
# pytestmark = pytest.mark.flaky(reruns=2)
#
# FINAL_ERROR = "Account service unavailable after retry exhaustion"
# ERRORS = {
#     "setup": (
#         "Setup credentials could not be loaded",
#         "Setup connection could not be established",
#         FINAL_ERROR,
#     ),
#     "call": (
#         "Account response contained an invalid payload",
#         "Account response exceeded the request deadline",
#         FINAL_ERROR,
#     ),
#     "teardown": (
#         "Cleanup session could not be closed",
#         "Cleanup resources could not be released",
#         FINAL_ERROR,
#     ),
# }
#
#
# def next_attempt(request, phase):
#     key = f"_similar_errors_{phase}_attempt"
#     attempt = getattr(request.node, key, 0) + 1
#     setattr(request.node, key, attempt)
#     return attempt
#
#
# @pytest.fixture
# def setup_fails(request):
#     attempt = next_attempt(request, "setup")
#     raise RuntimeError(ERRORS["setup"][attempt - 1])
#
#
# def test_setup_fails_on_all_attempts(setup_fails):
#     pytest.fail("The test body must not run when setup fails")
#
#
# def test_call_fails_on_all_attempts(request):
#     attempt = next_attempt(request, "call")
#     raise RuntimeError(ERRORS["call"][attempt - 1])
#
#
# @pytest.fixture
# def teardown_fails(request):
#     attempt = next_attempt(request, "teardown")
#     yield attempt
#     raise RuntimeError(ERRORS["teardown"][attempt - 1])
#
#
# def test_teardown_fails_on_all_attempts(teardown_fails):
#     assert teardown_fails in (1, 2, 3)
# END MANUAL DEMO
