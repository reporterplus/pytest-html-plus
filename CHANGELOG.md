# Changelog

All notable changes to `pytest-html-plus` are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

_Changes merged to `main` but not yet released._

---

## [1.1.0] — 2026-06-10

### Added

* Universal search now indexes error messages and trace snippets in addition to test names and linked references.
* Users can quickly locate related failures by searching for exception names, assertion text, or custom error messages.

### Changed

* Updated README and documentation examples for universal search and traceability.

### Fixed

* Addressed security and reliability issues identified by CodeQL analysis.
* Improved report generation robustness and resolved minor quality issues highlighted during static analysis.

### Maintenance

* Bumped version to `1.1.0` in `pyproject.toml` and `docs/conf.py`.


## [1.0.1] — 2026-05-07

### Changed
- Merged `pytest-html` and Allure comparison tables into a single three-way table in `README.md`, placed early for maximum visibility. Removed the redundant `vs Allure` section at the bottom.
- `CONTRIBUTING.md` now references `make` targets throughout instead of duplicating raw `poetry run` commands. Ad-hoc commands (single file, single test by name) use a `{{placeholder}}` template pattern.

### Fixed
- `test-with-xdist` Makefile target had a double `poetry run` that caused it to fail.
- `clean` Makefile target referenced an undefined `$(REPORTS_DIR)` variable.
- `install-formatter` Makefile target used bare `pip install pre-commit` instead of `poetry run pre-commit install`.

### Added
- `dist` Makefile target (`poetry build`) for building the distribution package.
- GitHub Actions publish workflow (`publish.yml`) — manually triggered via `workflow_dispatch`, builds with `make dist`, and publishes to PyPI using Twine with `TWINE_PASSWORD` secret.

### Maintenance
- Bumped version to `1.0.1` in `pyproject.toml` and `docs/conf.py`.

---

## [1.0.0] — 2026-04-12

### Added
- **Reusable configuration profiles** — define named profiles (e.g. `ci`, `ci-warnings`) in `pyproject.toml` under `[tool.pytest-html-plus.profiles.*]` and activate them with `--profile=<name>`. Eliminates the need to repeat flags across CI jobs.

### Changed
- Marked as Production/Stable (`Development Status :: 5 - Production/Stable`) in PyPI classifiers.

---

## [0.5.2] — 2026-04-04

### Fixed
- Multiple code quality improvements across the codebase (unused variables, import cleanup, lint violations).
- Applied Copilot Autofix suggestion to `json_merge.py`.

### Maintenance
- Updated CI workflows for Windows and Linux unit tests.
- Bumped `requests`, `black`, and `cryptography` dependencies.

---

## [0.5.1] — 2026-03-29

### Fixed
- Tech debt: resolved all outstanding lint issues flagged by ruff.

### Maintenance
- OSS best practices: standardised GitHub Actions workflow structure.
- Updated ReadTheDocs documentation.

---

## [0.5.0] — 2026-02-06

### Added
- **VSCode Extension** — `pytest-html-plus-vscode` published to the VS Code Marketplace. Run tests and view rich HTML reports directly inside VS Code.

---

## [0.4.9] — 2026-01-16

### Fixed
- Reverted v0.4.8 regression; re-applied stable fix.

---

## [0.4.7] — 2026-01-04

### Maintenance
- Dependency and compatibility updates.

---

## [0.4.6] — 2025-12-29

### Maintenance
- Dependency and compatibility updates.

---

## [0.4.5] — 2025-12-03

### Added
- Documented and improved automatic screenshot attachment flow — screenshots are now captured and embedded without any hook code.

---

## [0.4.4] — 2025-11-22

### Maintenance
- Stability and dependency updates.

---

## [0.4.3] — 2025-11-12

### Maintenance
- Stability and dependency updates.

---

## [0.4.2] — 2025-10-30

### Maintenance
- Documentation and version metadata updates.

---

## [0.4.1] — 2025-09-18

### Added
- Full usage documentation published to ReadTheDocs.

---

## [0.4.0] — 2025-08-23

### Added
- **GitHub Actions Marketplace** — `pytest-html-plus-action` published. Generate rich reports in CI without manually managing dependencies.

---

## [0.3.9] — 2025-08-15

### Maintenance
- Documentation updates and link fixes.

---

## [0.3.7] — 2025-07-27

### Added
- ReadTheDocs documentation site set up at `pytest-html-plus.readthedocs.io`.

