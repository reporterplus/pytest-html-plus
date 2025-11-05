import os
import threading
import subprocess
from typing import Tuple, Optional

_CACHE_LOCK = threading.Lock()
_CACHED_REPO_INFO: Optional[Tuple[str, str]] = None

# Env vars we treat as authoritative when present (CI) — cheap checks
_CI_BRANCH_VARS = [
    "GITHUB_HEAD_REF", "GITHUB_REF_NAME",
    "CI_COMMIT_REF_NAME", "BITBUCKET_BRANCH",
    "BUILD_SOURCEBRANCHNAME", "CIRCLE_BRANCH",
    "BRANCH_NAME", "TRAVIS_BRANCH", "GIT_BRANCH"
]
_CI_COMMIT_VARS = [
    "GITHUB_SHA", "CI_COMMIT_SHA", "BITBUCKET_COMMIT",
    "BUILD_SOURCEVERSION", "CIRCLE_SHA1", "TRAVIS_COMMIT"
]

def _run_git(cmd: list, timeout: float = 1.0) -> Optional[str]:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=timeout)
        return out.decode().strip()
    except Exception:
        return None

def get_repo_info() -> Tuple[str, str]:
    """
    Return (branch, commit_sha).
    - Branch is a readable branch name or "NA".
    - Commit is full SHA or "NA".
    Behavior:
      1) If REPORTER_BRANCH / REPORTER_COMMIT provided -> use them (manual override).
      2) Else read common CI env vars (cheap).
      3) Else call git once to get commit, and try to get branch (symbolic-ref / points-at).
    Result is cached per-process.
    """
    global _CACHED_REPO_INFO

    # 0) Manual overrides (explicit, highest priority) - zero cost
    manual_branch = os.getenv("REPORTER_BRANCH")
    manual_commit = os.getenv("REPORTER_COMMIT")
    if manual_branch or manual_commit:
        branch = manual_branch or "NA"
        commit = manual_commit or _run_git(["git", "rev-parse", "HEAD"]) or "NA"
        with _CACHE_LOCK:
            _CACHED_REPO_INFO = (branch, commit)
        return _CACHED_REPO_INFO

    # 1) CI envs (cheap, no subprocess)
    for var in _CI_COMMIT_VARS:
        val = os.getenv(var)
        if val:
            commit = val
            # try branch envs (if any)
            branch = next((os.getenv(bv) for bv in _CI_BRANCH_VARS if os.getenv(bv)), "NA")
            with _CACHE_LOCK:
                _CACHED_REPO_INFO = (branch, commit)
            return _CACHED_REPO_INFO

    for var in _CI_BRANCH_VARS:
        val = os.getenv(var)
        if val:
            # branch available but commit not set in CI envs -> get commit cheaply
            commit = _run_git(["git", "rev-parse", "HEAD"]) or "NA"
            with _CACHE_LOCK:
                _CACHED_REPO_INFO = (val, commit)
            return _CACHED_REPO_INFO

    # 2) Return cached if already computed
    with _CACHE_LOCK:
        if _CACHED_REPO_INFO is not None:
            return _CACHED_REPO_INFO

    # 3) Final: use git (one or two quick calls), cached afterwards
    commit = _run_git(["git", "rev-parse", "HEAD"]) or "NA"
    branch = _run_git(["git", "symbolic-ref", "--short", "-q", "HEAD"])

    # If symbolic-ref didn't return and commit is present, try local branches pointing to HEAD
    if not branch and commit != "NA":
        branches = _run_git(["git", "branch", "--points-at", "HEAD", "--format=%(refname:short)"])
        if branches:
            branch = branches.splitlines()[0].strip()

    if not branch:
        branch = "NA"

    with _CACHE_LOCK:
        _CACHED_REPO_INFO = (branch, commit)
    return _CACHED_REPO_INFO

def display_repo_ref(short_len: int = 7) -> str:
    """Return a friendly display like 'feature/foo (5bb4c87)' or '5bb4c87'."""
    branch, commit = get_repo_info()
    commit_short = commit[:short_len] if commit and commit != "NA" else "NA"
    if branch and branch != "NA":
        return f"{branch} ({commit_short})"
    return commit_short
