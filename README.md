# AI Agent with Gemini API
This project implements an AI agent that uses Google's Gemini API to interact with a codebase. The agent can perform various operations like listing files, reading file contents, executing Python files, and writing to files.

## Features
+ Interactive AI agent using Gemini API
+ File system operations:
    + List files and directories
    + Read file contents
    + Execute Python files
    + Write or modify files
+ Debug logging for function calls and responses
+ Secure file operations (restricted to working directory)

## Prerequisites
+ Python 3.x
+ Google Gemini API key

## Installation
1. Clone the repository:

```
git clone <repository-url>
cd <repository-name>
```

2. Install required packages:
```

pip install -r requirements.txt

```
3. Create a .env file in the project root and add your Gemini API key:
```

GEMINI_API_KEY=your_api_key_here

```
4. Usage
Run the agent with a prompt:

`python main.py "your prompt here"`

For verbose output (including function call details):

`python main.py "your prompt here" --verbose`

### Example Prompts
+ "List all files in the current directory"
+ "Read the contents of file.py"
+ "Run the calculator.py file"
+ "Fix the bug in calculator.py"

## Security
+ All file operations are restricted to the working directory
+ No access to files outside the working directory
+ API key is stored in environment variables

## Debug Output
The agent provides debug output for:

+ Function calls and their arguments
+ Function responses
+ Message history
+ Number of function calls and responses
