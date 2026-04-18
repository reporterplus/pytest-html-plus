import json
import os
from collections import defaultdict

from pytest_html_plus.compute_filter_counts import compute_filter_count
from pytest_html_plus.utils import build_error_meta


def merge_json_reports(
    directory=".pytest_worker_jsons", output_path="final_report.json"
):
    all_tests = []

    # Collect all test results
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath) as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_tests.extend(data)
                    elif isinstance(data, dict) and "results" in data:
                        all_tests.extend(data["results"])
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    raise ValueError(f"Could not parse {filename}: {e}") from e

    # Group by nodeid
    tests_by_nodeid = defaultdict(list)
    for test in all_tests:
        nodeid = test.get("nodeid") or test.get("test")
        tests_by_nodeid[nodeid].append(test)

    merged_results = []

    for nodeid, attempts in tests_by_nodeid.items():
        if not attempts:
            continue

        # Sort attempts chronologically
        attempts.sort(key=lambda x: x.get("timestamp") or "")

        final_test = attempts[-1].copy()

        # If attempts already exist inside test, use them
        if "attempts" in final_test and final_test["attempts"]:
            statuses = [a.get("status", "unknown") for a in final_test["attempts"]]
        else:
            statuses = [t.get("status", "unknown") for t in attempts]
        final_status = statuses[-1]

        had_prior_failure = any(s in ("failed", "error") for s in statuses[:-1])

        # Flaky detection
        final_test["flaky"] = final_status == "passed" and had_prior_failure

        # Attempt metadata
        final_test["attempt_statuses"] = statuses

        if "attempts" in final_test and final_test["attempts"]:
            simplified_attempts = final_test["attempts"]
        else:
            simplified_attempts = [
                {
                    "status": t.get("status"),
                    "trace": t.get("trace"),
                    "error": t.get("error"),
                    "duration": t.get("duration"),
                    "timestamp": t.get("timestamp"),
                }
                for t in attempts
            ]

        final_test["attempts"] = simplified_attempts
        final_test["attempt_count"] = len(simplified_attempts)

        if "attempts" in final_test and final_test["attempts"]:
            simplified_attempts = final_test["attempts"]
        else:
            simplified_attempts = [
                {
                    "status": t.get("status"),
                    "trace": t.get("trace"),
                    "error": t.get("error"),
                    "duration": t.get("duration"),
                    "timestamp": t.get("timestamp"),
                }
                for t in attempts
            ]

        final_test["attempts"] = simplified_attempts

        # First failure detection
        first_failure_index = next(
            (i for i, s in enumerate(statuses) if s in ("failed", "error")),
            None,
        )

        final_test["first_failure_index"] = first_failure_index

        final_test["first_failure"] = (
            simplified_attempts[first_failure_index]
            if first_failure_index is not None
            else None
        )

        error_meta = None
        error_source = None

        if final_test.get("first_failure"):
            error_source = final_test["first_failure"].get("error")
        else:
            error_source = final_test.get("error")

        if error_source:
            try:
                print("\n--- DEBUG START ---")
                print("nodeid:", nodeid)
                print("first_failure:", final_test.get("first_failure"))
                print("error_source:", error_source)
                print("--- DEBUG END ---\n")
                print("BUILD META INPUT:", error_source)

                error_meta = build_error_meta({"error": error_source})

                print("BUILD META OUTPUT:", error_meta)
                error_meta = build_error_meta({"error": error_source})
            except Exception as e:
                print("ERROR IN build_error_meta:", e)
                raise

        # if error_meta:
            final_test["error_meta"] = error_meta

        merged_results.append(final_test)

    # Final report structure
    report_data = {
        "filters": compute_filter_count(merged_results),
        "results": merged_results,
    }

    # Write output
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
    except OSError as e:
        raise RuntimeError(
            f"Failed to write merged report to {output_path}: {e}"
        ) from e
