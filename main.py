import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key is invalid.")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")
    args = parser.parse_args()

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

    main.py is located in the root of the working directory.
    """

    messages = [types.Content(
        role="user", parts=[types.Part(text=args.user_prompt)])]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
    )

    res = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt)
    )

    if res.usage_metadata is None:
        raise RuntimeError("API request failed: invalid response.")

    if args.verbose:
        print("User prompt:", args.user_prompt)
        print("Prompt tokens:", res.usage_metadata.prompt_token_count)
        print("Response tokens: ", res.usage_metadata.candidates_token_count)

    print(res.text)

    if res.function_calls:
        for fc in res.function_calls:
            print(f"Calling function: {fc.name}({fc.args})")


if __name__ == "__main__":
    main()
