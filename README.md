[![Build Status](https://github.com/hukkin/tomli-dumps/workflows/Tests/badge.svg?branch=master)](https://github.com/hukkin/tomli-dumps/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush)
[![codecov.io](https://codecov.io/gh/hukkin/tomli-dumps/branch/master/graph/badge.svg)](https://codecov.io/gh/hukkin/tomli-dumps)
[![PyPI version](https://img.shields.io/pypi/v/tomli-dumps)](https://pypi.org/project/tomli-dumps)

# Tomli dumps

> A lil' TOML writer

**Table of Contents**  *generated with [mdformat-toc](https://github.com/hukkin/mdformat-toc)*

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Intro](#intro)
- [Installation](#installation)
- [Usage](#usage)
- [FAQ](#faq)
  - [Does Tomli dumps sort the document?](#does-tomli-dumps-sort-the-document)
  - [Does Tomli dumps support writing documents with comments, custom whitespace, or other stylistic choices?](#does-tomli-dumps-support-writing-documents-with-comments-custom-whitespace-or-other-stylistic-choices)

<!-- mdformat-toc end -->

## Intro<a name="intro"></a>

_Tomli dumps_ is a Python library for writing [TOML](https://toml.io).
It is a write-only counterpart to [Tomli](https://github.com/hukkin/tomli),
which is a read-only TOML parser.
_Tomli dumps_ is fully compatible with [TOML v1.0.0](https://toml.io/en/v1.0.0).

## Installation<a name="installation"></a>

```bash
pip install tomli-dumps
```

## Usage<a name="usage"></a>

```python
import tomli_dumps

doc = {"table": {"nested": {}, "val3": 3}, "val2": 2, "val1": 1}
expected_toml = """\
val2 = 2
val1 = 1

[table]
val3 = 3

[table.nested]
"""
assert tomli_dumps.dumps(doc) == expected_toml
```

## FAQ<a name="faq"></a>

### Does _Tomli dumps_ sort the document?<a name="does-tomli-dumps-sort-the-document"></a>

No, but it respects sort order of the input data,
so one could sort the content of the `dict` (recursively) before calling `tomli_dumps.dumps`.

### Does _Tomli dumps_ support writing documents with comments, custom whitespace, or other stylistic choices?<a name="does-tomli-dumps-support-writing-documents-with-comments-custom-whitespace-or-other-stylistic-choices"></a>

No.
