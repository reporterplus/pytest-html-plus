⚡ **Test your code, not your reporting setup.**  
> _Get started with rich pytest reports in under 3 seconds. Just install — no setup required. The simplest, fastest reporter for pytest._

## Get a self-contained, actionable, easy-to-read single page HTML unified reports summarizing all your test results — no hassle, just clarity. Detect **flaky tests**, **attach screenshots** automatically without hooks and optionally send reports via email**. Works beautifully with or without `xdist`.

➡️ [View Demo Report](https://reporterplus.github.io/pytest-html-plus/)

[![Docs](https://img.shields.io/badge/docs-online-blue)](https://pytest-html-plus.readthedocs.io/en/main/) [![PyPI Downloads](https://static.pepy.tech/badge/pytest-html-plus)](https://pepy.tech/projects/pytest-html-plus) ![PyPI](https://img.shields.io/pypi/v/pytest-html-plus) ![Python Versions](https://img.shields.io/pypi/pyversions/pytest-html-plus)  ![License](https://img.shields.io/pypi/l/pytest-html-plus)  [![Unit Tests](https://github.com/reporterplus/pytest-html-plus/actions/workflows/unit-test.yml/badge.svg)](https://github.com/reporterplus/pytest-html-plus/actions/workflows/unit-test.yml) [![codecov](https://codecov.io/gh/reporterplus/pytest-html-plus/branch/main/graph/badge.svg)](https://codecov.io/gh/reporterplus/pytest-html-plus)

---

## Already using pytest-html or Allure?

No uninstall needed — `pytest-html-plus` works alongside `pytest-html`. Install it, run your suite, and see what you've been missing. Most teams uninstall `pytest-html` within the same day.

```bash
pip install pytest-html-plus
```

Your existing `pytest --html=report.html` commands keep working unchanged.

| Feature | pytest-html | Allure | pytest-html-plus |
|---|:---:|:---:|:---:|
| Self-contained single HTML file | ✅ | ❌ | ✅ |
| No server or CLI tool needed | ✅ | ❌ | ✅ |
| Zero config — works out of the box | ✅ | ❌ | ✅ |
| xdist parallel run support | ⚠️ extra plugin | ✅ | ✅ built-in |
| Screenshots (no hooks or decorators) | ❌ | ❌ requires decorators | ✅ |
| Automatic log & print() capture | ❌ | ✅ | ✅ |
| Flaky test detection + retry history | ❌ | ✅ | ✅ |
| Slow test highlighting | ❌ | ❌ | ✅ |
| Traceability links (Jira, Testmo, etc.) | ❌ | ✅ | ✅ |
| JUnit XML export (merged, one flag) | ❌ extra steps | ✅ | ✅ |
| Run metadata (branch, commit, env) | ❌ | ✅ | ✅ |
| Reusable config profiles | ❌ | ❌ | ✅ |
| Unlinked test detection | ❌ | ❌ | ✅ |
| Copy logs & traces to clipboard | ❌ | ❌ | ✅ |
| Email reports | ❌ | ❌ | ✅ |
| Mobile-friendly layout | ❌ | ✅ | ✅ |
| Report size | 🟢 single file | 🔴 many files | 🟢 single file |

---

## 🚀 Installation

```bash
pip install pytest-html-plus
# or with Poetry
poetry add pytest-html-plus
```

## Pytest HTML Plus Action

If you don't want the burden of installing pytest-html-plus manually and your project already manages dependencies with `requirements.txt` or Poetry, use this GitHub Action to generate rich pytest reports automatically.

[![🚀 Checkout on GitHub Marketplace](https://img.shields.io/badge/Marketplace-Pytest%20HTML%20Plus-blue?logo=github)](https://github.com/marketplace/actions/pytest-html-plus-action)
[![Documentation](https://img.shields.io/badge/docs-readthedocs.io-brightgreen)](https://pytest-html-plus.readthedocs.io/en/main/marketplace/usage.html)

## Pytest HTML Plus VSCode

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/reporterplus.pytest-html-plus-vscode?label=VS%20Code%20Marketplace&logo=visualstudiocode&logoColor=white&color=0078d7)](https://marketplace.visualstudio.com/items?itemName=reporterplus.pytest-html-plus-vscode)
[![Installs](https://img.shields.io/visual-studio-marketplace/i/reporterplus.pytest-html-plus-vscode)]
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://pytest-html-plus.readthedocs.io/en/main/extensions/vscode/usage.html)

## ✨ Features

#### 🧩 Seamless Combined XML Export to your favourite test management tools — No Plugins Needed
Export a fully merged JUnit XML report effortlessly — no external tools or plugins required. (No More merge html additional plugins or steps in your YAML to feed xml reports)

✔ Links, logs, stdout/stderr, and even flaky history — all included
✔ Works out-of-the-box with your test management tools (like TestRail, XRay, Zephyr)
✔ Just one flag. No extra lines of code. Total traceability.

![ScreenRecording2025-07-06at11 38 21PM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/02da5cc9-7ef5-4a3a-a475-88907964a9c6)

#### 🔄 Stop Guessing — See What's Breaking Your Flaky Tests
Instantly see how your tests behave across retries — from failure to recovery. Spot patterns like cache issues, race conditions, and random crashes without the guesswork.

![ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/1f7e0cd8-d2f9-47fd-8909-6f12adf8a800)

#### 🏷️ Tag your tests on the fly!
With dynamic markers, you can assign tags like `api`, `critical`, or `slow` — or any custom label — at runtime using standard `pytest.mark.*`.
No need for custom marker definitions. Perfect for smarter filtering, reporting, and analysis.

![ScreenRecording2025-07-12at10 15 33PM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/f000388f-cdbc-418d-829b-a54309b8ffc4)

#### 📦 Ship reports with provenance 📜 — full run metadata included 📋 and copy-ready.

![ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/fa397d22-e40b-4e4a-9321-a2e88aea1c08)

#### 📋⚡ Turn failure context into a single click — copy logs, traces, and errors instantly for your team.

![ezgif com-video-to-gif-converter (1)](https://github.com/user-attachments/assets/396e8cf6-862b-4619-82bf-81a8eae8e7b6)

#### Easily track Untracked test scenarios

![ScreenRecording2025-06-29at1 06 02AM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/af40622f-f548-44a5-982b-344c74a65e13)

#### 🔍 Universal Test Search + Smart Traceability

Whether you're tracing coverage, investigating failures, or tracking unlinked test cases — this search has your back!

Just start typing, and the dashboard will instantly filter tests by:

✅ Test names

✅ Linked issue or documentation IDs (JIRA, Testmo, Notion, etc.)

✅ Custom URLs or keywords present in linked references

✅ Error messages and trace snippets to quickly group related failures

<img width="800" height="421" alt="new_search" src="https://github.com/user-attachments/assets/54858747-ab16-4d4f-baa9-0d651a1d8bac" />


#### 📸 Screenshot Support: View screenshots directly in the report to understand failures faster.

#### 📧 Email Test Reports: Send your reports via email effortlessly using SendGrid integration.

![Screenshot 2025-05-28 at 4 38 49 PM](https://github.com/user-attachments/assets/3f40e206-5dfd-45e9-a511-4dd206cf3318)

#### 🐢 Spot Slow Tests: Highlights the slowest tests so you know where to optimize your suite.

![ScreenRecording2025-06-21at2 52 49PM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/b9760927-7c67-4bbf-b03d-e13964c727ee)

#### 📝 Comprehensive output capture: All your test logs with loggers, print() statements, and screenshots are automatically captured and embedded in the report...

![ezgif-744a5d34a4c46d](https://github.com/user-attachments/assets/209cd2c0-d33b-48ec-b58b-8c8991ce35be)

### Complete Feature List

| Feature | Details |
|---|---|
| 📊 **Single-file HTML report** | Fully self-contained — no external CSS, JS, or image folders to archive |
| 🔄 **Flaky test detection** | Detects tests that fail then pass on retry; shows full retry history |
| 📸 **Automatic screenshots** | Selenium & Playwright screenshots captured and embedded with no conftest hooks |
| 🧩 **JUnit XML export** | Merged XML output compatible with TestRail, Xray, and Zephyr (`--generate-xml`) |
| 🔗 **Traceability links** | Attach Jira, Testmo, Notion, or any URL to a test; rendered and searchable in the report |
| 🏷️ **Dynamic markers** | Tag tests at runtime with `pytest.mark.*` — no marker pre-registration needed |
| 🔍 **Universal search** | Filter tests by name, issue ID, or any URL keyword in real time |
| 🐢 **Slow test highlighting** | Slowest tests in the run automatically flagged |
| 📋 **Copy-to-clipboard** | Copy test path, logs, trace, and errors in one click |
| 📦 **Run metadata** | Branch, commit SHA, environment, and custom metadata embedded in the report header |
| 📝 **Comprehensive log capture** | `print()`, logger output, and stdout/stderr automatically captured per test |
| ⚡ **xdist support** | Parallel runs with `pytest-xdist` produce a single merged report, no extra steps |
| 🌐 **Auto-open report** | `--should-open-report` opens the report in your browser after a run (always / failed / never) |
| 📄 **JSON report** | Raw JSON output (`--json-report`) for custom dashboards or post-processing |
| 🔎 **Unlinked test detection** | Instantly filter tests that have no associated issue or documentation link |
| ⚙️ **Reusable config profiles** | Define named profiles in `pyproject.toml` (`--profile=ci`) — no more repeated CLI flags |
| 📱 **Mobile-friendly layout** | Report renders cleanly on any screen size |
| 📧 **Email reports** | Send reports via SendGrid integration (`--send-email`) |

## Target Audience

This plugin is aimed at those who are:

- Tired of writing extra code just to generate reports or capture screenshots

- Manually attaching logs or outputs to test results

- Are frustrated with archiving folders full of assets, CSS, JS, and dashboards just to share test results.

- Don't want to refactor existing test suites or tag everything with new decorators just to integrate with a reporting tool.

- Prefer simplicity — a zero-config, zero code, lightweight report that still looks clean, useful, and polished.

- Want "just enough" — not bare-bones plain text, not a full dashboard with database setup — just a portable HTML report that STILL supports features like links, screenshots, and markers.

## Contributing

We welcome pull requests, issues, and feature suggestions from the community.

See the [contribution guide](CONTRIBUTING.md) for setup instructions.

## 📜 License

MIT
