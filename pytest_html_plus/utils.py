from importlib.metadata import files
import os
from pathlib import Path
import platform
import shutil

import yaml



def get_env_marker(config):
    for arg in ("--env", "--environment"):
        if config.getoption(arg.lstrip("-").replace("-", "_"), default=None):
            return config.getoption(arg.lstrip("-").replace("-", "_"))
    return "Pass --rp-env to populate environment"


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
        error_lines = [
            line for line in error.splitlines() if line.strip().startswith("E ")
        ]
        return "\n".join(error_lines).strip() or error.strip()
    except Exception as e:
        return f"[Error extracting error block: {e}]"


def zip_report_folder(report_path: str, output_zip: str = "report.zip") -> str:
    """Zips the given report folder into a zip file."""
    if not os.path.exists(report_path):
        raise FileNotFoundError(f"Report path does not exist: {report_path}")

    zip_path = shutil.make_archive(
        base_name=output_zip.replace(".zip", ""), format="zip", root_dir=report_path
    )
    return zip_path


def load_email_env(filepath="emailenv"):
    if not os.path.exists(filepath):
        raise FileNotFoundError("emailenv file not found!")

    config = {}
    with open(filepath) as f:
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
    
def to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() == "true"
    return False

def extract_errors_from_attempts(t):
    errors = set()

    for attempt in t.get("attempts", []):
        if not attempt:
            continue

        err = attempt.get("error")
        if err:
            cleaned = extract_error_block(err)
            first_line = cleaned.splitlines()[0].replace("E ", "").strip()
            errors.add(first_line)

    if not errors:
        first_failure = t.get("first_failure") or {}
        raw_error = t.get("error") or first_failure.get("error")

        if raw_error:
            cleaned = extract_error_block(raw_error)
            first_line = cleaned.splitlines()[0].replace("E ", "").strip()
            errors.add(first_line)

    return list(errors)


def validate_rules(config):
    assert "rules" in config, "Missing rules section"

    for rule in config["rules"]:
        assert "type" in rule, "Rule missing 'type'"
        assert "priority" in rule, "Rule missing 'priority'"
        assert "match" in rule, "Rule missing 'match'"


def load_error_rules():
    override_path = os.getenv("REPORTERPLUS_RULES_PATH")

    try:
        if override_path and Path(override_path).exists():
            with open(override_path) as f:
                config = yaml.safe_load(f)
        else:
            # 👇 resolve relative to current file
            base_path = Path(__file__).resolve().parent
            path = base_path / "config" / "error_rules.yaml"

            with open(path) as f:
                config = yaml.safe_load(f)

        validate_rules(config)
        return config

    except yaml.YAMLError as e:
        raise RuntimeError(f"Invalid error_rules.yaml: {e}")
    

def extract_message(error: str | None) -> str | None:
    if not error:
        return None

    msg = error.split("\n")[0].strip()

    # remove pytest prefixes like "E", "F", etc.
    if msg and msg[0] in {"E", "F"}:
        msg = msg[1:].strip()

    return msg or None

CONFIG = load_error_rules()
RULES = sorted(CONFIG["rules"], key=lambda r: r["priority"])
FALLBACK = CONFIG.get("defaults", {}).get("fallback_type", "other")


def get_type_hint(message: str | None) -> str:
    if not message:
        return FALLBACK

    msg = message.lower()

    for rule in RULES:
        if any(pattern in msg for pattern in rule["match"]):
            return rule["type"]

    return FALLBACK

import re

def generate_signature(message: str, type_hint: str) -> str:
    msg = message.lower()

    # remove numbers (timeouts, IDs, etc.)
    msg = re.sub(r"\d+", "", msg)

    # remove special characters
    msg = re.sub(r"[^a-z\s]", "", msg)

    # collapse whitespace
    msg = re.sub(r"\s+", " ", msg).strip()

    # take first few meaningful words
    words = msg.split()[:3]

    base = "_".join(words) if words else "unknown"

    return f"{type_hint}_{base}"

def get_type_hint(message: str | None) -> str:
    config = CONFIG
    error_rules = config["rules"]
    if not message:
        return "unknown"

    msg = message.lower()

    for rule in error_rules:
        for pattern in rule["match"]:
            if pattern in msg:
                return rule["type"]

    return "other"


def build_error_meta(test: dict) -> dict | None:
    error = test.get("error")
    if not error:
        return None

    message = extract_message(error)
    if not message:
        return None

    type_hint = get_type_hint(message)
    signature = generate_signature(message, type_hint)

    return {
        "message": message,
        "type_hint": type_hint,
        "signature": signature,
    }