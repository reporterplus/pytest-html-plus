from __future__ import annotations

from typing import Any

import requests

DEFAULT_TIMEOUT_SECONDS = 12


def build_upload_payload(api_key, data):
    raw_summary = data.get("summary", {})
    raw_tests = data.get("results", [])

    passed = raw_summary.get("passed", 0)
    total = raw_summary.get("total", len(raw_tests))
    failed = total - passed

    return {
        "api_key": api_key,
        "summary": {
            "passed": passed,
            "failed": failed,
            "skipped": raw_summary.get("skipped", 0),
        },
        "tests": raw_tests,
    }


def upload_report(api_url: str, api_key: str, payload: dict) -> bool:
    """Upload a normalized pytest report to a remote API endpoint.

    This function is intentionally defensive and must never raise exceptions
    back to the caller.
    """

    try:
        print(payload)
        test_count = len(payload.get("tests", []))
        print(f"Uploading {test_count} tests...")

        response = requests.post(
            api_url,
            json=payload,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )

        if response.status_code != 200:
            error_message = _extract_error_message(response)
            print(
                f"Upload failed ❌ HTTP {response.status_code}"
                f"{': ' + error_message if error_message else ''}"
            )
            return False

        run_id = _extract_run_id(response)
        if run_id:
            print(f"Upload successful ✅ Run ID: {run_id}")
        else:
            print("Upload successful ✅ Run ID: unknown")
        return True
    except requests.RequestException as exc:
        print(f"Upload failed ❌ Network error: {exc}")
        return False
    except Exception as exc:
        print(f"Upload failed ❌ Unexpected error: {exc}")
        return False


def _extract_run_id(response: requests.Response) -> str | None:
    try:
        data = response.json()
    except ValueError:
        return None
    except Exception:
        return None

    if not isinstance(data, dict):
        return None

    for key in ("run_id", "runId", "id"):
        value = data.get(key)
        if value is not None:
            return str(value)
    return None


def _extract_error_message(response: requests.Response) -> str:
    try:
        data: Any = response.json()
    except ValueError:
        text = (response.text or "").strip()
        return text[:200] if text else ""
    except Exception:
        return ""

    if isinstance(data, dict):
        for key in ("error", "message", "detail"):
            value = data.get(key)
            if value:
                return str(value)

    return str(data)[:200] if data else ""


if __name__ == "__main__":
    api_url = "https://us-central1-reporterplus-6f164.cloudfunctions.net/uploadReport"
    api_key = "rp_6fc4d3adb1746d8ed17fffcfd015409a"

    summary = {
        "total": 20,
        "passed": 10,
        "failed": 3,
        "skipped": 1,
        "flaky": 4,
        "total_duration": 22.5,
    }

    tests = [
        {
            "name": "test_login",
            "status": "failed",
            "duration": 1.2,
            "flaky": False,
            "file": "tests/test_login.py",
        },
        {
            "name": "test_login_flaky",
            "status": "failed",
            "duration": 1.2,
            "flaky": True,
            "file": "tests/test_login_flaky.py",
        },
    ]

    success = upload_report(
        api_url=api_url, api_key=api_key, summary=summary, tests=tests
    )
    print(f"Upload result: {success}")
