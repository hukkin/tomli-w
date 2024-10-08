# Changelog

## 1.1.0

- Removed
  - Support for Python 3.7 and 3.8
- Added
  - Accept generic `collections.abc.Mapping`, not just `dict`, as input.
    Thank you [Watal M. Iwasaki](https://github.com/heavywatal) for the
    [PR](https://github.com/hukkin/tomli-w/pull/46).
  - `indent` keyword argument for customizing indent width of arrays.
    Thank you [Wim Jeantine-Glenn](https://github.com/wimglenn) for the
    [PR](https://github.com/hukkin/tomli-w/pull/49).
- Type annotations
  - Type annotate `dump` function's output stream object as `typing.IO[bytes]` (previously `typing.BinaryIO`)

## 1.0.0

- Removed
  - Support for Python 3.6
  - Positional arguments of `dump` and `dumps` can no longer be passed by keyword.
- Changed
  - Revised logic for when the "Array of Tables" syntax will be used.
    AoT syntax is used when at least one of the tables needs multiple lines, or a single line wider than 100 chars, when rendered inline.
    A nested structure no longer alone triggers the AoT syntax.

## 0.4.0

- Added
  - Support for formatting Python `tuple`s as TOML arrays.
- Fixed
  - Formatting of `decimal.Decimal("inf")`, `decimal.Decimal("-inf")` and `decimal.Decimal("nan")`.
- Changed
  - A list of dicts is now rendered using the "Array of Tables" syntax
    if at least one of the tables is a nested structure,
    or at least one of the tables would need a line wider than 100 chars when rendered inline.
    Thank you [Anderson Bravalheri](https://github.com/abravalheri) for the
    [PR](https://github.com/hukkin/tomli-w/pull/15).

## 0.3.0

- Changed
  - `dump` now supports binary file objects instead of text file objects

## 0.2.2

- Added
  - `multiline_strings` keyword argument for enabling multi-line strings
- Changed
  - Style: Do not make multi-line strings by default because they don't support lossless round-tripping

## 0.2.1

- Changed
  - Style: Decide between multi-line and single line string solely based on if line breaks are present

## 0.2.0

- Added
  - `tomli_w.dump`
- Changed
  - Style: Format strings containing line breaks and that are longer than threshold value as multiline strings

## 0.1.0

- Added
  - `tomli_w.dumps`
