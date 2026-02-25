
attempt_counter = {"count": 0}

def test_flaky_network_call():
    attempt_counter["count"] += 1
    if attempt_counter["count"] == 1:
        assert False, "Simulated network failure"
    assert True
