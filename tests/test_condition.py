# ruff: noqa: S101
import pytest
from quandary import compiler


@pytest.mark.parametrize(
    "program, state, expected",
    [
        ["""(TRUE?1:0)""", {}, 1],
        ["""(FALSE?1:0)""", {}, 0],
        ["""(x = 1 ? 10 : x = 2 ? 100 : 1)""", {"x":1}, 10],
        ["""(x = 1 ? 10 : x = 2 ? 100 : 1)""", {"x":2}, 100],
        ["""(x = 1 ? 10 : x = 2 ? 100 : 1)""", {"x":3}, 1],
        ["""(x = 1 ? 10 : x = 2 ? 100 : x = 3 ? 1000 : 1)""", {"x":1}, 10],
        ["""(x = 1 ? 10 : x = 2 ? 100 : x = 3 ? 1000 : 1)""", {"x":2}, 100],
        ["""(x = 1 ? 10 : x = 2 ? 100 : x = 3 ? 1000 : 1)""", {"x":3}, 1000],
        ["""(x = 1 ? 10 : x = 2 ? 100 : x = 3 ? 1000 : 1)""", {"x":4}, 1],
        ["""(x = 1 ? 10 : x = 2 ? 100 : x = 3 ? 1000 : 1)""", {"x":0}, 1],
        ["""(x=1?10:x=2?100:1)""", {"x":0}, 1],
        ["""(TRUE?x+1:1)""", {"x":1}, 2],
        ["""(FALSE?x+1:1)""", {"x":1}, 1],
    ],
)
def test_condition(program, state, expected):
    code = compiler.parse(program)

    result = code(state)

    assert result == expected
