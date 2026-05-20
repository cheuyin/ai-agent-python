import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from call_function import available_functions, call_function
from config import MAX_ITERS, SYSTEM_PROMPT


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

    messages = [types.Content(
        role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(MAX_ITERS):
        res = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=SYSTEM_PROMPT)
        )

        if res.candidates:
            for candidate in res.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if res.usage_metadata is None:
            raise RuntimeError("API request failed: invalid response.")

        if args.verbose:
            print("User prompt:", args.user_prompt)
            print("Prompt tokens:", res.usage_metadata.prompt_token_count)
            print("Response tokens: ", res.usage_metadata.candidates_token_count)

        if not res.function_calls:
            print(res.text)
            break

        function_responses: list[types.Part] = []

        for fc in res.function_calls:
            result = call_function(fc, args.verbose)

            if (
                not result.parts
                or not result.parts[0].function_response
                or not result.parts[0].function_response.response
            ):
                raise RuntimeError(
                    f"Empty function response for {fc.name}")

            function_responses.append(result.parts[0])

            if args.verbose:
                print(
                    f"-> {result.parts[0].function_response.response}")

        messages.append(types.Content(role="tool", parts=function_responses))
    else:
        print("Maximum number of back-and-forths reached. Exiting program.")
        exit(1)


if __name__ == "__main__":
    main()
