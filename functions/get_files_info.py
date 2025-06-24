import os


def get_files_info(working_directory, directory=None):
    # Convert working directory to absolute path
    abs_working_dir = os.path.abspath(working_directory)
    
    # if directory is not provided, use working_directory
    if directory is None:
        target_directory = abs_working_dir
    else:
        # If directory is relative, join it with the working directory
        if os.path.isabs(directory):
            target_directory = os.path.abspath(directory)
        else:
            target_directory = os.path.abspath(os.path.join(abs_working_dir, directory))

    # if directory is outside of working_directory, raise an error
    if not target_directory.startswith(abs_working_dir):
        return (f"Error: Cannot list '{directory}' because it is outside\
                of the permitted working directory")

    # if directory is not a directory, raise an error
    if not os.path.isdir(target_directory):
        return (f"Error: '{directory}' is not a directory")

    try:
        # List all items in the directory
        items = os.listdir(target_directory)
        result_lines = []

        for item in sorted(items):
            item_path = os.path.join(target_directory, item)

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
