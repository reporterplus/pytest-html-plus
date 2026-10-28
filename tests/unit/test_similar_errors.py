import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from pytest_html_plus.json_merge import merge_json_reports
from pytest_html_plus.plugin import pytest_addoption, resolve_similar_errors
from pytest_html_plus.similar_errors import annotate_similar_errors, error_fingerprint
from tests.unit.conftest import make_test_result


def result(index, **kwargs):
    return make_test_result(
        nodeid=f"test_a.py::test_{index}",
        test=f"test_{index}",
        **{"status": "failed", "error": "E ValueError: invalid account name", **kwargs},
    )


@pytest.mark.parametrize(
    "error",
    [
        None,
        "",
        "AssertionError",
        "AssertionError:",
        "AssertionError: assert False",
        "TimeoutError: 3000",
        "TimeoutError",
        "TimeoutError:",
        "TimeoutError: timed out",
        "TimeoutError: operation timed out",
        "TimeoutError: timeout exceeded",
        "Exception: error",
    ],
)
def test_uninformative(error):
    assert error_fingerprint(error) is None
    report = {"results": [result(1, error=error), result(2, error=error)]}
    annotate_similar_errors(report)
    assert report["similar_error_groups"] == {}
    assert all("similar_error_group" not in test for test in report["results"])


@pytest.mark.parametrize(
    "left,right",
    [
        ("ValueError: invalid name", "TypeError: invalid name"),
        (
            "AssertionError: expected login page",
            "AssertionError: expected checkout page",
        ),
        ("ValueError: missing /tmp/account", "ValueError: missing /tmp/customer"),
    ],
)
def test_meaningful_differences(left, right):
    assert error_fingerprint(left) != error_fingerprint(right)


@pytest.mark.parametrize(
    "left,right",
    [
        (
            "E ValueError: invalid  account name",
            "\x1b[31mValueError: invalid account name\x1b[0m",
        ),
        (
            "RuntimeError: bad object at 0x123abc",
            "RuntimeError: bad object at 0x456def",
        ),
        (
            "playwright._impl._errors.Error:\nBrowserType.launch: Executable doesn't exist at /ms-playwright/a",
            "playwright._impl._errors.Error: BrowserType.launch: Executable doesn't exist at /ms-playwright/a",
        ),
    ],
)
def test_normalization(left, right):
    assert error_fingerprint(left) == error_fingerprint(right)
    assert error_fingerprint(left)


@pytest.mark.parametrize("count", [2, 4, 100])
def test_groups_and_retries(count):
    tests = [result(i, attempts=[{"status": "failed"}] * 3) for i in range(count)]
    tests += [
        result("flaky", status="passed", flaky=True),
        result("other", error="ValueError: different message"),
    ]
    report = {"results": tests}
    annotate_similar_errors(report)
    (group,) = report["similar_error_groups"].values()
    assert len(group["nodeids"]) == count
    assert len(set(group["nodeids"])) == count
    assert all("similar_error_group" in t for t in tests[:count])
    assert all("similar_error_group" not in t for t in tests[count:])


@pytest.mark.parametrize("status", ["passed", "skipped", "xfailed", "xpassed"])
def test_non_failures(status):
    report = {"results": [result(1), result(2, status=status)]}
    annotate_similar_errors(report)
    assert report["similar_error_groups"] == {}


def test_no_self_match():
    report = {"results": [result(1), result(1)]}
    annotate_similar_errors(report)
    assert report["similar_error_groups"] == {}


@pytest.mark.parametrize("workers", [1, 2])
@pytest.mark.parametrize("enabled", [False, True])
def test_aggregation_json_only(tmp_path, workers, enabled, monkeypatch):
    source = tmp_path / "workers"
    source.mkdir()
    tests = [result(1), result(2, status="error")]
    for i in range(workers):
        (source / f"gw{i}.json").write_text(
            json.dumps({"results": tests[i::workers]}), encoding="utf-8"
        )
    if not enabled:
        monkeypatch.setattr(
            "pytest_html_plus.json_merge.annotate_similar_errors",
            lambda _: pytest.fail("analysis ran while disabled"),
        )
    output = tmp_path / "final.json"
    merge_json_reports(source, output, similar_errors=enabled)
    data = json.loads(output.read_text(encoding="utf-8"))
    assert ("similar_error_groups" in data) is enabled
    assert all(("similar_error_group" in t) is enabled for t in data["results"])


