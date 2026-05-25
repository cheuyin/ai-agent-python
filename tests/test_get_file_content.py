from tools.get_file_content import get_file_content
from config import MAX_CHARS


def test_get_file_content_reads_file(tmp_path):
    (tmp_path / "hello.txt").write_text("hello world")
    result = get_file_content(str(tmp_path), "hello.txt")
    assert result == "hello world"


def test_get_file_content_subdirectory(tmp_path):
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "nested.txt").write_text("nested content")
    result = get_file_content(str(tmp_path), "subdir/nested.txt")
    assert result == "nested content"


def test_get_file_content_missing_file(tmp_path):
    result = get_file_content(str(tmp_path), "does_not_exist.txt")
    assert "Error:" in result


def test_get_file_content_outside_sandbox(tmp_path):
    result = get_file_content(str(tmp_path), "/bin/cat")
    assert "Error:" in result


def test_get_file_content_truncation(tmp_path):
    large_content = "x" * (MAX_CHARS + 100)
    (tmp_path / "large.txt").write_text(large_content)
    result = get_file_content(str(tmp_path), "large.txt")
    assert "truncated" in result
