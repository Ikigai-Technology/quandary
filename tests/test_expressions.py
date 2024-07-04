# ruff: noqa: S101
import pytest
from quandary import compiler


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("measurements.weight / measurements.height", pytest.approx(54.91329)),
        ("(measurements.height * measurements.height)", pytest.approx(2.9929)),
        ("(measurements.height * measurements.height) / measurements.weight", pytest.approx(0.0315042)),
        ("measurements.weight / (measurements.height * measurements.height)", pytest.approx(31.74178)),
        ("measurements.weight / (measurements.height / 100) ^ 2", pytest.approx(317417.8)),
        # Legacy power operator
        ("measurements.weight / (measurements.height / 100) ** 2", pytest.approx(317417.8)),
    ],
)
def test_expression(expr, expected):
    scope = {
        "measurements": {
            "weight": 95.0,
            "height": 1.73,
        }
    }

    code = compiler.parse(expr)
    result = code(scope)

    assert result == expected
