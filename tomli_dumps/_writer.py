from datetime import date, datetime, time
from decimal import Decimal
import string
from types import MappingProxyType
from typing import Any, Dict, TextIO

ASCII_CTRL = frozenset(chr(i) for i in range(32)) | frozenset(chr(127))
ILLEGAL_BASIC_STR_CHARS = frozenset('"\\') | ASCII_CTRL - frozenset("\t")
BARE_KEY_CHARS = frozenset(string.ascii_letters + string.digits + "-_")

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
    raise NotImplementedError


def dumps(obj: Dict[str, Any]) -> str:
    return write_table(obj, name="")


def write_table(table: Dict[str, Any], *, name: str) -> str:
    literals = []
    tables = []
    for k, v in table.items():
        if isinstance(v, dict):
            tables.append((k, v))
        else:
            literals.append((k, v))

    output = ""

    if name and (literals or not tables):
        output += f"[{name}]\n"

    for k, v in literals:
        output += f"{format_key_part(k)} = {write_literal(v)}\n"

    for k, v in tables:
        if output:
            output += "\n"
        output += write_table(
            v, name=name + "." + format_key_part(k) if name else format_key_part(k)
        )

    return output


def write_literal(obj: object, *, nest_level: int = 0) -> str:
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, (int, float, Decimal, time, date, datetime)):
        return str(obj)
    if isinstance(obj, str):
        return format_string(obj, allow_multiline=False)
    if isinstance(obj, list):
        if not obj:
            return "[]"
        lst_str = "[\n"
        for item in obj:
            lst_str += (
                "    " * (1 + nest_level)
                + write_literal(item, nest_level=nest_level + 1)
                + ",\n"
            )
        return lst_str + "    " * nest_level + "]"
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        dct_str = "{ "
        for k, v in obj.items():
            dct_str += f"{format_key_part(k)} = {write_literal(v)}, "
        dct_str = dct_str[:-2] + " }"
        return dct_str
    raise TypeError(f"Object of type {type(obj)} is not TOML serializable")


def format_key_part(part: str) -> str:
    if part and BARE_KEY_CHARS.issuperset(part):
        return part
    return format_string(part, allow_multiline=False)


def format_string(s: str, *, allow_multiline: bool = False) -> str:
    if allow_multiline:
        # TODO: If there are line breaks, make a multiline string.
        #       Make sure this is not used for keys.
        raise NotImplementedError
    result = '"'
    pos = seq_start = 0
    while True:
        try:
            char = s[pos]
        except IndexError:
            return result + s[seq_start:pos] + '"'
        if char in ILLEGAL_BASIC_STR_CHARS:
            result += s[seq_start:pos]
            if char in COMPACT_ESCAPES:
                result += COMPACT_ESCAPES[char]
            else:
                result += "\\u" + hex(ord(char))[2:].rjust(4, "0")
            seq_start = pos + 1
        pos += 1
