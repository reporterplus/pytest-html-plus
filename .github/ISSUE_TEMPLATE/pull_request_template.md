## PR Checklist

Before submitting, please make sure you've done the following:

**Branch**
- [ ] PR is targeting `main`

**Code**
- [ ] Ran `poetry run ruff check .` with no errors
- [ ] Ran `poetry run pytest tests/unit` and all tests pass
- [ ] Added or updated tests for any new or changed behavior

**Docs**
- [ ] Updated README if user-facing behavior changed
- [ ] Updated docs in `docs/` if applicable

**Changelog**
- [ ] Added a short entry under `[Unreleased]` in `CHANGELOG.md`

**General**
- [ ] PR description explains *what* changed and *why*
- [ ] Linked the related issue (if one exists) using `Closes #123`