### Fixed
- Screenshot filename mismatch — screenshots were not being attached to the correct test in the report when test names differed from screenshot filenames (#121).
- Screenshot not attached when sending reports via email.

---

## [0.3.4] — 2025-07-16

### Changed
- **Package renamed** to `pytest-html-plus` (previously published under a different name). Update your `pip install` command accordingly.

---

## [0.3.3] — 2025-07-12

### Fixed
- Email report screenshots attachment bug.

---

## [0.3.2] — 2025-07-09

### Maintenance
- Stability improvements.

---

## [0.3.1] — 2025-07-07

### Added
- **Unlinked test detection** — filter and highlight tests that have no associated issue or documentation link.
- **Auto-driver detection** — Selenium/Playwright driver properties are detected automatically; no need to pass the automation tool name manually.
- Error messages now highlighted in red within the report cell for faster scanning.
- Responsive screenshot alignment with fixed dimensions.
- `OPEN_REPORT` environment variable — automatically open the HTML report after a test run.

---

## [0.2.9] — 2025-06-21

### Added
- **Universal test search** — filter tests in real time by test name, linked issue ID, or any URL keyword.
- Flaky test filter — show only flaky tests with one click.

---

## [0.2.8] — 2025-06-18

### Changed
- Removed `--verbose` dependency; package footprint reduced.

---

## [0.2.7] — 2025-06-18

### Added
- Report layout alignment — all metadata and result columns consistently aligned.

---

## [0.2.6] — 2025-06-12

### Added
- Code coverage reporting integrated with Codecov; coverage badge added to README.
- `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` added.

---

## [0.2.5] — 2025-06-06

### Added
- Expanded unit test suite with broader coverage.

---

## [0.2.3] — 2025-06-05

### Added
- **Dynamic markers** — tag tests at runtime using standard `pytest.mark.*` (e.g. `api`, `critical`, `slow`) without predefining markers. Tags are rendered and filterable in the report.
- **Traceability links** — attach Jira, Testmo, Notion, or any URL to a test; links are rendered in the report and searchable.

---

## [0.2.1] — 2025-06-04

### Added
- **Slow test highlighting** — the slowest tests in a run are automatically identified and flagged.
- **Copy-to-clipboard** — copy test path, logs, traces, and errors with a single click for fast sharing.
- **Run metadata** — branch, commit SHA, environment, and custom metadata embedded in report header.

---

## [0.1.x] — 2025-05 (initial releases)

### Added
- Single-file self-contained HTML report generated from pytest JSON output.
- **Flaky test detection** — tests that fail then pass on retry are marked as flaky with full retry history.
- **Screenshot support** — Selenium and Playwright screenshots automatically captured and embedded; no conftest hooks required.
- **Email reports** — send reports via SendGrid integration using `--send-email`.
- **xdist support** — parallel test runs with `pytest-xdist` produce a single merged report.
- Comprehensive log capture — `print()`, logger output, stdout/stderr all embedded per test.
- **JUnit XML export** — merged XML output compatible with TestRail, Xray, and Zephyr; one flag, no extra plugins.

---

[Unreleased]: https://github.com/reporterplus/pytest-html-plus/compare/v1.0.1...HEAD
[1.0.0]: https://github.com/reporterplus/pytest-html-plus/compare/v0.5.2...v1.0.0
[0.5.2]: https://github.com/reporterplus/pytest-html-plus/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/reporterplus/pytest-html-plus/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/reporterplus/pytest-html-plus/compare/v0.4.9...v0.5.0
[0.4.9]: https://github.com/reporterplus/pytest-html-plus/compare/v0.4.7...v0.4.9
[0.4.7]: https://github.com/reporterplus/pytest-html-plus/compare/v0.4.6...v0.4.7
[0.4.6]: https://github.com/reporterplus/pytest-html-plus/compare/v0.4.5...v0.4.6
[0.4.5]: https://github.com/reporterplus/pytest-html-plus/compare/v0.4.4...v0.4.5
[0.4.4]: https://github.com/reporterplus/pytest-html-plus/compare/v0.4.3...v0.4.4
[0.4.3]: https://github.com/reporterplus/pytest-html-plus/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/reporterplus/pytest-html-plus/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/reporterplus/pytest-html-plus/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/reporterplus/pytest-html-plus/compare/v0.3.9...v0.4.0
[0.3.9]: https://github.com/reporterplus/pytest-html-plus/compare/v0.3.7...v0.3.9
[0.3.7]: https://github.com/reporterplus/pytest-html-plus/compare/v0.3.4...v0.3.7
[0.3.4]: https://github.com/reporterplus/pytest-html-plus/compare/v0.3.3...v0.3.4
[0.3.3]: https://github.com/reporterplus/pytest-html-plus/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/reporterplus/pytest-html-plus/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/reporterplus/pytest-html-plus/compare/v0.2.9...v0.3.1
[0.2.9]: https://github.com/reporterplus/pytest-html-plus/compare/v0.2.8...v0.2.9
[0.2.8]: https://github.com/reporterplus/pytest-html-plus/compare/v0.2.7...v0.2.8
[0.2.7]: https://github.com/reporterplus/pytest-html-plus/compare/v0.2.6...v0.2.7
[0.2.6]: https://github.com/reporterplus/pytest-html-plus/compare/v0.2.5...v0.2.6
[0.2.5]: https://github.com/reporterplus/pytest-html-plus/compare/v0.2.3...v0.2.5
[0.2.3]: https://github.com/reporterplus/pytest-html-plus/compare/v0.2.1...v0.2.3
[0.2.1]: https://github.com/reporterplus/pytest-html-plus/releases/tag/v0.2.1
