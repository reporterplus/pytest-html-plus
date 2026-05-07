# Contributing to pytest-html-plus

Thanks for your interest in contributing! This guide covers everything you need to go from zero to a passing PR — without leaving this file.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Linting and Formatting](#linting-and-formatting)
- [Making Changes](#making-changes)
- [Submitting a PR](#submitting-a-pr)
- [Changelog](#changelog)
- [Versioning](#versioning)
- [Questions](#questions)

---

## Getting Started

### Option A — Local (recommended for most contributions)

Prerequisites: Python ≥ 3.10, [Poetry](https://python-poetry.org/docs/#installation).

```bash
git clone https://github.com/reporterplus/pytest-html-plus.git
cd pytest-html-plus

# Install all dependencies (including dev tools)
poetry install --with dev

# Verify the install worked
make test
```

Expected output on a clean install:

```
========================= X passed in Y.Zs ==========================
```

### Option B — Docker (if you prefer an isolated environment)

Prerequisites: Docker.

```bash
git clone https://github.com/reporterplus/pytest-html-plus.git
cd pytest-html-plus

# Build the dev image (only needed once, or after pyproject.toml changes)
make build

# Drop into a shell inside the container
make shell
```

From inside the container shell, all the same `make` commands work.

---

## Running Tests

### Unit tests (fast, no browser needed)

```bash
make test
```

### Run a single test file

```bash
poetry run pytest tests/unit/{{your-test-file}}.py
```

### Run a single test by name

```bash
poetry run pytest tests/unit -k "{{your-test-name}}"
```

### Run with xdist (parallel)

```bash
make test-with-xdist
```

### What the test output should look like

A clean run prints a summary at the end:

```
========================= X passed in Y.Zs ==========================
```

If you see import errors on first run, make sure you ran `poetry install --with dev` first.

---

## Linting and Formatting

We use [ruff](https://docs.astral.sh/ruff/) for linting and formatting.

```bash
make lint    # check for issues
make fix     # auto-fix and format
```

### Pre-commit hooks (optional but recommended)

```bash
make install-formatter
```

After this, lint runs automatically on every `git commit`.

---

## Making Changes

1. **Fork** the repo and create a branch off `main`:

   ```bash
   git checkout -b your-feature-name
   ```

2. **Write your code.** Keep changes focused — one concern per PR makes review faster.

3. **Add or update tests** in `tests/unit/` for any logic you changed. We aim to keep coverage above 80%.

4. **Run the test suite** and confirm everything passes:

   ```bash
   make test
   ```

5. **Run lint** and fix any issues:

   ```bash
   make fix
   ```

6. **Update the docs** in `docs/` or `README.md` if your change affects user-facing behaviour.

7. **Add a CHANGELOG entry** under `[Unreleased]` in `CHANGELOG.md`:

   ```markdown
   ## [Unreleased]

   ### Added
   - Brief description of what you added (#PR number)
   ```

---

## Submitting a PR

- **Target branch:** `main`
- Title should be clear and imperative: `Fix screenshot not attached when using xdist`, not `fixes`
- Link the related issue with `Closes #123` in the PR description

### PR checklist

Before marking as Ready for Review:

- [ ] `make test` passes
- [ ] `make lint` passes
- [ ] Tests added or updated for changed behaviour
- [ ] README / docs updated if user-facing behaviour changed
- [ ] Changelog entry added under `[Unreleased]` in `CHANGELOG.md`
- [ ] PR description explains what changed and why
- [ ] Issue linked with `Closes #123` (if applicable)

---

## Changelog

We follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). Every PR that changes behaviour, fixes a bug, or adds a feature should include an entry in `CHANGELOG.md` under `[Unreleased]`.

Use these section headings:

| Section | When to use |
|---|---|
| `Added` | New features or flags |
| `Changed` | Behaviour changes to existing features |
| `Fixed` | Bug fixes |
| `Deprecated` | Features being phased out |
| `Removed` | Removed features |
| `Security` | Security fixes |
| `Maintenance` | Dependency bumps, CI changes, refactors with no user impact |

Example:

```markdown
## [Unreleased]

### Fixed
- Screenshot not attached to report when test name contains special characters (#142)
```

---

## Versioning

We follow [Semantic Versioning](https://semver.org/):

| Type | Example | When |
|---|---|---|
| `PATCH` | `1.0.1` | Bug fixes, docs, performance, dependency bumps |
| `MINOR` | `1.1.0` | New features, backwards-compatible |
| `MAJOR` | `2.0.0` | Breaking changes |

Maintainers handle version bumps and releases — you don't need to change the version number in your PR.

---

## Questions?

- Open an [Issue](https://github.com/reporterplus/pytest-html-plus/issues) for bugs or feature ideas
- Start a [Discussion](https://github.com/reporterplus/pytest-html-plus/discussions) for questions or design ideas
