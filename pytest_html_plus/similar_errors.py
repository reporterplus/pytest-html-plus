"""Conservative, linear-time matching of final errors in a consolidated report."""

import re
from collections import defaultdict

_ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
_EXCEPTION = re.compile(r"^([\w.]*(?:Error|Exception|Failure)):\s*(.*)$")
_ADDRESS = re.compile(r"(\bobject at )0x[0-9a-fA-F]+\b")


def error_fingerprint(error):
    """Keep exception identity and message; never hash a traceback or type alone."""
    if not isinstance(error, str):
        return None
    lines = [
        re.sub(r"^E\s+", "", line.strip()) for line in _ANSI.sub("", error).splitlines()
    ]
    for index, line in enumerate(lines):
        match = _EXCEPTION.match(line)
        if not match:
            continue
        kind, message = match.groups()
        # Preserve multiline message differences, stopping at diagnostic sections.
        continuation = []
        for following in lines[index + 1 :]:
            if following.startswith(
                ("Call log:", "Traceback ", "During handling", "The above exception")
            ):
                break
            continuation.append(following)
        message = "\n".join([message, *continuation]).strip()
        # Preserve paths: worker directories and filenames may be meaningful.
        message = " ".join(_ADDRESS.sub(r"\1<address>", message).split())
        if len(re.findall(r"[A-Za-z]{2,}", message)) < 2:
            return None
        if kind.rsplit(".", 1)[-1] == "TimeoutError" and message.casefold().rstrip(
            "."
        ) in {
            "timed out",
            "operation timed out",
            "timeout exceeded",
        }:
            return None
        if message in {"assert False", "assert True", "assert 0", "assert 1"}:
            return None
        return kind, message
    return None


def annotate_similar_errors(report):
    """Annotate consolidated results in place, storing membership only once.

    Call only when enabled. Distinct nodeids are test identities; attempts and
    traces are deliberately not inspected. Can also be used by JSON-only callers.
    """
    groups = defaultdict(dict)
    for test in report["results"]:
        test.pop("similar_error_group", None)
        if test.get("status") not in {"failed", "error"} or not test.get("nodeid"):
            continue
        fingerprint = error_fingerprint(test.get("error"))
        if fingerprint:
            groups[fingerprint][test["nodeid"]] = test
    metadata = {}
    for fingerprint, members in groups.items():
        if len(members) < 2:
            continue
        group_id = f"similar-{len(metadata) + 1}"
        metadata[group_id] = {"message": fingerprint[1], "nodeids": list(members)}
        for test in members.values():
            test["similar_error_group"] = group_id
    report["similar_error_groups"] = metadata
