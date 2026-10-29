from pathlib import Path

import pytest

from tests.unit.conftest import make_test_result


@pytest.mark.parametrize(
    "value",
    range(8),
    ids=[
        'label="large"',
        "<em>important</em>",
        "<strong>admin</strong>",
        "<button>Click me</button>",
        "<img src=x>",
        "Tom & Jerry",
        '" onclick="doSomething()',
        "</strong><div>unexpected</div>",
    ],
)
def test_parameter_name_contains_html(value):
    assert value in range(8)


def test_parameterized_test_name_is_escaped_in_html(reporter_factory):
    test_name = 'test_example[label="<em>INJECTED</em>"]'
    reporter = reporter_factory(
        results=[
            make_test_result(
                nodeid="tests/test_example.py::test_example",
                test=test_name,
                status="passed",
            )
        ]
    )

    reporter.generate_html_report()

    html = Path(reporter.output_dir, "report.html").read_text(encoding="utf-8")
    escaped_name = "test_example[label=&quot;&lt;em&gt;INJECTED&lt;/em&gt;&quot;]"
    assert f'data-name="{escaped_name}"' in html
    assert f"<strong>{escaped_name}</strong>" in html
