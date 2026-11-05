import io
from typing import IO, cast

import pytest

import tomli_w


def test_dump(tmp_path):
    toml_obj = {"testing": "test\ntest"}
    path = tmp_path / "test.toml"
    with open(path, "wb") as f:
        tomli_w.dump(toml_obj, f)
    assert path.read_bytes().decode() == 'testing = "test\\ntest"\n'


class ShortWriter(io.RawIOBase):
    """Control raw write progress without file metadata required by typing.IO."""

    def __init__(self, limit):
        super().__init__()
        self.limit = limit
        self.data = bytearray()
        self.flushed = False

    def writable(self):
        return True

    def write(self, data):
        if self.limit is None:
            return None
        count = min(self.limit, len(data))
        self.data.extend(data[:count])
        return count

    def flush(self):
        self.flushed = True


@pytest.mark.parametrize("limit", [1, 5, 1000])
def test_dump_completes_binary_writes(limit):
    class BytesOnlyWriter(ShortWriter):
        def write(self, data):
            assert isinstance(data, bytes)
            return super().write(data)

    doc = {"a": 1234, "nested": {"unicode": "é", "values": [1, 2]}}
    stream = BytesOnlyWriter(limit)

    tomli_w.dump(doc, cast(IO[bytes], stream))

    assert bytes(stream.data) == tomli_w.dumps(doc).encode()
    assert not stream.closed
    assert not stream.flushed


@pytest.mark.parametrize("limit", [0, None])
def test_dump_rejects_writes_without_progress(limit):
    stream = ShortWriter(limit)

    with pytest.raises(OSError):
        tomli_w.dump({"a": 1234}, cast(IO[bytes], stream))

    assert not stream.closed
    assert not stream.flushed


@pytest.mark.parametrize("error_type", [OSError, BlockingIOError])
def test_dump_preserves_write_errors_after_a_short_write(error_type):
    failure = error_type("synthetic write failure")

    class FailingWriter(ShortWriter):
        def write(self, data):
            if self.data:
                raise failure
            return super().write(data)

    stream = FailingWriter(5)
    with pytest.raises(error_type) as caught:
        tomli_w.dump({"a": 1234}, cast(IO[bytes], stream))

    assert caught.value is failure
    assert bytes(stream.data) == b"a = 1"
    assert not stream.closed
    assert not stream.flushed


def test_dump_buffered_short_writer():
    doc = {"a": 1234}
    raw = ShortWriter(5)
    with io.BufferedWriter(raw) as stream:
        tomli_w.dump(doc, stream)
        stream.flush()
        assert bytes(raw.data) == tomli_w.dumps(doc).encode()
        assert not stream.closed
