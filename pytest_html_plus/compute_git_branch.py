import os
import threading
import subprocess
from typing import Optional

_cache_lock = threading.Lock()
_cached_git_branch: Optional[str] = None

def _read_file(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return None

def _branch_from_dotgit(dotgit_path: str) -> Optional[str]:
    """
    Try to read .git/HEAD and resolve a branch name without calling subprocess.
    Handles:
      - normal HEAD -> "ref: refs/heads/<branch>"
      - detached HEAD (sha1) -> return "DETACHED" or None
      - packed-refs resolution when needed
    """
    head_path = os.path.join(dotgit_path, "HEAD")
    head = _read_file(head_path)
    if not head:
        return None

    # Standard case: "ref: refs/heads/<branch>"
    if head.startswith("ref:"):
        ref = head.split(":", 1)[1].strip()
        # try to read the ref file
        ref_path = os.path.join(dotgit_path, *ref.split("/"))
        val = _read_file(ref_path)
        if val:
            return val if len(val) == 40 else val  # sometimes refs store an annotated string; we return as-is

        # If the ref file doesn't exist, try packed-refs
        packed = _read_file(os.path.join(dotgit_path, "packed-refs"))
        if packed:
            # packed-refs lines are: "<sha> <ref>"
            for line in packed.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if " " in line:
                    sha, refname = line.split(" ", 1)
                    if refname.strip() == ref:
                        return sha.strip()
        return None

    # Detached HEAD (contains a commit sha)
    if len(head) >= 7 and all(c in "0123456789abcdefABCDEF" for c in head[:7]):
        return head  # return sha or indicate detached
    return None

def compute_git_branch() -> str:
    """Get git branch fast: env vars -> cached -> .git files -> subprocess -> 'NA'."""
    global _cached_git_branch

    # 1) Check common CI/env override vars (very cheap)
    branch_env_vars = [
        "GITHUB_HEAD_REF", "GITHUB_REF_NAME",
        "CI_COMMIT_REF_NAME", "BITBUCKET_BRANCH",
        "BUILD_SOURCEBRANCHNAME", "CIRCLE_BRANCH",
        "BRANCH_NAME", "TRAVIS_BRANCH", "GIT_BRANCH"
    ]
    for var in branch_env_vars:
        val = os.getenv(var)
        if val:
            return val

    with _cache_lock:
        if _cached_git_branch is not None:
            return _cached_git_branch

    try:
        cwd = os.getcwd()
        dotgit_path = os.path.join(cwd, ".git")
        if os.path.exists(dotgit_path):
            # If .git is a file (git worktree/submodule), it contains "gitdir: /path/to/actual/git"
            if os.path.isfile(dotgit_path):
                content = _read_file(dotgit_path)
                if content and content.startswith("gitdir:"):
                    gitdir = content.split(":", 1)[1].strip()
                    if not os.path.isabs(gitdir):
                        gitdir = os.path.normpath(os.path.join(cwd, gitdir))
                    branch = _branch_from_dotgit(gitdir)
                else:
                    branch = None
            else:
                branch = _branch_from_dotgit(dotgit_path)

            if branch:
                with _cache_lock:
                    _cached_git_branch = branch
                return branch
    except Exception:
        pass

    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL,
            timeout=2  # don't let this hang
        )
        branch = out.decode().strip()
        with _cache_lock:
            _cached_git_branch = branch
        return branch
    except Exception:
        with _cache_lock:
            _cached_git_branch = "NA"
        return "NA"
