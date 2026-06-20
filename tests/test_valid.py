from decimal import Decimal
from math import isnan
from pathlib import Path
import sys

import pytest

import tomli_w

if sys.version_info >= (3, 11):
    import tomllib as tomli
else:
    import tomli

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


def replace_nans(cont: dict | list) -> dict | list:
    """Replace NaNs with a sentinel object to fix the problem that NaN is not
    equal to another NaN."""
    for k, v in cont.items() if isinstance(cont, dict) else enumerate(cont):
        if isinstance(v, (float, Decimal)) and isnan(v):
            cont[k] = NAN
        elif isinstance(v, dict) or isinstance(v, list):
            cont[k] = replace_nans(cont[k])
    return cont


@pytest.mark.parametrize(
    "obj,expected_str,multiline_strings",
    [
        ({"cr-newline": "foo\rbar"}, 'cr-newline = "foo\\rbar"\n', True),
        # A "\r\n" must keep its carriage return: it is escaped (as a lone
        # "\r" already is above) rather than collapsed to a bare newline,
        # which would drop the "\r" on read. See test_crlf_roundtrip below.
        ({"crlf-newline": "foo\r\nbar"}, 'crlf-newline = """\nfoo\\r\nbar"""\n', True),
    ],
)
def test_obj_to_str_mapping(obj, expected_str, multiline_strings):
    assert tomli_w.dumps(obj, multiline_strings=multiline_strings) == expected_str


@pytest.mark.parametrize("multiline_strings", [False, True])
@pytest.mark.parametrize("value", ["x\r\ny", "a\r\nb\r\nc", "\r\n", "foo\r\n"])
def test_crlf_roundtrip(value, multiline_strings):
    # A carriage return must survive a dump/load round-trip in both modes;
    # previously multiline_strings=True collapsed "\r\n" to "\n" and dropped
    # the "\r".
    dumped = tomli_w.dumps({"k": value}, multiline_strings=multiline_strings)
    assert tomli.loads(dumped)["k"] == value
