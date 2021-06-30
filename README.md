[![Build Status](https://github.com/hukkin/tomli-w/workflows/Tests/badge.svg?branch=master)](https://github.com/hukkin/tomli-w/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush)
[![codecov.io](https://codecov.io/gh/hukkin/tomli-w/branch/master/graph/badge.svg)](https://codecov.io/gh/hukkin/tomli-w)
[![PyPI version](https://img.shields.io/pypi/v/tomli-w)](https://pypi.org/project/tomli-w)

# Tomli-W

> A lil' TOML writer

**Table of Contents**  *generated with [mdformat-toc](https://github.com/hukkin/mdformat-toc)*

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Intro](#intro)
- [Installation](#installation)
- [Usage](#usage)
- [FAQ](#faq)
  - [Does Tomli-W sort the document?](#does-tomli-w-sort-the-document)
  - [Does Tomli-W support writing documents with comments, custom whitespace, or other stylistic choices?](#does-tomli-w-support-writing-documents-with-comments-custom-whitespace-or-other-stylistic-choices)

<!-- mdformat-toc end -->

## Intro<a name="intro"></a>

Tomli-W is a Python library for writing [TOML](https://toml.io).
It is a write-only counterpart to [Tomli](https://github.com/hukkin/tomli),
which is a read-only TOML parser.
Tomli-W is fully compatible with [TOML v1.0.0](https://toml.io/en/v1.0.0).

## Installation<a name="installation"></a>

```bash
pip install tomli-w
```

## Usage<a name="usage"></a>

```python
import tomli_w

doc = {"table": {"nested": {}, "val3": 3}, "val2": 2, "val1": 1}
expected_toml = """\
val2 = 2
val1 = 1

[table]
val3 = 3

[table.nested]
"""
assert tomli_w.dumps(doc) == expected_toml
```

## FAQ<a name="faq"></a>

### Does Tomli-W sort the document?<a name="does-tomli-w-sort-the-document"></a>

No, but it respects sort order of the input data,
so one could sort the content of the `dict` (recursively) before calling `tomli_w.dumps`.

### Does Tomli-W support writing documents with comments, custom whitespace, or other stylistic choices?<a name="does-tomli-w-support-writing-documents-with-comments-custom-whitespace-or-other-stylistic-choices"></a>

No.
