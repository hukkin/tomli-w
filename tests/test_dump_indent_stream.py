from io import BytesIO
import sys

import pytest

import tomli_w

if sys.version_info >= (3, 11):
    import tomllib as tomli
else:
    import tomli


class RecordingStream(BytesIO):
    def __init__(self, initial_bytes):
        super().__init__(initial_bytes)
        self.write_calls = 0

    def write(self, data):
        self.write_calls += 1
        return super().write(data)


@pytest.mark.parametrize("indent", [True, False, 1.5, None])
def test_invalid_indent_leaves_stream_untouched(indent):
    with RecordingStream(b"previous output\n") as stream:
        stream.seek(3)
        before = stream.getvalue(), stream.tell()
        with pytest.raises(TypeError):
            tomli_w.dump({"answer": 42}, stream, indent=indent)
        assert stream.write_calls == 0
        assert (stream.getvalue(), stream.tell()) == before


@pytest.mark.parametrize("indent", [0, 2])
def test_valid_indent_stream_round_trip(indent):
    data = {"items": [1, 2, 3], "nested": {"enabled": True}}
    with BytesIO() as stream:
        tomli_w.dump(data, stream, indent=indent)
        output = stream.getvalue()
        assert tomli.loads(output.decode()) == data
        assert stream.tell() == len(output)
