"""
Simulated flaky test — fails on the first attempt, passes on retry.
Demonstrates flaky test detection in the HTML report.
Requires --reruns 1 (included in `make test`).
"""

attempt_counter = {"count": 0}


def test_flaky_network_call():
    attempt_counter["count"] += 1
    if attempt_counter["count"] == 1:
        assert False, "Simulated network failure"
    assert True
