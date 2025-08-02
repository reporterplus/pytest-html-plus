import json
from datetime import datetime

from pytest_html_plus.utils import is_main_worker, get_env_marker, get_git_branch, get_git_commit


def write_plus_metadata_if_main_worker(config, output_path="plus_metadata.json"):
    if not is_main_worker():
        return
    print(get_env_marker(config))
    metadata = {
        "report_title": "Automated Test Report",
        "environment": get_env_marker(config),
        "branch": get_git_branch(),
        "commit": get_git_commit(),
        "generated_at": datetime.now().isoformat()
    }
    print(metadata)

    with open(output_path, "w") as f:
        print(metadata)
        json.dump(metadata, f, indent=2)
