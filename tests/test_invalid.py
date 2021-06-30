from datetime import time, timezone

import pytest

import tomli_w


def test_invalid_type_nested():
    with pytest.raises(TypeError):
        tomli_w.dumps({"bytearr": bytearray()})


def test_invalid_time():
    offset_time = time(23, 59, 59, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        tomli_w.dumps({"offset time": offset_time})
