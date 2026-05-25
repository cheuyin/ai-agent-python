import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from call_function import available_functions, call_function
from config import MAX_ITERS, SYSTEM_PROMPT, MODEL, THINKING_LEVEL, MAX_CONTEXT_TOKENS


def trim_oldest_turn(messages: list) -> None:
    """Drop the oldest complete turn (user + model/tool messages) from history in place."""
    user_indices = [i for i, m in enumerate(messages) if m.role == "user"]
    if len(user_indices) >= 2:
        del messages[:user_indices[1]]


def run_agent_turn(messages: list, client, verbose: bool) -> None:
    for _ in range(MAX_ITERS):
        for attempt in range(3):
            try:
                res = client.models.generate_content(
                    model=MODEL,
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=[available_functions],
                        system_instruction=SYSTEM_PROMPT,
                        thinking_config=types.ThinkingConfig(
                            thinking_level=THINKING_LEVEL) if THINKING_LEVEL else None,
                    )
                )
                break
            except Exception as e:
                if attempt == 2:
                    raise
                wait = 2 ** attempt
                print(f"API error ({e}), retrying in {wait}s...")
                time.sleep(wait)
        else:
            raise RuntimeError("unreachable")

        if res.candidates:
            for candidate in res.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if res.usage_metadata is None:
            raise RuntimeError("API request failed: invalid response.")

        if verbose:
            print("Prompt tokens:", res.usage_metadata.prompt_token_count)
            print("Response tokens:", res.usage_metadata.candidates_token_count)

        token_count = res.usage_metadata.prompt_token_count or 0
        if token_count > MAX_CONTEXT_TOKENS:
            trim_oldest_turn(messages)
            print(f"Warning: context large ({token_count:,} tokens), trimmed oldest turn from history")

        if not res.function_calls:
            print(f"Agent: {res.text}")
            return

        function_responses: list[types.Part] = []

        for fc in res.function_calls:
            result = call_function(fc, verbose)

            if (
                not result.parts
                or not result.parts[0].function_response
                or not result.parts[0].function_response.response
            ):
                print(
                    f"Warning: empty function response for {fc.name}, skipping")
                continue

            function_responses.append(result.parts[0])

            if verbose:
                print(f"-> {result.parts[0].function_response.response}")

        messages.append(types.Content(role="tool", parts=function_responses))
    else:
        print("Maximum number of back-and-forths reached. Exiting program.")
        raise SystemExit(1)


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key is invalid.")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", nargs="?", default=None, type=str,
                        help="Optional initial user prompt")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")
    args = parser.parse_args()

    messages: list = []
    initial_prompt = args.user_prompt

    while True:
        if initial_prompt is not None:
            user_input = initial_prompt
            initial_prompt = None
            print(f"You: {user_input}")
        else:
            try:
                user_input = input("You: ")
            except EOFError:
                print()
                break

        if user_input.strip().lower() in ("exit", "quit"):
            break
        if not user_input.strip():
            continue

        messages.append(types.Content(
            role="user", parts=[types.Part(text=user_input)]))
        run_agent_turn(messages, client, args.verbose)


if __name__ == "__main__":
    main()
