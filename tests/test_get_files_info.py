from tools.get_files_info import get_files_info


def test_get_files_info_root(tmp_path):
    (tmp_path / "alpha.txt").write_text("a")
    (tmp_path / "beta.txt").write_text("b")
    result = get_files_info(str(tmp_path), ".")
    assert "alpha.txt" in result
    assert "beta.txt" in result


def test_get_files_info_subdirectory(tmp_path):
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "child.txt").write_text("c")
    result = get_files_info(str(tmp_path), "subdir")
    assert "child.txt" in result


def test_get_files_info_outside_sandbox(tmp_path):
    result = get_files_info(str(tmp_path), "/bin")
    assert "Error:" in result


def test_get_files_info_traversal(tmp_path):
    result = get_files_info(str(tmp_path), "../")
    assert "Error:" in result
