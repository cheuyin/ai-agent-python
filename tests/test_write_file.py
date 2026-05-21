from tools.write_file import write_file


def test():
    result = write_file("sandbox/calculator", "lorem.txt",
                        "wait, this isn't lorem ipsum")
    print(result)

    result = write_file("sandbox/calculator", "pkg/morelorem.txt",
                        "lorem ipsum dolor sit amet")
    print(result)

    result = write_file("sandbox/calculator", "/tmp/temp.txt",
                        "this should not be allowed")
    print(result)


if __name__ == "__main__":
    test()
