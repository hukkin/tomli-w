import tomli_w


def test_dump(tmp_path):
    toml_obj = {"testing": "test\ntest"}
    path = tmp_path / "test.toml"
    with open(path, "w", encoding="utf-8") as f:
        tomli_w.dump(toml_obj, f)
    assert path.read_text(encoding="utf-8") == 'testing = "test\\ntest"\n'
