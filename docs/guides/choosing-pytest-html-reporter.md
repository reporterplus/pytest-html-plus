# Choosing a pytest HTML Reporter: Setup, Screenshots, and xdist

A useful pytest report should answer two questions: what failed, and what evidence
will help fix it? The right reporter also needs to fit the way a project runs tests:
locally or in CI, serially or with `pytest-xdist`, and with or without browser
automation.

This guide compares
[`pytest-html-plus` 1.3.1](https://github.com/reporterplus/pytest-html-plus/tree/v1.3.1)
and
[`pytest-html-reporter` 0.4.3](https://github.com/prashanth-sams/pytest-html-reporter/tree/v0.4.3).
It describes behavior verified in those releases from their documentation, source,
and tests. Both projects are active, so check their release notes when evaluating a
newer version.

## At a glance

| Capability | pytest-html-plus 1.3.1 | pytest-html-reporter 0.4.3 |
| --- | --- | --- |
| Report from a bare `pytest` run | Yes | Yes |
| Automatic failure screenshots | Synchronous Selenium and Playwright-style fixtures | Synchronous Selenium and Playwright-style fixtures |
| Custom hook or `attach()` required for those automatic screenshots | No | No |
| One merged report from `pytest -n ...` | Yes | Yes |
| Captured stdout, stderr, logging, and failure details | Yes | Yes |
| Machine-readable result data | `final_report.json` by default | `output.json` beside the HTML report |
| Reporting server required | No | No |
| Cross-machine shard merge workflow | Not documented | Built-in `pytest-html-reporter merge` command |
| Historical archives, trends, steps, BDD, and coverage views | Not built in as a combined history UI | Built in |
| Verified editor integration | VS Code extension consumes the JSON report | Not independently verified from the reporter repository |

The table deliberately excludes claims that could not be verified in the released
repositories. In particular, `pytest-html-reporter` lists dedicated GitHub Action
and VS Code integrations in its README, but that repository does not link to or
contain their implementations.

## Getting started and setup effort

Both reporters register as pytest plugins, so installation is enough to produce a
report from an existing suite:

```console
pip install pytest-html-plus
pytest
```

`pytest-html-plus` writes `report_output/report.html` and
`report_output/final_report.json` by default. Output names can be changed without
test-code changes:

```console
pytest --html-output=reports/smoke --json-report=smoke.json
```

The equivalent starting point for the other reporter is also short:

```console
pip install pytest-html-reporter
pytest
```

It writes `report/pytest_html_report.html` and `report/output.json`. Use
`--html-report` to choose the report directory or filename:

```console
pytest --html-report=reports/smoke/report.html
```

Neither tool requires decorators, imports, a `conftest.py` hook, or a reporting
service for its default report. Both also support named configuration profiles for
teams that want stable local and CI settings. See the
[`pytest-html-plus` profile implementation](https://github.com/reporterplus/pytest-html-plus/blob/v1.3.1/pytest_html_plus/plugin.py)
and the
[`pytest-html-reporter` profile documentation](https://github.com/prashanth-sams/pytest-html-reporter/blob/v0.4.3/README.md#named-configuration-profiles).

## Screenshots and failure investigation

For ordinary synchronous browser tests, both tools inspect fixtures at the end of a
test and capture a screenshot automatically. A minimal Playwright test therefore
does not need reporter-specific code:

```python
def test_checkout(page):
    page.goto("https://example.test/cart")
    assert page.locator("h1").inner_text() == "Cart"
```

With `pytest-html-plus`, failed tests are captured by default. Use
`--capture-screenshots=all` for every test or `--capture-screenshots=none` to turn
automatic capture off. Its resolver detects Playwright-style `screenshot()` and
Selenium-style screenshot methods; the behavior is covered by its
[`driver screenshot tests`](https://github.com/reporterplus/pytest-html-plus/blob/v1.3.1/tests/unit/test_driver_screenshots.py).

`pytest-html-reporter` likewise defaults to failed tests and supports
`--report-screenshots=all` or `none`. Its
[`automatic screenshot tests`](https://github.com/prashanth-sams/pytest-html-reporter/blob/v0.4.3/tests/unit/test_auto_screenshots.py)
verify fixture discovery without a user hook. It also provides optional `attach()`
calls for an exact mid-test moment, async Playwright, or a `unittest` teardown that
closes the browser before automatic capture runs. Optional attachment code is not a
requirement for its normal synchronous failure capture.

Both reports retain assertion errors and tracebacks as well as captured stdout,
stderr, and logging. `pytest-html-plus` exposes an output-size policy:

```console
pytest --plus-output=failed-only
```

The default is `all`; `failed-only` keeps output for failures, setup/teardown
errors, and expected failures, while `none` omits stdout and stderr. Reporter has a
similar `--report-logs=all|failed|none` policy plus a per-test character limit.
These controls affect captured output, not the assertion failure or traceback.

As with any pytest reporter, `-s`/`--capture=no` prevents pytest from supplying
captured stdout and stderr. Remove `-s`, or use `--capture=tee-sys` when terminal
streaming and report capture are both needed.

## Parallel execution with pytest-xdist

Both tools produce one combined report for a normal xdist run:

```console
pytest -n auto
```

`pytest-html-plus` writes per-worker JSON and merges it on the controller before
rendering the final HTML and JSON. The behavior is exercised by its
[`xdist worker-directory tests`](https://github.com/reporterplus/pytest-html-plus/blob/v1.3.1/tests/unit/test_worker_json_dir.py).
`--worker-json-dir` is available when the default temporary location is unsuitable,
for example in a read-only CI workspace.

`pytest-html-reporter` sends each worker's records to the controller, which orders
and renders a single result set. Its
[`xdist tests`](https://github.com/prashanth-sams/pytest-html-reporter/blob/v0.4.3/tests/unit/test_xdist.py)
cover worker collection and merged results.

Do not confuse xdist with cross-machine sharding. xdist has one controller and
needs no post-processing in either tool. Reporter additionally documents a shard
bundle and merge command for separate machines or CI stages:

```console
pytest tests/ui --html-report=report --report-shard=ui
pytest-html-reporter merge artifacts --html-report=report
```

No equivalent cross-machine merge workflow was verified for `pytest-html-plus`.
Its built-in merge applies to workers participating in the same xdist session; use
unique output paths for separate pytest jobs and combine their data in your own CI
step if necessary.

## Portability, CI integration, and reporting infrastructure

Neither project needs a database, hosted dashboard, or report server. The generated
HTML opens locally and can be uploaded as a CI artifact. Keep the whole output
directory when sharing a report: screenshots and machine-readable output are
companion artifacts even when the page's CSS and JavaScript are embedded.

A generic CI job for `pytest-html-plus` can therefore remain conventional:

```yaml
- run: pytest -n auto --html-output=report_output
- uses: actions/upload-artifact@v4
  with:
    name: pytest-report
    path: report_output/
```

The project also publishes a
[`pytest-html-plus` GitHub Action](https://github.com/marketplace/actions/pytest-html-plus-action)
for teams that prefer a packaged workflow. The
[`pytest-html-plus` VS Code extension](https://marketplace.visualstudio.com/items?itemName=reporterplus.pytest-html-plus-vscode)
reads `final_report.json`, shows results in the editor, and navigates to test source;
it consumes an existing report rather than replacing pytest or the HTML artifact.

For other CI systems, upload the report directory with the platform's normal
artifact mechanism. Both reporters also generate JUnit XML for CI test-result
interfaces. Their JSON artifacts can feed scripts and dashboards without scraping
HTML. Plus documents a stable result-oriented JSON file for custom integrations;
Reporter's `output.json` also drives its archive and analytics views, and its
attachment APIs add structured text, JSON, files, and HTTP exchanges.

Reporter may be the better fit when the report itself should retain historical
builds, calculate trends, display coverage, represent named or BDD steps, or merge
cross-machine shards. Those capabilities add useful analysis without requiring a
separate service, though they also make the report artifact responsible for more
history and configuration.

## Choosing based on your project's requirements

Choose based on the workflow you need to maintain:

- Start with `pytest-html-plus` when you want a small reporting surface: install the
  plugin, keep existing tests unchanged, collect automatic debugging context, and
  archive portable HTML plus straightforward JSON. Its published VS Code and GitHub
  Actions integrations are useful when those are already part of the toolchain.
- Consider `pytest-html-reporter` when archives and trend analysis belong inside the
  report, or when coverage, test steps, BDD presentation, richer attachment APIs,
  and explicit cross-machine shard merging outweigh the value of a narrower
  artifact.
- Run a representative slice of the actual suite before deciding. Include a failed
  browser test, a fixture setup error, captured logs, reruns, and `pytest -n auto`.
  Then inspect both the report and the files that CI would retain.

The practical goal is not the longest feature list. It is a report that preserves
enough evidence to investigate failures while keeping tests independent of a
reporting platform. Both projects can work without hosted infrastructure; the main
choice is whether the report should remain a focused run artifact or also become a
history and analysis surface.

## Primary sources

- [`pytest-html-plus` 1.3.1 source and tests](https://github.com/reporterplus/pytest-html-plus/tree/v1.3.1)
- [`pytest-html-plus` CLI documentation](https://pytest-html-plus.readthedocs.io/en/main/cli/cli.html)
- [`pytest-html-reporter` 0.4.3 README](https://github.com/prashanth-sams/pytest-html-reporter/blob/v0.4.3/README.md)
- [`pytest-html-reporter` 0.4.3 source and tests](https://github.com/prashanth-sams/pytest-html-reporter/tree/v0.4.3)
