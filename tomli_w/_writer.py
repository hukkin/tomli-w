from datetime import date, datetime, time
from decimal import Decimal
import string
from types import MappingProxyType
from typing import Any, Dict, Generator, TextIO

# Strings this long or longer that contain line breaks will be formatted
# as multiline strings
MULTILINE_STR_THRESHOLD = 70

ASCII_CTRL = frozenset(chr(i) for i in range(32)) | frozenset(chr(127))
ILLEGAL_BASIC_STR_CHARS = frozenset('"\\') | ASCII_CTRL - frozenset("\t")
BARE_KEY_CHARS = frozenset(string.ascii_letters + string.digits + "-_")
ARRAY_INDENT = " " * 4

COMPACT_ESCAPES = MappingProxyType(
    {
        "\u0008": "\\b",  # backspace
        "\u000A": "\\n",  # linefeed
        "\u000C": "\\f",  # form feed
        "\u000D": "\\r",  # carriage return
        "\u0022": '\\"',  # quote
        "\u005C": "\\\\",  # backslash
    }
)


def dump(obj: Dict[str, Any], fp: TextIO) -> None:
    for chunk in gen_table_chunks(obj, name=""):
        fp.write(chunk)


def dumps(obj: Dict[str, Any]) -> str:
    return "".join(gen_table_chunks(obj, name=""))


def gen_table_chunks(table: Dict[str, Any], *, name: str) -> Generator[str, None, None]:
    yielded = False
    literals = []
    tables = []
    for k, v in table.items():
        if isinstance(v, dict):
            tables.append((k, v))
        else:
            literals.append((k, v))

    if name and (literals or not tables):
        yielded = True
        yield f"[{name}]\n"

    if literals:
        yielded = True
        for k, v in literals:
            yield f"{format_key_part(k)} = {format_literal(v)}\n"

    for k, v in tables:
        if yielded:
            yield "\n"
        else:
            yielded = True
        yield from gen_table_chunks(
            v, name=name + "." + format_key_part(k) if name else format_key_part(k)
        )


def format_literal(obj: object, *, nest_level: int = 0) -> str:
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, (int, float, Decimal, date, datetime)):
        return str(obj)
    if isinstance(obj, time):
        if obj.tzinfo:
            raise ValueError("TOML does not support offset times")
        return str(obj)
    if isinstance(obj, str):
        return format_string(obj, allow_multiline=True)
    if isinstance(obj, list):
        if not obj:
            return "[]"
        item_indent = ARRAY_INDENT * (1 + nest_level)
        closing_bracket_indent = ARRAY_INDENT * nest_level
        return (
            "[\n"
            + ",\n".join(
                item_indent + format_literal(item, nest_level=nest_level + 1)
                for item in obj
            )
            + f",\n{closing_bracket_indent}]"
        )
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        return (
            "{ "
            + ", ".join(
                f"{format_key_part(k)} = {format_literal(v)}" for k, v in obj.items()
            )
            + " }"
        )
    raise TypeError(f"Object of type {type(obj)} is not TOML serializable")


def format_key_part(part: str) -> str:
    if part and BARE_KEY_CHARS.issuperset(part):
        return part
    return format_string(part, allow_multiline=False)


def format_string(s: str, *, allow_multiline: bool = False) -> str:
    result = '"'

    # If there are line breaks and the string is longer than threshold,
    # make a multiline string instead.
    do_multiline = allow_multiline and "\n" in s and len(s) >= MULTILINE_STR_THRESHOLD
    if do_multiline:
        result += '""\n'
        s = s.replace("\r\n", "\n")

    pos = seq_start = 0
    while True:
        try:
            char = s[pos]
        except IndexError:
            result += s[seq_start:pos]
            if do_multiline:
                return result + '"""'
            return result + '"'
        if char in ILLEGAL_BASIC_STR_CHARS:
            result += s[seq_start:pos]
            if char in COMPACT_ESCAPES:
                if do_multiline and char == "\n":
                    result += "\n"
                else:
                    result += COMPACT_ESCAPES[char]
            else:
                result += "\\u" + hex(ord(char))[2:].rjust(4, "0")
            seq_start = pos + 1
        pos += 1