@pytest.mark.parametrize(
    "cli,toml,expected",
    [
        (None, None, True),
        ("true", None, True),
        ("false", None, False),
        (None, True, True),
        (None, False, False),
        ("false", True, False),
        ("true", False, True),
    ],
)
def test_configuration(tmp_path, cli, toml, expected):
    (tmp_path / "pyproject.toml").write_text(
        "[tool.pytest-html-plus]\n"
        + (f"similar_errors = {str(toml).lower()}\n" if toml is not None else ""),
        encoding="utf-8",
    )
    config = SimpleNamespace(rootpath=tmp_path, getoption=lambda *a, **kw: cli)
    assert resolve_similar_errors(config) is expected


def test_option_accepts_explicit_booleans():
    from _pytest.config.argparsing import Parser

    parser = Parser(_ispytest=True)
    pytest_addoption(parser)
    for value in ("true", "false"):
        assert (
            parser.parse([f"--plus-similar-errors={value}"]).plus_similar_errors
            == value
        )
    assert parser.parse([]).plus_similar_errors is None


def make_report(reporter_factory):
    tests = [
        result(1),
        result(2, status="error"),
        result(3),
        result(4, error="ValueError: unmatched error"),
    ]
    data = {"results": tests}
    annotate_similar_errors(data)
    reporter = reporter_factory(results=tests)
    reporter.similar_error_groups = data["similar_error_groups"]
    reporter.generate_html_report()
    return Path(reporter.output_dir, "report.html")


def test_html(reporter_factory):
    content = make_report(reporter_factory).read_text(encoding="utf-8")
    assert content.count(">2 similar</button>") == 3
    assert 'id="similarErrorsOnlyCheckbox"' not in content
    assert content.count('data-group="similar-1"') == 3
    assert "copyTestLink(" in content
    assert "revealTestFromFragment()" in content
    assert "similar-errors-data" in content


def test_disabled_html(reporter_factory):
    reporter = reporter_factory(results=[result(1)])
    reporter.generate_html_report()
    content = Path(reporter.output_dir, "report.html").read_text(encoding="utf-8")
    assert 'class="similar-errors-badge"' not in content
    assert 'id="similar-errors-data"' not in content
    assert 'id="similarErrorsOnlyCheckbox"' not in content
    assert 'class="header failed"' in content
    assert "report-card-header" not in content


def test_browser_navigation(reporter_factory):
    from playwright.sync_api import sync_playwright

    from pytest_html_plus.generate_html_report import stable_test_anchor

    path = make_report(reporter_factory)
    with sync_playwright() as pw:
        if not Path(pw.chromium.executable_path).exists():
            pytest.skip(
                "Chromium is not installed for this Playwright version; run python -m playwright install chromium"
            )
        browser = pw.chromium.launch()
        page = browser.new_page()
        page.goto(path.as_uri())
        badge = page.locator(".similar-errors-badge").first
        badge.focus()
        page.keyboard.press("Enter")
        panel = page.locator("#similar-errors-popover")
        assert panel.is_visible()
        assert panel.locator("a").all_text_contents() == ["test_2", "test_3"]
        assert (
            "Similar messages may have different causes."
            in panel.locator(".similar-errors-note").inner_text()
        )
        assert (
            panel.locator(".similar-errors-note code").inner_text()
            == "--plus-similar-errors=false"
        )
        page.keyboard.press("Escape")
        assert not panel.is_visible()
        assert badge.evaluate("(b) => b === document.activeElement")
        badge.click()
        page.mouse.click(1, 1)
        assert not panel.is_visible()
        target = "#" + stable_test_anchor("test_a.py::test_2")
        page.locator("#universal-search").fill("test_1")
        assert not page.locator(target).is_visible()
        badge.click()
        panel.get_by_role("link", name="test_2", exact=True).click()
        page.wait_for_function(
            '(id) => document.querySelector(id).classList.contains("deep-link-target")',
            arg=target,
        )
        assert page.locator(target).is_visible()
        assert page.locator(target + " .details").is_visible()
        assert not panel.is_visible()
        assert page.url.endswith(target)
        assert page.locator("#universal-search").input_value() == ""
        page.evaluate(
            "Object.defineProperty(navigator, 'clipboard', {value: {writeText: text => {window.copied = text; return Promise.resolve();}}})"
        )
        page.locator(target + " .test-link-btn").click()
        assert page.evaluate("window.copied") == page.url
        page.go_back()
        page.go_forward()
        assert page.url.endswith(target)
        browser.close()


