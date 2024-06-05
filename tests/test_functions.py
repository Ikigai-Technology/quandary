# ruff: noqa: S101
import pytest
from quandary import Scope, compiler


@pytest.mark.parametrize(
    "program, state, expected",
    [
        ["""abs(-5)""", Scope(functions={"abs": abs}), 5],
        [
            """join(a, "two")""",
            Scope(
                {"a": "one"},
                {"join": lambda *args: " ".join(str(a) for a in args)},
            ),
            "one two",
        ],
        # Support expressions as arguments
        ["""abs(2 * -3)""", Scope(functions={"abs": abs}), 6],
        # Functions with no arguments
        ["""int()""", Scope(functions={"int": int}), 0],
        # Functions being passed lists
        ["""sum([1, 2, 3])""", Scope(functions={"sum": sum}), 6],
    ],
)
def test_functions(program, state, expected):
    code = compiler.parse(program)

    result = code(state)

    assert result == expected
