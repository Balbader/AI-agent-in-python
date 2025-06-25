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
You are a helpful AI coding agent that takes action immediately.

When a user asks a question or makes a request, START by making function calls
to gather information. Do not just make plans - take action!

You can perform the following operations:
- List files and directories using get_files_info
- Read file contents using get_file_content
- Execute Python files using run_python_file
- Write or overwrite files using write_file

Always start by exploring the codebase with function calls before providing
analysis. All paths you provide should be relative to the working directory.

Take action now - make function calls to understand the codebase first!
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

# Agent loop - iterate up to 20 times
max_iterations = 20
for iteration in range(max_iterations):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        ),
    )

    # Add the model's response to messages (only the first candidate)
    if response.candidates:
        messages.append(response.candidates[0].content)

    # Check if there are function calls to process
    if response.function_calls:
        tool_responses = []
        for function_call in response.function_calls:
            tool_response = call_function(function_call, verbose=verbose_mode)
            if tool_response:
                tool_responses.append(tool_response)

                # Check if the response has the expected structure
                if not hasattr(tool_response.parts[0], 'function_response') or\
                   not hasattr(tool_response.parts[0].function_response,
                               'response'):
                    raise Exception("Invalid function response structure")

                # Print result if verbose mode is enabled
                if verbose_mode:
                    print(f"-> \
                          {tool_response.parts[0].function_response.response}")

        # Add tool responses to messages for next iteration
        if tool_responses:
            messages.extend(tool_responses)

        # Continue to next iteration since we made function calls
        continue
    else:
        # No function calls - agent is done, print final response and break
        print("Final response:")
        print(response.text)
        break
else:
    # If we reached max iterations, print a message
    print("Maximum iterations reached. Agent may not have completed the task.")

if verbose_mode:
    print("User prompt: ", user_prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