@pytest.mark.parametrize("workers", [0, 2])
@pytest.mark.parametrize("similar_option", [None, "true", "false"])
def test_real_execution(tmp_path, workers, similar_option):
    import os
    import subprocess
    import sys

    (tmp_path / "test_example.py").write_text(
        """
import pytest
@pytest.fixture
def broken():
    raise ValueError('invalid account name')
def test_setup(broken):
    pass
def test_call():
    raise ValueError('invalid account name')
@pytest.fixture
def broken_teardown():
    yield
    raise ValueError('invalid account name')
def test_teardown(broken_teardown):
    pass
def test_assertion_login():
    raise AssertionError('expected login page')
def test_assertion_checkout():
    raise AssertionError('expected checkout page')
def test_pass():
    pass
""",
        encoding="utf-8",
    )
    env = os.environ.copy()
    for key in (
        "PYTEST_XDIST_WORKER",
        "PYTEST_XDIST_WORKER_COUNT",
        "PYTEST_XDIST_TESTRUNUID",
        "PYTEST_CURRENT_TEST",
        "PYTEST_ADDOPTS",
    ):
        env.pop(key, None)
    from importlib.metadata import entry_points

    # Installed distributions already register the plugin through pytest11.
    # Explicit registration is only needed when testing an uninstalled checkout.
    env.pop("PYTEST_PLUGINS", None)
    if not any(
        ep.value == "pytest_html_plus.plugin" for ep in entry_points(group="pytest11")
    ):
        env["PYTEST_PLUGINS"] = "pytest_html_plus.plugin"
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[2])
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--should-open-report=never",
    ]
    if similar_option is not None:
        cmd.append(f"--plus-similar-errors={similar_option}")
    if workers:
        cmd += ["-n", str(workers)]
    run = subprocess.run(
        cmd, cwd=tmp_path, env=env, capture_output=True, text=True, timeout=90
    )
    assert run.returncode == 1, run.stdout + run.stderr
    report = json.loads(
        (tmp_path / "report_output/final_report.json").read_text(encoding="utf-8")
    )
    if similar_option == "false":
        assert "similar_error_groups" not in report
        assert all("similar_error_group" not in test for test in report["results"])
        assert 'class="similar-errors-badge"' not in (
            tmp_path / "report_output/report.html"
        ).read_text(encoding="utf-8")
        return
    (group,) = report["similar_error_groups"].values()
    assert set(group["nodeids"]) == {
        "test_example.py::test_setup",
        "test_example.py::test_call",
        "test_example.py::test_teardown",
    }
    by_name = {test["test"]: test for test in report["results"]}
    assert by_name["test_setup"]["status"] == "error"
    assert by_name["test_teardown"]["status"] == "error"
    assert by_name["test_call"]["status"] == "failed"
    for name in ("test_assertion_login", "test_assertion_checkout"):
        assert "similar_error_group" not in by_name[name]
    if workers:
        assert (
            len(
                {
                    by_name[name]["worker"]
                    for name in ("test_setup", "test_call", "test_teardown")
                }
            )
            == 2
        )
    assert (tmp_path / "report_output/report.html").read_text(encoding="utf-8").count(
        ">2 similar</button>"
    ) == 3


def test_profile_boolean(tmp_path):
    from pytest_html_plus.plugin import apply_plus_profile_args

    (tmp_path / "pyproject.toml").write_text(
        "[tool.pytest-html-plus.profiles.ci]\nsimilar_errors = true\n", encoding="utf-8"
    )
    args = apply_plus_profile_args(
        ["--plus-profile=ci", "--plus-similar-errors=false"], start_path=tmp_path
    )
    assert args.index("--plus-similar-errors=true") < args.index(
        "--plus-similar-errors=false"
    )


