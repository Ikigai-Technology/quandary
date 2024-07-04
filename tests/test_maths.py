# ruff: noqa: S101
import pytest
from quandary import compiler


@pytest.mark.parametrize(
    "expr, scope, expected",
    [
        ("1 + 1.0", {}, 2.0),
        ("1 * 2", {}, 2),
        ("12 / 3", {}, 4),
        ("2 + 3 * 6 - 5", {}, 15),
        ("2 + 3 * (6 - 5)", {}, 5),
        ("(2 + 3) - 5", {}, 0),
        ("(2 + 3) * 6 - 5", {}, 25),
        ("2 ^ 3", {}, 8),
    ],
)
def test_maths(expr, scope, expected):
    code = compiler.parse(expr)

    result = code(scope)

    assert result == expected
