# ruff: noqa: S101
import pytest
from quandary import compiler


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
        # TODO: Power precedence
        ("x * 2 ** 2", {"x": 5}, 20),
        ("x ** 3 / x ** 2", {"x": 5}, 5),
    ],
)
def test_basic(program, state, expected):
    code = compiler.parse(program)

    result = code(state)

    assert result == expected
