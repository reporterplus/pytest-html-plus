import platform
import subprocess
import shutil
import os

def get_env_marker(config):
    for arg in ("--env", "--environment"):
        if config.getoption(arg.lstrip("-").replace("-", "_"), default=None):
            return config.getoption(arg.lstrip("-").replace("-", "_"))
    return "NA"

def get_report_title(output_path):
    report_path = output_path
    report_filename = os.path.basename(report_path)
    report_title = os.path.splitext(report_filename)[0]
    return report_title

def extract_trace_block(trace: str) -> str:
    try:
        if not trace:
            return ""
        lines = trace.splitlines()
        trace_lines = []

        for line in lines:
            if line.lstrip().startswith("E "):
                break
            trace_lines.append(line)
        return "\n".join(trace_lines)
    except Exception as e:
        return f"[Error extracting trace block: {e}]"


def extract_error_block(error: str) -> str:
    try:
        if not error:
            return ""
        error_lines = [line for line in error.splitlines() if line.strip().startswith("E ")]
        return "\n".join(error_lines).strip() or error.strip()
    except Exception as e:
        return f"[Error extracting error block: {e}]"

def zip_report_folder(report_path: str, output_zip: str = "report.zip") -> str:
    """Zips the given report folder into a zip file."""
    if not os.path.exists(report_path):
        raise FileNotFoundError(f"Report path does not exist: {report_path}")

    zip_path = shutil.make_archive(base_name=output_zip.replace('.zip', ''), format='zip', root_dir=report_path)
    return zip_path

def load_email_env(filepath="emailenv"):
    if not os.path.exists(filepath):
        raise FileNotFoundError("emailenv file not found!")

    config = {}
    with open(filepath, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                config[key.strip()] = value.strip()
    return config


def is_main_worker():
    return os.environ.get("PYTEST_XDIST_WORKER") in (None, "gw0")

def get_python_version():
    try:
        return platform.python_version()
    except Exception:
        return "NA"