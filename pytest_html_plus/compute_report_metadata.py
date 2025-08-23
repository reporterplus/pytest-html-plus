import json
from datetime import datetime

from pytest_html_plus.utils import is_main_worker, get_env_marker, get_git_branch, get_git_commit, get_report_title, \
    get_python_version


def write_plus_metadata_if_main_worker(config, report_path, output_path="plus_metadata.json"):
    if not is_main_worker():
        return
    metadata = {
        "report_title": get_report_title(output_path=report_path),
        "environment": get_env_marker(config),
        "branch": get_git_branch(),
        "commit": get_git_commit(),
        "python_version": get_python_version(),
        "generated_at": datetime.now().isoformat()
    }
    with open(output_path, "w") as f:
        print(metadata)
        json.dump(metadata, f, indent=2)
