## PR Checklist

Before submitting, please make sure you've done the following:

**Branch**
- [ ] PR is targeting the correct upcoming version branch (e.g. `0.4.1`), not `main`

**Code**
- [ ] Ran `make lint` with no errors
- [ ] Ran `make test` and all tests pass
- [ ] Added or updated tests for any new or changed behavior

**Docs**
- [ ] Updated README if user-facing behavior changed
- [ ] Updated ReadTheDocs documentation if applicable

**Changelog**
- [ ] Added a short entry under the upcoming version in `CHANGELOG.md`

**General**
- [ ] PR description explains *what* changed and *why*
- [ ] Linked the related issue (if one exists) using `Closes #123`