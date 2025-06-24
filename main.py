import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

user_prompt = sys.argv[1]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan.\
    You can perform the following operations:

- List files and directories

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

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions],
    ),
)
if response.function_calls:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name} ({function_call.args})")
else:
    print(response.text)

if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
    print("User prompt: ", user_prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
