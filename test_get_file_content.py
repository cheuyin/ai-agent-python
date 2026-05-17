from functions.get_file_content import get_file_content


result = get_file_content("calculator", "lorem.txt")
print("Result for 'calculator/lorem.txt' file")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")

result = get_file_content("calculator", "main.py")
print("Result for 'calculator/main.py' file")
print(result)

result = get_file_content("calculator", "pkg/calculator.py")
print("Result for 'calculator/pkg/calculator.py' file")
print(result)

result = get_file_content("calculator", "/bin/cat")
print("Result for '/bin/cat' file")
print(result)

result = get_file_content("calculator", "pkg/does_not_exist.py")
print("Result for 'calculator/pkg/does_not_exist.py' file")
print(result)
