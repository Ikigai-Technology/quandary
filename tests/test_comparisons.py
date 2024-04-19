# ruff: noqa: S101
import pytest
from quandary import compiler

COMPARISON_VALUES = [
    (0, 0),
    (0, 1),
    (1, 0),
    (1, 1),
]


@pytest.mark.parametrize(
    "op, results",
    [
        ["<", [False, True, False, False]],
        ["<=", [True, True, False, True]],
        ["=", [True, False, False, True]],
        ["<>", [False, True, True, False]],
        [">=", [True, False, True, True]],
        [">", [False, False, True]],
    ],
)
def test_comparison(op, results):
    code = compiler.parse(f"left {op} right")

    for (left, right), expected in zip(COMPARISON_VALUES, results):
        result = code({"left": left, "right": right})
        assert result == expected, (left, right)


def test_in():
    code = compiler.parse("a in b")

    result = code({"a": 6, "b": [2, 4, 6]})

    assert result

    result = code({"a": 6, "b": [1, 2, 3]})

    assert not result
