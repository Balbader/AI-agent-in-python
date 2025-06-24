import os
import subprocess


def run_python(working_directory, file_path):
    result = None

    # Run the Python file
    try:
        # Resolve both paths to absolute paths for proper comparison
        abs_working_dir = os.path.abspath(working_directory)

        # Resolve the file path relative to the working directory
        if os.path.isabs(file_path):
            abs_file_path = file_path
        else:
            abs_file_path = os.path.abspath(
                os.path.join(abs_working_dir, file_path)
                )

        # Check if the file path is within the working directory
        if not abs_file_path.startswith(abs_working_dir):
            return (f'Cannot execute "{file_path}" as it is outside\
                    the permitted working directory.')

        # if the file does not exist, return an error
        if not os.path.exists(abs_file_path):
            return (f'File "{file_path}" not found.')

        # if the file is not a Python file, return an error
        elif not abs_file_path.endswith('.py'):
            return (f'"{file_path}" is not a Python file.')

        result = subprocess.run(
            ['python', abs_file_path],
            cwd=abs_working_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            text=True,
        )
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)

        # if the process exits with a non-zero exit code, return an error
        if result.returncode != 0:
            return (f'Process exited with code {result.returncode}.')

        # if no output is returned, return an error
        if result is None:
            return ('No output produced.')

    # if the process exits with a timeout, return an error
    except subprocess.TimeoutExpired:
        print("The script timed out after 30 seconds.")

    # if an error occurs, return an error
    except Exception as e:
        print(f"An error occurred: {e}")

    # return the result
    return result
