import pytest

import tomli_dumps


def test_invalid_type_nested():
    with pytest.raises(TypeError):
        tomli_dumps.dumps({"bytearr": bytearray()})
