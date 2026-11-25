from decimal import Decimal, localcontext

import pytest

import tomli_w


@pytest.mark.parametrize(
    "value,expected",
    [
        ("1.234567890123456789", "1.234567890123456789"),
        ("-0", "-0.0"),
        ("1E+1000", "1e+1000"),
    ],
)
def test_decimal_ignores_context_precision(value, expected):
    number = Decimal(value)
    with localcontext() as context:
        context.prec = 2
        actual = tomli_w.dumps({"value": number})
    assert actual == f"value = {expected}\n"


def test_decimal():
    obj = {
        "decimal-0": Decimal("0"),
        "decimal-4": Decimal("4"),
        "decimal-pi": Decimal("3.14159"),
        "decimal-inf": Decimal("inf"),
        "decimal-minus-inf": Decimal("-inf"),
        "decimal-nan": Decimal("nan"),
        "decimal-2e3": Decimal("2e3"),
        "decimal-2E3": Decimal("2E3"),
        "float-2E16": float("2E16"),
    }
    assert (
        tomli_w.dumps(obj)
        == """\
decimal-0 = 0.0
decimal-4 = 4.0
decimal-pi = 3.14159
decimal-inf = inf
decimal-minus-inf = -inf
decimal-nan = nan
decimal-2e3 = 2e+3
decimal-2E3 = 2e+3
float-2E16 = 2e+16
"""
    )


def test_tuple():
    obj = {"empty-tuple": (), "non-empty-tuple": (1, (2, 3))}
    assert (
        tomli_w.dumps(obj)
        == """\
empty-tuple = []
non-empty-tuple = [
    1,
    [
        2,
        3,
    ],
]
"""
    )
