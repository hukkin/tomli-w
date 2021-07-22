from decimal import Decimal
from math import isnan
from pathlib import Path
from typing import Union

import pytest
import tomli

import tomli_w

COMPLIANCE_DIR = Path(__file__).parent / "data" / "toml-lang-compliance" / "valid"
EXTRAS_DIR = Path(__file__).parent / "data" / "extras" / "valid"

VALID_FILES = tuple(COMPLIANCE_DIR.glob("**/*.toml")) + tuple(
    EXTRAS_DIR.glob("**/*.toml")
)


@pytest.mark.parametrize(
    "valid",
    VALID_FILES,
    ids=[p.stem for p in VALID_FILES],
)
def test_valid(valid):
    if valid.stem in {"qa-array-inline-nested-1000", "qa-table-inline-nested-1000"}:
        pytest.xfail("This much recursion is not supported")
    original_str = valid.read_bytes().decode()
    original_data = tomli.loads(original_str)
    dump_str = tomli_w.dumps(original_data)
    after_dump_data = tomli.loads(dump_str)
    assert replace_nans(after_dump_data) == replace_nans(original_data)


NAN = object()


def replace_nans(cont: Union[dict, list]) -> Union[dict, list]:
    """Replace NaNs with a sentinel object to fix the problem that NaN is not
    equal to another NaN."""
    for k, v in cont.items() if isinstance(cont, dict) else enumerate(cont):
        if isinstance(v, (float, Decimal)) and isnan(v):
            cont[k] = NAN
        elif isinstance(v, dict) or isinstance(v, list):
            cont[k] = replace_nans(cont[k])
    return cont
