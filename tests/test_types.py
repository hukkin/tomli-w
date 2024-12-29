from decimal import Decimal

import tomli_w


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
decimal-2e3 = 2E+3
decimal-2E3 = 2E+3
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
