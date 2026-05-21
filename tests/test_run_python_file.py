from tools.run_python_file import run_python_file


def main():
    result = run_python_file("sandbox/calculator", "main.py")
    print(result)

    result = run_python_file("sandbox/calculator", "main.py", ["3 + 5"])
    print(result)

    result = run_python_file("sandbox/calculator", "tests.py")
    print(result)

    result = run_python_file("sandbox/calculator", "../main.py")
    print(result)

    result = run_python_file("sandbox/calculator", "nonexistent.py")
    print(result)

    result = run_python_file("sandbox/calculator", "lorem.txt")
    print(result)


if __name__ == "__main__":
    main()
