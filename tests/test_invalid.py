from datetime import time, timezone

import pytest

import tomli_w


def test_invalid_type_nested():
    with pytest.raises(TypeError) as exc_info:
        tomli_w.dumps({"bytearr": bytearray()})
    assert str(exc_info.value) == "Object of type 'bytearray' is not TOML serializable"


def test_invalid_time():
    offset_time = time(23, 59, 59, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        tomli_w.dumps({"offset time": offset_time})


def test_negative_indent():
    with pytest.raises(ValueError):
        tomli_w.dumps({"k": "v"}, indent=-1)


def test_invalid_key__falsy():
    with pytest.raises(TypeError) as exc_info:
        tomli_w.dumps({None: "v"})  # type: ignore[dict-item]
    assert (
        str(exc_info.value)
        == "Invalid mapping key 'None' of type 'NoneType'. A string is required."
    )


def test_invalid_key__truthy():
    with pytest.raises(TypeError) as exc_info:
        tomli_w.dumps({2: "v"})  # type: ignore[dict-item]
    assert (
        str(exc_info.value)
        == "Invalid mapping key '2' of type 'int'. A string is required."
    )
