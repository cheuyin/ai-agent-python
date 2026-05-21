from tools.get_files_info import get_files_info


def test():
    # result = get_files_info("sandbox/calculator", ".")
    # print("Result for current directory:")
    # print(result)
    # print("")

    # result = get_files_info("sandbox/calculator", "/bin")
    # print("Result for '/bin' directory:")
    # print(result)
    # print("")

    # result = get_files_info("sandbox/calculator", "../")
    # print("Result for '../' directory:")
    # print(result)
    # print("")

    # result = get_files_info("sandbox/calculator", "main.py")
    # print("Result for 'main.py':")
    # print(result)

    result = get_files_info("sandbox/calculator", ".")
    print("Result for current directory:")
    print(result)

    result = get_files_info("sandbox/calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)

    result = get_files_info("sandbox/calculator", "/bin")
    print("Result for '/bin' directory:")
    print(result)

    result = get_files_info("sandbox/calculator", "../")
    print("Result for '../' directory:")
    print(result)


if __name__ == "__main__":
    test()
