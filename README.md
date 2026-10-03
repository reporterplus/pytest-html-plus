⚡ **Test your code, not your reporting setup.**

> A pytest report built for fast debugging, with parallel execution support, automatic screenshots, and shareable failure context.

`pytest-html-plus` turns pytest results into portable debugging artifacts for CI, collaboration, and integrations, without a reporting platform.

➡️ [View Demo Report](https://reporterplus.github.io/pytest-html-plus/)

[![Docs](https://img.shields.io/badge/docs-online-blue)](https://pytest-html-plus.readthedocs.io/en/main/) [![PyPI Downloads](https://img.shields.io/pypi/dm/pytest-html-plus?label=downloads%2Fmonth)](https://pypistats.org/packages/pytest-html-plus) ![PyPI](https://img.shields.io/pypi/v/pytest-html-plus) ![Python Versions](https://img.shields.io/pypi/pyversions/pytest-html-plus) ![License](https://img.shields.io/pypi/l/pytest-html-plus) [![Unit Tests](https://github.com/reporterplus/pytest-html-plus/actions/workflows/unit-test.yml/badge.svg)](https://github.com/reporterplus/pytest-html-plus/actions/workflows/unit-test.yml) [![codecov](https://codecov.io/gh/reporterplus/pytest-html-plus/branch/main/graph/badge.svg)](https://codecov.io/gh/reporterplus/pytest-html-plus) [![GitHub Action](https://img.shields.io/badge/GitHub_Action-Pytest_HTML_Plus-2088FF?logo=githubactions&logoColor=white)](https://github.com/marketplace/actions/pytest-html-plus-action) [![VS Code](https://img.shields.io/badge/VS_Code-Pytest_HTML_Plus-007ACC?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=reporterplus.pytest-html-plus-vscode)

---

## 🚀 Quick Start

```bash
pip install pytest-html-plus
# or
poetry add pytest-html-plus

pytest
```

By default, that generates a portable HTML report and structured JSON output. No hooks, decorators, or reporting server are required.

## Why pytest-html-plus?

- ⚡ Produce one unified report with or without `pytest-xdist`.
- 📸 Capture failure screenshots automatically for Selenium and Playwright tests.
- 📋 Keep errors, traces, logs, stdout, and stderr together in one report.
- 🔄 Understand flaky tests with complete retry history.
- 🔗 Share a direct link to an individual test result.
- 🔍 Find tests, failures, traces, issue references, and documentation links from the same report.

## ✨ Features

#### ⚡ One Unified Report with xdist

Run tests in parallel and receive one merged HTML and JSON report without an additional merge plugin or post-processing step.

#### 📸 See What Failed Automatically

Capture Selenium and Playwright screenshots automatically and view them alongside the relevant failure context, with no custom hooks or decorators required.

#### 📋 Everything You Need to Investigate a Failure

Review errors, traces, logs, stdout, stderr, and screenshots together. Copy the context you need in one click and use `--plus-output=failed-only` to keep passing-test output compact.

![Configurable output capture](https://github.com/user-attachments/assets/209cd2c0-d33b-48ec-b58b-8c8991ce35be)

![Copy failure context](https://github.com/user-attachments/assets/396e8cf6-862b-4619-82bf-81a8eae8e7b6)

#### 🔄 Understand Flaky Tests Across Every Retry

See how a test behaves across retries, from initial failure to recovery. Spot patterns such as cache issues, race conditions, and intermittent crashes without guesswork.

![Flaky test retry history](https://github.com/user-attachments/assets/1f7e0cd8-d2f9-47fd-8909-6f12adf8a800)

#### 🔗 Share Any Test with a Direct Link

Copy a direct link to any test result and share it with your team. The report opens at the linked test, reveals it, expands its details, and highlights it, so teammates can jump straight to the relevant context without searching through the report.

<img width="3024" height="1778" alt="ScreenRecording2026-10-03at8 55 26AM-ezgif com-cut" src="https://github.com/user-attachments/assets/0c44a38f-7898-4a4d-8241-4f1d1c57ccfb" />

#### 🔍 Find the Context You Need

Search tests, errors, traces, issue references, documentation links, and custom references from the same report.

<img width="800" height="421" alt="Universal test search" src="https://github.com/user-attachments/assets/54858747-ab16-4d4f-baa9-0d651a1d8bac" />

---

## Try It Without Changing Your Test Suite

`pytest-html-plus` works alongside existing pytest tooling, so you can evaluate it with your current test suite without adopting a reporting server, rewriting tests, or maintaining reporting infrastructure.

## More Built In

Also includes merged JUnit XML export, run metadata, slow-test visibility, reusable profiles, traceability helpers, email delivery, dynamic markers, and configurable output capture.

**[See all features and configuration options →](https://pytest-html-plus.readthedocs.io/en/main/)**

## Project Status

pytest-html-plus is stable and actively maintained, with its core reporting experience now well established. Future development will focus on compatibility, reliability, and carefully selected improvements that strengthen the core reporting experience.

We're also looking for co-maintainers to help review pull requests, triage issues, and keep the project healthy across future Python and pytest releases.

If you're interested in becoming a long-term contributor, we'd love to hear from you. Please open an issue or start a discussion.

## Contributing

We welcome pull requests, issues, and feature suggestions from the community.

See the [contribution guide](CONTRIBUTING.md) for setup instructions.

## 📜 License

MIT
