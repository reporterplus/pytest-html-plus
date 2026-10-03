⚡ **Test your code, not your reporting setup.**

> Get a rich, actionable pytest report in under three seconds. Install, run your tests, and start investigating—no reporting setup required.

`pytest-html-plus` generates a portable, easy-to-read HTML report with automatic screenshots, captured failure context, flaky-test history, direct test links, and built-in `xdist` support.

➡️ [View Demo Report](https://reporterplus.github.io/pytest-html-plus/)

[![Docs](https://img.shields.io/badge/docs-online-blue)](https://pytest-html-plus.readthedocs.io/en/main/) [![PyPI Downloads](https://static.pepy.tech/badge/pytest-html-plus)](https://pepy.tech/projects/pytest-html-plus) ![PyPI](https://img.shields.io/pypi/v/pytest-html-plus) ![Python Versions](https://img.shields.io/pypi/pyversions/pytest-html-plus) ![License](https://img.shields.io/pypi/l/pytest-html-plus) [![Unit Tests](https://github.com/reporterplus/pytest-html-plus/actions/workflows/unit-test.yml/badge.svg)](https://github.com/reporterplus/pytest-html-plus/actions/workflows/unit-test.yml) [![codecov](https://codecov.io/gh/reporterplus/pytest-html-plus/branch/main/graph/badge.svg)](https://codecov.io/gh/reporterplus/pytest-html-plus)

---

## 🚀 Quick Start

```bash
pip install pytest-html-plus
# or
poetry add pytest-html-plus

pytest
```

That is enough to generate an HTML report and structured JSON output. No hooks, decorators, or reporting server are required.

## Why pytest-html-plus?

- 📸 Capture failure screenshots automatically for Selenium and Playwright tests.
- 📋 Keep errors, traces, logs, stdout, and stderr together in one report.
- 🔄 Understand flaky tests with complete retry history.
- 🔗 Share a direct link to an individual test result.
- 🔍 Search across test names, failures, traces, and linked references.
- ⚡ Produce one unified report with or without `pytest-xdist`.
- 🏷️ Connect tests to Jira, Testmo, documentation, and custom references.
- 🧩 Export merged JUnit XML for test-management tools with one flag.

---

## Use pytest-html-plus Wherever You Work

### GitHub Actions

Generate reports in CI, upload report artifacts, and publish test summaries without maintaining custom reporting scripts.

[![🚀 View on GitHub Marketplace](https://img.shields.io/badge/Marketplace-Pytest%20HTML%20Plus-blue?logo=github)](https://github.com/marketplace/actions/pytest-html-plus-action)
[![Documentation](https://img.shields.io/badge/docs-readthedocs.io-brightgreen)](https://pytest-html-plus.readthedocs.io/en/main/marketplace/usage.html)

### VS Code

Browse test results, inspect failures, and jump directly to source code from the VS Code sidebar.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/reporterplus.pytest-html-plus-vscode?label=VS%20Code%20Marketplace&logo=visualstudiocode&logoColor=white&color=0078d7)](https://marketplace.visualstudio.com/items?itemName=reporterplus.pytest-html-plus-vscode)
[![Installs](https://img.shields.io/visual-studio-marketplace/i/reporterplus.pytest-html-plus-vscode)](https://marketplace.visualstudio.com/items?itemName=reporterplus.pytest-html-plus-vscode)
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://pytest-html-plus.readthedocs.io/en/main/extensions/vscode/usage.html)

## ✨ Features

#### 📸 See What Failed—Automatically

Capture Selenium and Playwright screenshots automatically and view them alongside the relevant failure context—no custom hooks or decorators required.

#### 📋 Everything You Need to Investigate a Failure

Review errors, traces, logs, stdout, stderr, and screenshots together. Copy the context you need in one click and use `--plus-output=failed-only` to keep passing-test output compact.

![Copy failure context](https://github.com/user-attachments/assets/396e8cf6-862b-4619-82bf-81a8eae8e7b6)

![Configurable output capture](https://github.com/user-attachments/assets/209cd2c0-d33b-48ec-b58b-8c8991ce35be)

#### 🔄 Understand Flaky Tests Across Every Retry

See how a test behaves across retries—from initial failure to recovery. Spot patterns such as cache issues, race conditions, and intermittent crashes without guesswork.

![Flaky test retry history](https://github.com/user-attachments/assets/1f7e0cd8-d2f9-47fd-8909-6f12adf8a800)

#### 🔗 Share Any Test with a Direct Link

Copy a direct link to any test result and share it with your team. The report opens at the linked test, reveals it, expands its details, and highlights it—so teammates can jump straight to the relevant context without searching through the report.

#### 🔍 Find Any Test or Failure Instantly

Search in real time by:

- Test name
- Linked issue or documentation ID
- Custom URL or reference keyword
- Error message or trace snippet

<img width="800" height="421" alt="Universal test search" src="https://github.com/user-attachments/assets/54858747-ab16-4d4f-baa9-0d651a1d8bac" />

#### 🏷️ Connect Tests to Requirements, Issues, and Releases

Add dynamic markers such as `api`, `critical`, or `slow`, link tests to Jira, Testmo, Notion, or documentation, and quickly find tests that are still untracked.

![Dynamic test markers](https://github.com/user-attachments/assets/f000388f-cdbc-418d-829b-a54309b8ffc4)

![Find untracked tests](https://github.com/user-attachments/assets/af40622f-f548-44a5-982b-344c74a65e13)

#### ⚡ One Unified Report—even with xdist

Run tests in parallel and receive one merged HTML and JSON report without an additional merge plugin or post-processing step.

#### 🧩 Export Merged JUnit XML with One Flag

Export links, logs, stdout, stderr, and flaky-test history to JUnit XML for tools such as TestRail, Xray, and Zephyr—without an additional XML merge step.

![Merged JUnit XML export](https://github.com/user-attachments/assets/02da5cc9-7ef5-4a3a-a475-88907964a9c6)

#### 📦 Know Exactly Where Every Report Came From

Include branch, commit, environment, generation time, and runtime metadata directly in the report.

![Report provenance metadata](https://github.com/user-attachments/assets/fa397d22-e40b-4e4a-9321-a2e88aea1c08)

#### 🐢 Spot Your Slowest Tests

Sort by duration and identify slow tests directly from the report.

![Slow test sorting](https://github.com/user-attachments/assets/b9760927-7c67-4bbf-b03d-e13964c727ee)

#### 📧 Share Reports by Email

Send the generated report through the optional email integration when a downloadable CI artifact is not the right delivery method.

![Email report](https://github.com/user-attachments/assets/3f40e206-5dfd-45e9-a511-4dd206cf3318)

---

## Already using pytest-html or Allure?

`pytest-html-plus` can run alongside `pytest-html`, so you can evaluate it without removing your existing reporter.

| Feature | pytest-html | Allure | pytest-html-plus |
|---|:---:|:---:|:---:|
| Portable HTML report | ✅ | ❌ | ✅ |
| No report server required | ✅ | ❌ | ✅ |
| Zero-config defaults | ✅ | ❌ | ✅ |
| xdist parallel run support | ⚠️ extra plugin | ✅ | ✅ built-in |
| Screenshots without custom hooks or decorators | ❌ | ❌ requires integration code | ✅ |
| Automatic log and `print()` capture | ❌ | ✅ | ✅ |
| Flaky-test detection and retry history | ❌ | ✅ | ✅ |
| Direct links to individual test results | ❌ | ✅ | ✅ |
| Slow-test highlighting | ❌ | ❌ | ✅ |
| Traceability links (Jira, Testmo, etc.) | ❌ | ✅ | ✅ |
| JUnit XML export | ❌ extra steps | ✅ | ✅ merged, one flag |
| Run metadata (branch, commit, environment) | ❌ | ✅ | ✅ |
| Reusable configuration profiles | ❌ | ❌ | ✅ |
| Untracked-test detection | ❌ | ❌ | ✅ |
| Copy logs and traces to clipboard | ❌ | ❌ | ✅ |
| Email reports | ❌ | ❌ | ✅ |
| Mobile-friendly layout | ❌ | ✅ | ✅ |

### Complete Feature List

| Feature | Details |
|---|---|
| 📸 **Automatic screenshots** | Selenium and Playwright screenshots captured without custom hooks or decorators |
| 📋 **Failure context** | Errors, traces, logs, stdout, and stderr collected with each result |
| 🔄 **Flaky-test detection** | Detects tests that fail and later pass; shows complete retry history |
| 🔗 **Direct test links** | Copy a link that opens the report at a specific expanded and highlighted test |
| 🔍 **Universal search** | Search by test name, issue ID, URL, error message, or trace snippet |
| ⚡ **xdist support** | Parallel runs produce a single merged report without extra merge steps |
| 🔗 **Traceability links** | Attach Jira, Testmo, Notion, or custom references to tests |
| 🏷️ **Dynamic markers** | Tag tests at runtime using standard `pytest.mark.*` markers |
| 🔎 **Untracked-test detection** | Find tests that have no associated issue or documentation link |
| 🧩 **JUnit XML export** | Generate merged XML compatible with TestRail, Xray, and Zephyr |
| 📦 **Run metadata** | Include branch, commit SHA, environment, and generation metadata |
| 🐢 **Slow-test visibility** | Sort results by duration to identify slow tests |
| 📋 **Copy to clipboard** | Copy nodeids, logs, traces, errors, and test links |
| 📝 **Configurable stream capture** | Control captured stdout and stderr with `--plus-output` |
| 📄 **Structured JSON report** | Use raw result data for integrations and post-processing |
| ⚙️ **Reusable configuration profiles** | Store commonly used report options in `pyproject.toml` |
| 🌐 **Auto-open report** | Open reports locally according to an always, failed, or never policy |
| 📱 **Mobile-friendly layout** | Investigate reports from desktop, tablet, or mobile screens |
| 📧 **Email reports** | Send reports through the optional email integration |

## Target Audience

This plugin is aimed at those who are:

- Tired of writing extra code just to generate reports or capture screenshots

- Manually attaching logs or outputs to test results

- Frustrated with archiving folders full of assets, CSS, JavaScript, and dashboards just to share test results

- Unwilling to refactor existing test suites or add decorators just to integrate with a reporting tool

- Looking for a zero-config, lightweight report that remains clean, useful, and portable

- Wanting more than a bare report without adopting a full dashboard, database, or external service

## Project Status

pytest-html-plus is stable and actively maintained, with its core reporting experience now well established. Future development will prioritize compatibility, reliability, bug fixes, and thoughtfully selected enhancements.

We're also looking for co-maintainers to help review pull requests, triage issues, and keep the project healthy across future Python and pytest releases.

If you're interested in becoming a long-term contributor, we'd love to hear from you. Please open an issue or start a discussion.

## Contributing

We welcome pull requests, issues, and feature suggestions from the community.

See the [contribution guide](CONTRIBUTING.md) for setup instructions.

## 📜 License

MIT