def test_multiline_messages_differ():
    assert error_fingerprint(
        "AssertionError: invalid response\nexpected login"
    ) != error_fingerprint("AssertionError: invalid response\nexpected checkout")


@pytest.mark.parametrize("kind", ["playwright._impl._errors.Error", "ValueError"])
@pytest.mark.parametrize("path", ["/cache/worker2/chrome", "C:/cache/worker2/chrome"])
def test_preserves_executable_paths(kind, path):
    first = f"{kind}: Executable doesn't exist at /cache/worker1/chrome"
    other = f"{kind}: Executable doesn't exist at {path}"
    report = {
        "results": [
            result(1, error=first),
            result(2, error=first),
            result(3, error=other),
        ]
    }
    annotate_similar_errors(report)
    (group,) = report["similar_error_groups"].values()
    assert group["nodeids"] == ["test_a.py::test_1", "test_a.py::test_2"]
    assert "similar_error_group" not in report["results"][2]
    assert "/cache/worker1/chrome" in group["message"]


def test_meaningful_timeout_matches():
    report = {
        "results": [
            result(i, error="TimeoutError: waiting for checkout confirmation")
            for i in (1, 2)
        ]
    }
    annotate_similar_errors(report)
    assert len(report["similar_error_groups"]) == 1


@pytest.mark.parametrize(
    "message",
    [
        "transaction at 0x123abc",
        "transaction ID 0x123abc",
        "instruction failed at 0x123abc",
        "missing /cache/0x123abc/config.json",
    ],
)
def test_preserves_meaningful_hex_identifiers(message):
    first = "RuntimeError: " + message
    second = first.replace("123abc", "456def")
    assert error_fingerprint(first) != error_fingerprint(second)


def test_normalizes_python_object_representation():
    first = "RuntimeError: invalid <client.Session object at 0x123abc>"
    second = "RuntimeError: invalid <client.Session object at 0x456def>"
    assert error_fingerprint(first) == error_fingerprint(second)


def test_default_enabled_without_pyproject(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "pytest_html_plus.plugin._find_pyproject_toml", lambda *args: None
    )
    config = SimpleNamespace(rootpath=tmp_path, getoption=lambda *args, **kwargs: None)
    assert resolve_similar_errors(config) is True


@pytest.mark.parametrize("toml_value", ['"true"', '"false"', "1", "0", "[]"])
def test_rejects_non_boolean_toml_setting(tmp_path, toml_value):
    (tmp_path / "pyproject.toml").write_text(
        f"[tool.pytest-html-plus]\nsimilar_errors = {toml_value}\n",
        encoding="utf-8",
    )
    config = SimpleNamespace(rootpath=tmp_path, getoption=lambda *args, **kwargs: None)

    with pytest.raises(
        pytest.UsageError, match="^similar_errors must be a TOML boolean$"
    ):
        resolve_similar_errors(config)


@pytest.mark.parametrize("toml_value", ['"true"', '"false"', "1", "0", "[]"])
def test_rejects_non_boolean_profile_setting(tmp_path, toml_value):
    from pytest_html_plus.plugin import apply_plus_profile_args

    (tmp_path / "pyproject.toml").write_text(
        f"[tool.pytest-html-plus.profiles.ci]\nsimilar_errors = {toml_value}\n",
        encoding="utf-8",
    )
    with pytest.raises(
        pytest.UsageError,
        match="^Profile 'ci' option 'similar_errors' must be true or false$",
    ):
        apply_plus_profile_args(["--plus-profile=ci"], start_path=tmp_path)


@pytest.mark.parametrize(
    "boundary",
    [
        "Call log:",
        "Traceback (most recent call last):",
        "During handling of the above exception, another exception occurred:",
        "The above exception was the direct cause of the following exception:",
    ],
)
def test_fingerprint_stops_at_diagnostic_boundary(boundary):
    message = "ValueError: invalid account name\nexpected a nonempty value"
    expected = ("ValueError", "invalid account name expected a nonempty value")
    assert error_fingerprint(message) == expected
    assert (
        error_fingerprint(
            f"{message}\n{boundary}\ndiagnostic details that must not enter the fingerprint"
        )
        == expected
    )
