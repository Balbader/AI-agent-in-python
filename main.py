import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

user_prompt = sys.argv[1]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan.\
    You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not\
    need to specify the working directory in your function calls as it is\
        automatically injected for security reasons.
"""

if len(sys.argv) < 2:
    print("Usage: python main.py <message>")
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their\
        sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the\
                    working directory. If not provided, lists files in the\
                    working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of the specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The file to get the content of, relative to the\
                    working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to the specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working\
                    directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified Python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The Python file to run, relative to the working\
                    directory.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python,
    ]
)


# Check if verbose mode is enabled
verbose_mode = len(sys.argv) == 3 and sys.argv[2] == "--verbose"

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions],
    ),
)

if response.function_calls:
    tool_responses = []
    for function_call in response.function_calls:
        tool_response = call_function(function_call, verbose=verbose_mode)
        if tool_response:
            tool_responses.append(tool_response)

            # Check if the response has the expected structure
            if not hasattr(tool_response.parts[0], 'function_response') or \
               not hasattr(tool_response.parts[0].function_response,
                           'response'):
                raise Exception("Invalid function response structure")

            # Print result if verbose mode is enabled
            if verbose_mode:
                print(f"-> \
                      {tool_response.parts[0].function_response.response}")

    # Print function results directly instead of making another API call
    if tool_responses:
        for tool_response in tool_responses:
            result = tool_response.parts[0].function_response.response
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                print(result['result'])
else:
    print(response.text)

if verbose_mode:
    print("User prompt: ", user_prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
