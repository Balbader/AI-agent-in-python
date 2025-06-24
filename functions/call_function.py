from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python

# Dictionary mapping function names to actual functions
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python,
}

# Dictionary mapping schema parameter names to function parameter names
parameter_mapping = {
    "get_files_info": {},  # No mapping needed
    "get_file_content": {"file": "file_path"},
    "write_file": {"file": "file_path"},
    "run_python_file": {"file": "file_path"},
}


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args.copy()

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    # Add working directory to function arguments
    import os
    function_args["working_directory"] = os.path.join(os.getcwd(), "calculator")

    # Check if function name is valid
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    try:
        # Map parameter names if needed
        if function_name in parameter_mapping:
            mapped_args = {}
            for schema_param, func_param in \
                    parameter_mapping[function_name].items():
                if schema_param in function_args:
                    mapped_args[func_param] = function_args[schema_param]

            # Add any unmapped parameters
            for param, value in function_args.items():
                if param not in parameter_mapping[function_name]:
                    mapped_args[param] = value

            function_args = mapped_args

        # Call the function using the dictionary mapping
        function_result = function_map[function_name](**function_args)

        # Return the function result as a tool response
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": str(e)},
                )
            ],
        )
