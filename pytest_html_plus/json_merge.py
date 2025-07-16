import json
import os
from collections import defaultdict
from pytest_html_plus.compute_filter_counts import compute_filter_count


def merge_json_reports(directory=".pytest_worker_jsons", output_path="final_report.json"):
   all_tests = []
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

   # Group tests by nodeid
   tests_by_nodeid = defaultdict(list)
   for test in all_tests:
       nodeid = test.get("nodeid") or test.get("test")  # fallback if needed
       tests_by_nodeid[nodeid].append(test)

   # Create merged results with flaky info
   merged_results = []
   for nodeid, attempts in tests_by_nodeid.items():
       final_test = attempts[-1].copy()
       statuses = [t.get("status") for t in attempts]
       unique_statuses = set(statuses)

       # Mark flaky only if test status changed across runs
       final_test["flaky"] = len(unique_statuses) > 1
       final_test["flaky_attempts"] = statuses

       merged_results.append(final_test)

   report_data = {
       "filters": compute_filter_count(merged_results),
       "results": merged_results
   }

   try:
       with open(output_path, "w", encoding="utf-8") as f:
           json.dump(report_data, f, indent=2)
   except OSError as e:
       raise RuntimeError(f"Failed to write merged report to {output_path}: {e}") from e


   
