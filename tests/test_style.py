import tomli_w


def test_newline_before_table():
    actual = tomli_w.dumps({"table": {}})
    expected = "[table]\n"
    assert actual == expected

    actual = tomli_w.dumps({"table": {"nested": {}, "val3": 3}, "val2": 2, "val1": 1})
    expected = """\
val2 = 2
val1 = 1

[table]
val3 = 3

[table.nested]
"""
    assert actual == expected


def test_empty_doc():
    assert tomli_w.dumps({}) == ""


def test_dont_write_redundant_tables():
    actual = tomli_w.dumps({"tab1": {"tab2": {"tab3": {}}}})
    expected = "[tab1.tab2.tab3]\n"
    assert actual == expected


def test_multiline():
    multiline_string = (
        "This is longer than threshold!\n"
        "Should be formatted as a multiline basic string"
    )
    actual = tomli_w.dumps({"ml_string": multiline_string}, multiline_strings=True)
    expected = '''\
ml_string = """
This is longer than threshold!
Should be formatted as a multiline basic string"""
'''
    assert actual == expected


def test_only_tables():
    actual = tomli_w.dumps({"tab1": {}, "tab2": {}})
    expected = """\
[tab1]

[tab2]
"""
    assert actual == expected


def test_tricky_keys():
    actual = tomli_w.dumps({"f": 1, "tab1": {}, "": {"f": 2, "": {"": 1}}, "tab3": {}})
    expected = """\
f = 1

[tab1]

[""]
f = 2

["".""]
"" = 1

[tab3]
"""
    assert actual == expected


def test_nested_keys():
    actual = tomli_w.dumps(
        {
            "k": 1,
            "a": {"b": {"c": {"d": {"e": {"f": {}}, "e2": {"f2": {}}}, "d_key1": 1}}},
        }
    )
    expected = """\
k = 1

[a.b.c]
d_key1 = 1

[a.b.c.d.e.f]

[a.b.c.d.e2.f2]
"""
    assert actual == expected
