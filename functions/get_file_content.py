import os


def get_file_content(working_directory, file_path):
    try:
        # Convert to absolute paths for proper comparison
        abs_working_dir = os.path.abspath(working_directory)
        
        # If file_path is relative, join it with the working directory
        if os.path.isabs(file_path):
            abs_file_path = os.path.abspath(file_path)
        else:
            abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

        # if the file is outside of the working_directory, raise an error
        if not abs_file_path.startswith(abs_working_dir):
            return (f"Error: Cannot read '{file_path}' because it is outside\
                    of the permitted working directory")

        # if the file is not a file, raise an error
        if not os.path.isfile(abs_file_path):
            return (f"Error: File not found or is not a regular file:\
                    '{file_path}'")

        # Read the file content
        with open(abs_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Truncate if longer than 10000 characters
        if len(content) > 10000:
            content = (content[:10000] + f'\n[...File "{file_path}"\
                    \ntruncated at 10000 characters...]')

        return content

    except Exception as e:
        return f"Error: {str(e)}"
