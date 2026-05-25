import os
from tools.write_file import write_file


def test_write_file_creates_file(tmp_path):
    result = write_file(str(tmp_path), "hello.txt", "hello world")
    assert "Successfully" in result
    assert (tmp_path / "hello.txt").read_text() == "hello world"


def test_write_file_subdirectory(tmp_path):
    (tmp_path / "subdir").mkdir()
    result = write_file(str(tmp_path), "subdir/hello.txt", "hello")
    assert "Successfully" in result
    assert (tmp_path / "subdir" / "hello.txt").read_text() == "hello"


def test_write_file_creates_parent_dirs(tmp_path):
    result = write_file(str(tmp_path), "new/nested/hello.txt", "nested content")
    assert "Successfully" in result
    assert (tmp_path / "new" / "nested" / "hello.txt").read_text() == "nested content"


def test_write_file_outside_sandbox(tmp_path):
    escape_path = "/tmp/escape_test_write.txt"
    result = write_file(str(tmp_path), escape_path, "should not be written")
    assert "Error:" in result
    assert not os.path.exists(escape_path)
