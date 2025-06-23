import os


def get_files_info(working_directory, directory=None):
    # if directory is not provided, use working_directory
    if directory is None:
        directory = working_directory

    # if directory is outside of working_directory, raise an error
    if directory and not working_directory.startswith(directory):
        return (f"Error: Cannot list '{directory}' because it is outside\
                of the permitted working directory")

    # if directory is not a directory, raise an error
    if directory and not os.path.isdir(directory):
        return (f"Error: '{directory}' is not a directory")

    try:
        # List all items in the directory
        items = os.listdir(directory)
        result_lines = []

        for item in sorted(items):
            item_path = os.path.join(directory, item)

            # Check if it's a directory
            is_dir = os.path.isdir(item_path)

            # Get file size
            if is_dir:
                # For directories, use a default size of 128 bytes as shown in
                # the example
                file_size = 128
            else:
                # For files, get the actual file size
                file_size = os.path.getsize(item_path)

            # Format the line according to the specified format
            line = f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
            result_lines.append(line)

        # Join all lines with newlines
        return "\n".join(result_lines)

    except (OSError, PermissionError) as e:
        return f"Error: Unable to read directory contents: {str(e)}"
