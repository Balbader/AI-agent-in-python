import os


def get_files_info(working_directory, directory=None):
    # if directory is outside of working_directory, raise an error
    if directory and not working_directory.startswith(directory):
        return (f"Error: Cannot list '{directory}' because it is outside of \
                the permitted working directory")

    # if directory is not a directory, raise an error
    if not os.path.isdir(directory):
        return (f"Error: '{directory}' is not a directory")

    # Build and return a string representing the contents of the directory
    return "Contents of the directory:\n" + "\n".join(os.listdir(directory))
