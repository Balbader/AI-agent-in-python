from functions.run_python import run_python


print(run_python("calculator", "main.py"))
print(run_python("calculator", "tests.py"))
print(run_python("calculator", "../main.py"))
print(run_python("calculator", "nonexistent.py"))
