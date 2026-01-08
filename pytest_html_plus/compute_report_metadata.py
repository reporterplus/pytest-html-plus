import json
from datetime import datetime

from pytest_html_plus.utils import is_main_worker, get_env_marker, get_report_title, \
    get_python_version


def write_plus_metadata_if_main_worker(config, report_path, output_path="plus_metadata.json", **kwargs):
    if not is_main_worker():
        return
    branch = kwargs.get("git_branch", "NA")
    commit = kwargs.get("git_commit", "NA")
    metadata = {
        "report_title": get_report_title(output_path=report_path),
        "environment": get_env_marker(config),
        "branch": branch,
        "commit": commit,
        "python_version": get_python_version(),
        "generated_at": datetime.now().isoformat()
    }
    with open(output_path, "w") as f:
        print(metadata)
        json.dump(metadata, f, indent=2)
