⚠️ Package renamed: This plugin was previously known as pytest-reporter-plus.

> ⚡ **Plug. Play. Quickly debug without delay.**  
> _Just install. No setup. Crystal-clear test reports out of the box._

## Get a self-contained, actionable, easy-to-read single page HTML unified reports summarizing all your test results — no hassle, just clarity. Detect **flaky tests**, and optionally send reports via email**. Works beautifully with or without `xdist`.

[![Docs](https://img.shields.io/badge/docs-online-blue)](https://pytest-html-plus.readthedocs.io/en/latest/index.html) [![PyPI Downloads](https://static.pepy.tech/badge/pytest-html-plus)] (https://pepy.tech/projects/pytest-html-plus) ![PyPI](https://img.shields.io/pypi/v/pytest-html-plus) ![Python Versions](https://img.shields.io/pypi/pyversions/pytest-html-plus)  ![License](https://img.shields.io/pypi/l/pytest-html-plus)  [![Unit Tests](https://github.com/reach2jeyan/pytest-report-plus/actions/workflows/unit-test.yml/badge.svg)](https://github.com/reach2jeyan/pytest-report-plus/actions/workflows/unit-test.yml)

[![Discord](https://img.shields.io/discord/1377581416337903646?labelColor=black&logo=discord&logoColor=c20a71&style=for-the-badge&color=c20a71)](https://discord.gg/Pjy2sCBC) 

## 🚀 Installation

```bash
pip install pytest-html-plus
# or with Poetry
poetry add pytest-html-plus
```

# Keep using your regular pytest commands — just plug this in to unlock the below powerful reporting features with zero extra effort.

## ✨ Features

#### 🧩 Seamless Combined XML Export to your favourite test management tools — No Plugins Needed
Export a fully merged JUnit XML report effortlessly — no external tools or plugins required. (No More merge html additional plugins or steps in your YAML to feed xml reports)

✔ Links, logs, stdout/stderr, and even flaky history — all included
✔ Works out-of-the-box with your test management tools (like TestRail, XRay, Zephyr)
✔ Just one flag. No extra lines of code. Total traceability.


![ScreenRecording2025-07-06at11 38 21PM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/02da5cc9-7ef5-4a3a-a475-88907964a9c6)

#### 🏷️ Tag your tests on the fly!
With dynamic markers, you can assign tags like `api`, `critical`, or `slow` — or any custom label — at runtime using standard `pytest.mark.*`.
No need for custom marker definitions. Perfect for smarter filtering, reporting, and analysis.

![ScreenRecording2025-07-12at10 15 33PM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/f000388f-cdbc-418d-829b-a54309b8ffc4)

#### Easily track Untracked test scenarios

![ScreenRecording2025-06-29at1 06 02AM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/af40622f-f548-44a5-982b-344c74a65e13)

#### 🔍 Universal Test Search + Smart Link Navigation

Whether you're trying to trace coverage or track unlinked test cases — this search has your back!

Just start typing, and the dashboard will instantly filter tests by:

✅ Test name

✅ Linked issue/documentation IDs (like JIRA, Testmo, Notion, etc.)

✅ Custom URLs or keywords present in the links

![ScreenRecording2025-06-21at3 10 06PM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/f81c9a81-f98d-4151-ad7a-c1184cd199eb)

#### 🔄 Flaky Test Detection: Automatically flags flaky tests so you can spot and fix inconsistent failures quickly.

![ScreenRecording2025-06-21at2 37 31PM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/90f694bf-189c-45e1-8e1d-7acd2a975f91)

#### 📸 Screenshot Support: View screenshots directly in the report to understand failures faster.

#### 📧 Email Test Reports: Send your reports via email effortlessly using SendGrid integration.

![Screenshot 2025-05-28 at 4 38 49 PM](https://github.com/user-attachments/assets/3f40e206-5dfd-45e9-a511-4dd206cf3318)

#### 🐢 Spot Slow Tests: Highlights the slowest tests so you know where to optimize your suite.

![ScreenRecording2025-06-21at2 52 49PM-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/b9760927-7c67-4bbf-b03d-e13964c727ee)

#### 📝 Comprehensive output capture: All your test logs with loggers, print() statements, and screenshots are automatically captured and embedded in the report...

![ezgif-744a5d34a4c46d](https://github.com/user-attachments/assets/209cd2c0-d33b-48ec-b58b-8c8991ce35be)

### AND MANY MANY MORE

## Target Audience

This plugin is aimed at those who are:

- Tired of writing extra code just to generate reports or capture screenshots

- Manually attaching logs or outputs to test results

- Are frustrated with archiving folders full of assets, CSS, JS, and dashboards just to share test results.

- Don’t want to refactor existing test suites or tag everything with new decorators just to integrate with a reporting tool.

- Prefer simplicity — a zero-config, zero code, lightweight report that still looks clean, useful, and polished.

- Want “just enough” — not bare-bones plain text, not a full dashboard with database setup — just a portable HTML report that STILL supports features like links, screenshots, and markers.


## Comparison with Alternatives
Most existing pytest reporter tools:

Only generate HTML reports from a single run  (by making you write code for creating xmls like pytest-html) OR they generate all the JS and png files that are not the scope of test results and force you to archive it.

Heavy duty with bloated charts and other test management features(when they arent your only test management system either) increasing your archive size.

This plugin aims to fill those gaps by acting as a companion layer on top of the JSON report, focusing on:

🔄 Merge + flakiness intelligence

🔗 Traceability via metadata

🧼 HTML that’s both readable and minimal

🧼 Quickly copy test paths and run in your local

## Contributing

We welcome pull requests, issues, and feature suggestions from the community.

See the [contribution guide](https://pytest-html-plus.readthedocs.io/en/latest/contributing.html) for setup instructions.


## 📜 License

MIT
