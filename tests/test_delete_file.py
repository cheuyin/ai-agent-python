from tools.delete_file import delete_file


def test_delete_file_removes_file(tmp_path):
    f = tmp_path / "to_delete.txt"
    f.write_text("bye")
    result = delete_file(str(tmp_path), "to_delete.txt")
    assert "Successfully" in result
    assert not f.exists()


def test_delete_file_outside_sandbox(tmp_path):
    result = delete_file(str(tmp_path), "/tmp/some_file.txt")
    assert "Error:" in result


def test_delete_file_missing_file(tmp_path):
    result = delete_file(str(tmp_path), "does_not_exist.txt")
    assert "Error:" in result
