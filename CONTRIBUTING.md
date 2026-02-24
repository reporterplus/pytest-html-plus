# Contributing

We welcome PRs, issues, and feature suggestions. For full details, see the 
[Contributing Guide](https://pytest-html-plus.readthedocs.io/en/latest/contributing.html).

---

## Quick Start
```bash
make build-dev   # build the dev container
make test        # run the test suite
make lint        # check for lint errors
make fix         # auto-fix lint issues
```

## Branching

All PRs must target the **next upcoming version branch**, not `main`.

- Current release is `0.4.0`? → target `0.4.1`
- Can't find the branch? → open an issue asking us to create it

## Semantic Versioning

| Type | Example | When |
|------|---------|------|
| `PATCH` | `0.4.1` | fixes, docs, perf |
| `MINOR` | `0.5.0` | new features, backwards-compatible |
| `MAJOR` | `1.0.0` | breaking changes |

## PR Checklist

- [ ] Targeting the correct upcoming version branch
- [ ] `make lint` passes
- [ ] `make test` passes
- [ ] Tests added or updated for changed behavior
- [ ] README / docs updated if user-facing behavior changed
- [ ] Changelog entry added under the upcoming version
- [ ] PR description explains what changed and why
- [ ] Linked related issue with `Closes #123`

## Questions?

Open an issue or start a [Discussion](https://github.com/reporterplus/pytest-html-plus/discussions).