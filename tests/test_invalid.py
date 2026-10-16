from datetime import time, timedelta, timezone, tzinfo

import pytest

import tomli_w


class NoOffsetTzinfo(tzinfo):
    def utcoffset(self, dt):
        return None

    def dst(self, dt):
        return None

    def tzname(self, dt):
        return None


class FalseyOffsetTzinfo(tzinfo):
    def __bool__(self):
        return False

    def utcoffset(self, dt):
        return timedelta(hours=1)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "test"


def test_invalid_type_nested():
    with pytest.raises(TypeError) as exc_info:
        tomli_w.dumps({"bytearr": bytearray()})
    assert str(exc_info.value) == "Object of type 'bytearray' is not TOML serializable"


def test_invalid_time():
    offset_time = time(23, 59, 59, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        tomli_w.dumps({"offset time": offset_time})


def test_time_with_tzinfo_without_offset():
    local_time = time(12, 34, 56, tzinfo=NoOffsetTzinfo())
    assert tomli_w.dumps({"local time": local_time}) == '"local time" = 12:34:56\n'


def test_falsey_offset_time_is_rejected():
    offset_time = time(12, 34, 56, tzinfo=FalseyOffsetTzinfo())
    with pytest.raises(ValueError, match="TOML does not support offset times"):
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
