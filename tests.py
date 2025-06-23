from functions.get_file_content import get_file_content

print(get_file_content("./calculator", "./calculator/lorem.txt"))
print(get_file_content("./calculator", "./calculator/main.py"))
print(get_file_content("./calculator", "./calculator/pkg/calculator.py"))
print(get_file_content("./calculator", "/bin/cat"))
