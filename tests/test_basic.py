# ruff: noqa: S101
import pytest
from quandary import Scope, compiler


@pytest.mark.parametrize(
    "program, state, expected",
    [
        ["""a = TRUE""", {"a": False}, False],
        ["""a = TRUE or a = FALSE""", {"a": 1}, True],
        ["""a or b""", {}, None],
        ["""a = 1 and b = 2""", {}, False],
        ["""a = 1 and not b = 2""", {"a": 1, "b": 2}, False],
        ["""(a = 1 or a = 2) and b = 2""", {}, False],
        ["""5 + 6.0""", {}, 11.0],
        ["""-5 + 6.0""", {}, 1.0],
        ["""6.0 + -5""", {}, 1.0],
        ["""1 < 2""", {}, True],
        ["""1 > 2""", {}, False],
        ["""a = 5""", {"a": 5}, True],
        ["""a * 6""", {"a": 5}, 30],
        ["""a > 5 and a < 7""", {"a": 6}, True],
        ["""a > 5 and a < 7""", {"a": 5}, False],
        ["""a.b = TRUE""", {}, False],
        ["""a.b = TRUE""", {"a": {}}, False],
        ["""a.b = TRUE""", {"a": {"b": True}}, True],
        # Lookups on non-dicts should not explode
        ["""a.b = 1""", {"a": False}, False],
        # Strings
        ['''"test"''', {}, "test"],
        # Don't need to escape single quotes
        ['''"te'st"''', {}, "te'st"],
        # Do need to escape double quotes
        [r'''"te\"st"''', {}, 'te"st'],
        ['''"test" = "test"''', {}, True],
        [
            '''(a = "test" or b = "test") and c = "bar"''',
            {
                "a": "foo",
                "b": "test",
                "c": "bar",
            },
            True,
        ],
    ],
)
def test_basic(program, state, expected):
    # code = compiler.parse(program)
    tree = compiler.grammar.parse(program)

    print(tree)

    code = compiler.visit(tree)

    result = code(state)

    assert result == expected


COMPARISON_VALUES = [
    (0, 1),
    (1, 1),
    (1, 0),
]


@pytest.mark.parametrize(
    "op, results",
    [
        ["<", [True, False, False]],
        ["<=", [True, True, False]],
        ["=", [False, True, False]],
        ["<>", [True, False, True]],
        [">=", [False, True, True]],
        [">", [False, False, True]],
    ],
)
def test_comparison(op, results):
    code = compiler.parse(f"left {op} right")

    for (left, right), expected in zip(COMPARISON_VALUES, results):
        result = code(
            {
                "left": left,
                "right": right,
            }
        )
        assert result == expected


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
        ("2 ** 3", {}, 8),
    ],
)
def test_maths(expr, scope, expected):
    code = compiler.parse(expr)

    result = code(scope)

    assert result == expected


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
    ],
)
def test_functions(program, state, expected):
    code = compiler.parse(program)

    result = code(state)

    assert result == expected


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("measurements.weight / measurements.height", pytest.approx(54.91329)),
        ("(measurements.height * measurements.height)", pytest.approx(2.9929)),
        ("(measurements.height * measurements.height) / measurements.weight", pytest.approx(0.0315042)),
        ("measurements.weight / (measurements.height * measurements.height)", pytest.approx(31.74178)),
        ("measurements.weight / (measurements.height / 100 ** 2)", pytest.approx(317417.8)),
    ],
)
def test_expression(expr, expected):
    scope = Scope(
        {
            "measurements": {
                "weight": 95.0,
                "height": 1.73,
            }
        }
    )

    code = compiler.parse(expr)
    result = code(scope)

    assert result == expected
