import pytest


@pytest.mark.parametrize(
    "txt",
    [
        "<strong>admin</strong>",
        "<button>Click me</button>",
        "<img src=x>",
        "Tom & Jerry",
        '" onclick="doSomething()',
    ],
)
def test_parameter_name_contains_html(txt) -> None:
    pass
