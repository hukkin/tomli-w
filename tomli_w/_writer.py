from collections.abc import Sequence
from datetime import date, datetime, time
from decimal import Decimal
import string
from types import MappingProxyType
from typing import Any, BinaryIO, Dict, Generator, List, Mapping, NamedTuple, Tuple

ASCII_CTRL = frozenset(chr(i) for i in range(32)) | frozenset(chr(127))
ILLEGAL_BASIC_STR_CHARS = frozenset('"\\') | ASCII_CTRL - frozenset("\t")
BARE_KEY_CHARS = frozenset(string.ascii_letters + string.digits + "-_")
ARRAY_INDENT = " " * 4
LONG_LINE_HEURISTIC = 100

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


def dump(obj: Dict[str, Any], fp: BinaryIO, *, multiline_strings: bool = False) -> None:
    opts = Opts(multiline_strings)
    for chunk in gen_table_chunks(obj, opts, name=""):
        fp.write(chunk.encode())


def dumps(obj: Dict[str, Any], *, multiline_strings: bool = False) -> str:
    opts = Opts(multiline_strings)
    return "".join(gen_table_chunks(obj, opts, name=""))


class Opts(NamedTuple):
    allow_multiline: bool


def gen_table_chunks(
    table: Mapping[str, Any],
    opts: Opts,
    *,
    name: str,
    inside_aot: bool = False,
) -> Generator[str, None, None]:
    yielded = False
    literals = []
    tables: List[Tuple[str, Any, bool]] = []  # => [(key, value, inside_aot)]
    for k, v in table.items():
        if isinstance(v, dict):
            tables.append((k, v, False))
        elif is_aot(v) and not all(is_suitable_inline_table(k, t) for t in v):
            tables.extend((k, t, True) for t in v)
        else:
            literals.append((k, v))

    if name and (literals or not tables):
        yielded = True
        yield (f"[[{name}]]\n" if inside_aot else f"[{name}]\n")

    if literals:
        yielded = True
        for k, v in literals:
            yield f"{format_key_part(k)} = {format_literal(v, opts)}\n"

    for k, v, in_aot in tables:
        if yielded:
            yield "\n"
        else:
            yielded = True
        key_part = format_key_part(k)
        display_name = f"{name}.{key_part}" if name else key_part
        yield from gen_table_chunks(v, opts, name=display_name, inside_aot=in_aot)


def format_literal(obj: object, opts: Opts, *, nest_level: int = 0) -> str:
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, (int, float, Decimal, date, datetime)):
        return str(obj)
    if isinstance(obj, time):
        if obj.tzinfo:
            raise ValueError("TOML does not support offset times")
        return str(obj)
    if isinstance(obj, str):
        return format_string(obj, allow_multiline=opts.allow_multiline)
    if isinstance(obj, list):
        if not obj:
            return "[]"
        item_indent = ARRAY_INDENT * (1 + nest_level)
        closing_bracket_indent = ARRAY_INDENT * nest_level
        return (
            "[\n"
            + ",\n".join(
                item_indent + format_literal(item, opts, nest_level=nest_level + 1)
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
                f"{format_key_part(k)} = {format_literal(v, opts)}"
                for k, v in obj.items()
            )
            + " }"
        )
    raise TypeError(f"Object of type {type(obj)} is not TOML serializable")


def format_key_part(part: str) -> str:
    if part and BARE_KEY_CHARS.issuperset(part):
        return part
    return format_string(part, allow_multiline=False)


def format_string(s: str, *, allow_multiline: bool) -> str:
    do_multiline = allow_multiline and "\n" in s
    if do_multiline:
        result = '"""\n'
        s = s.replace("\r\n", "\n")
    else:
        result = '"'

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


def is_aot(obj: Any) -> bool:
    """Decides if object behaves as an array of tables (i.e. list of dicts).

    See: https://toml.io/en/v1.0.0#array-of-tables.
    """
    return isinstance(obj, Sequence) and all(isinstance(v, dict) for v in obj)


def is_suitable_inline_table(name: str, obj: dict) -> bool:
    """Uses heuristics to decide if the inline-style representation is a good
    choice for a given dict.

    For example, the spec strongly discourages inline tables that
    contain line breaks. See: https://toml.io/en/v1.0.0#inline-table
    """
    if any(isinstance(v, (list, tuple)) for v in obj.values()):
        # tomli-w will automatically introduce line breaks when converting lists
        return False
    # In the following line we use `repr(obj)` as an approximation for the
    # TOML representation of an inline-table when `obj` is a dict,
    # (for the purposes of roughly estimating the line length)
    return len(f"{name} = {obj!r}") < LONG_LINE_HEURISTIC
