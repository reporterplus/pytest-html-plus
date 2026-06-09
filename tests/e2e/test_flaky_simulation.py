"""
Simulated flaky test — fails on the first attempt, passes on retry.
Demonstrates flaky test detection in the HTML report.
Requires --reruns 1 (included in `make test`).
"""

import threading

attempt_counter = {"count": 0}
attempt_lock = threading.Lock()


def test_flaky_network_call():
    with attempt_lock:
        attempt_counter["count"] += 1
        is_first_attempt = attempt_counter["count"] == 1

    if is_first_attempt:
        assert False, "Simulated network failure"
    assert True
