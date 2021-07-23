import tomli_w


def test_dump(tmp_path):
    toml_obj = {"testing": "test\ntest"}
    path = tmp_path / "test.toml"
    with open(path, "wb") as f:
        tomli_w.dump(toml_obj, f)
    assert path.read_bytes().decode() == 'testing = "test\\ntest"\n'
