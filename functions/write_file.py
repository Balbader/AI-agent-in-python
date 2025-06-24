import os


def write_file(working_directory, file_path, content):
    # Resolve both paths to absolute paths for proper comparison
    abs_working_dir = os.path.abspath(working_directory)
    
    # If file_path is relative, join it with the working directory
    if os.path.isabs(file_path):
        abs_file_path = os.path.abspath(file_path)
    else:
        abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    # Check if the file path is within the working directory
    if not abs_file_path.startswith(abs_working_dir):
        return (f"Error: Cannot write '{file_path}' as it is outside "
                f"of the permitted working directory '{working_directory}'")

    # Create the directory if it doesn't exist
    file_dir = os.path.dirname(abs_file_path)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir, exist_ok=True)

    # Write the content to the file
    with open(abs_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    return f"Successfully wrote to '{file_path}'\
        ({len(content)} characters written)"
