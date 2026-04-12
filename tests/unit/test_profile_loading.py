import pytest

from pytest_html_plus.plugin import apply_plus_profile_args


def write_pyproject(tmp_path, body):
    pyproject_file = tmp_path / "pyproject.toml"
    pyproject_file.write_text(body, encoding="utf-8")
    return pyproject_file


def test_profile_args_are_prepended_so_cli_can_override(tmp_path):
    write_pyproject(
        tmp_path,
        """
[tool.pytest-html-plus.profiles.ci]
html-output = "ci-report"
json-report = "ci.json"
capture-screenshots = "all"
generate-xml = true
plus-email = false
""".strip(),
    )

    args = apply_plus_profile_args(
        ["tests/unit", "--plus-profile=ci", "--json-report=override.json"],
        start_path=tmp_path,
    )

    assert args == [
        "--html-output=ci-report",
        "--json-report=ci.json",
        "--capture-screenshots=all",
        "--generate-xml",
        "tests/unit",
        "--json-report=override.json",
    ]


def test_profile_can_be_passed_as_separate_argument(tmp_path):
    write_pyproject(
        tmp_path,
        """
[tool.pytest-html-plus.profiles.local]
screenshots = "artifacts"
""".strip(),
    )

    args = apply_plus_profile_args(
        ["--plus-profile", "local", "-q"],
        start_path=tmp_path,
    )

    assert args == ["--screenshots=artifacts", "-q"]


def test_invalid_profile_key_raises_usage_error(tmp_path):
    write_pyproject(
        tmp_path,
        """
[tool.pytest-html-plus.profiles.ci]
html = "report.html"
""".strip(),
    )

    with pytest.raises(pytest.UsageError, match="Invalid key\\(s\\) in profile 'ci'"):
        apply_plus_profile_args(["--plus-profile=ci"], start_path=tmp_path)


def test_duplicate_profile_keys_surface_toml_error(tmp_path):
    write_pyproject(
        tmp_path,
        """
[tool.pytest-html-plus.profiles.ci]
json-report = "one.json"
json-report = "two.json"
""".strip(),
    )

    with pytest.raises(pytest.UsageError, match="Invalid TOML"):
        apply_plus_profile_args(["--plus-profile=ci"], start_path=tmp_path)


def test_profile_requires_pyproject_file(tmp_path):
    nested = tmp_path / "nested"
    nested.mkdir()

    with pytest.raises(pytest.UsageError, match="requires a pyproject.toml file"):
        apply_plus_profile_args(["--plus-profile=ci"], start_path=nested)


def test_profile_boolean_values_must_be_boolean(tmp_path):
    write_pyproject(
        tmp_path,
        """
[tool.pytest-html-plus.profiles.ci]
generate-xml = "yes"
""".strip(),
    )

    with pytest.raises(pytest.UsageError, match="must be true or false"):
        apply_plus_profile_args(["--plus-profile=ci"], start_path=tmp_path)
