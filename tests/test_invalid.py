from datetime import datetime, time, timedelta, timezone

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


def test_invalid_datetime_offset():
    # TOML offsets are RFC 3339 `HH:MM`; a datetime whose UTC offset has a
    # seconds or microseconds component would be written as unparsable TOML.
    sub_minute_offset = timezone(timedelta(seconds=30))
    with pytest.raises(ValueError):
        tomli_w.dumps({"dt": datetime(2020, 1, 1, tzinfo=sub_minute_offset)})
    sub_second_offset = timezone(timedelta(microseconds=1))
    with pytest.raises(ValueError):
        tomli_w.dumps({"dt": datetime(2020, 1, 1, tzinfo=sub_second_offset)})


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
