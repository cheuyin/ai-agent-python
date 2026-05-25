from tools.run_python_file import run_python_file


def test_run_python_file_basic(tmp_path):
    (tmp_path / "hello.py").write_text('print("hello")')
    result = run_python_file(str(tmp_path), "hello.py")
    assert "hello" in result


def test_run_python_file_with_args(tmp_path):
    (tmp_path / "echo_arg.py").write_text("import sys\nprint(sys.argv[1])")
    result = run_python_file(str(tmp_path), "echo_arg.py", ["myarg"])
    assert "myarg" in result


def test_run_python_file_missing_file(tmp_path):
    result = run_python_file(str(tmp_path), "nonexistent.py")
    assert "Error:" in result


def test_run_python_file_outside_sandbox(tmp_path):
    result = run_python_file(str(tmp_path), "../main.py")
    assert "Error:" in result


def test_run_python_file_non_py_extension(tmp_path):
    (tmp_path / "script.txt").write_text("print('hi')")
    result = run_python_file(str(tmp_path), "script.txt")
    assert "Error:" in result
