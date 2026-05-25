import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from call_function import available_functions, call_function
from config import MAX_ITERS, SYSTEM_PROMPT, MODEL, THINKING_LEVEL, MAX_CONTEXT_TOKENS, MODEL_CONFIGS
from session_storage import new_session_id, save_session, load_session, list_sessions


def trim_oldest_turn(messages: list) -> None:
    """Drop the oldest complete turn (user + model/tool messages) from history in place."""
    user_indices = [i for i, m in enumerate(messages) if m.role == "user"]
    if len(user_indices) >= 2:
        del messages[:user_indices[1]]


def run_agent_turn(messages: list, client, verbose: bool) -> dict:
    total_input_tokens = 0
    total_output_tokens = 0
    last_prompt_token_count = 0

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

        prompt_tokens = res.usage_metadata.prompt_token_count or 0
        output_tokens = res.usage_metadata.candidates_token_count or 0
        total_input_tokens += prompt_tokens
        total_output_tokens += output_tokens
        last_prompt_token_count = prompt_tokens

        if prompt_tokens > MAX_CONTEXT_TOKENS:
            trim_oldest_turn(messages)
            print(f"Warning: context large ({prompt_tokens:,} tokens), trimmed oldest turn from history")

        if not res.function_calls:
            return {
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "prompt_token_count": last_prompt_token_count,
                "response_text": res.text,
            }

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

    if MODEL not in MODEL_CONFIGS:
        raise RuntimeError(f"Please define input_cost and output_cost for {MODEL} in config.py")
    model_config = MODEL_CONFIGS[MODEL]

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", nargs="?", default=None, type=str,
                        help="Optional initial user prompt")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")
    parser.add_argument("--resume", metavar="SESSION_ID", type=str,
                        help="Resume a previous session by ID")
    parser.add_argument("--history", action="store_true",
                        help="List and pick a previous session to resume")
    args = parser.parse_args()

    messages: list = []
    session_id = new_session_id()
    total_input_tokens = 0
    total_output_tokens = 0

    if args.resume:
        messages = load_session(args.resume)
        session_id = args.resume
        print(f"Resumed session: {session_id} ({len(messages)} messages)")
    elif args.history:
        sessions = list_sessions()
        if not sessions:
            print("No saved sessions found.")
        else:
            for i, s in enumerate(sessions):
                print(f"  {i + 1}. {s}")
            choice = input("Pick a session (number): ").strip()
            session_id = sessions[int(choice) - 1]
            messages = load_session(session_id)
            print(f"Resumed session: {session_id} ({len(messages)} messages)")

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
                if messages:
                    save_session(messages, session_id)
                    print(f"Session saved: {session_id}")
                break

        if user_input.strip().lower() in ("exit", "quit"):
            if messages:
                save_session(messages, session_id)
                print(f"Session saved: {session_id}")
            break
        if not user_input.strip():
            continue

        messages.append(types.Content(
            role="user", parts=[types.Part(text=user_input)]))
        result = run_agent_turn(messages, client, args.verbose)

        total_input_tokens += result["input_tokens"]
        total_output_tokens += result["output_tokens"]
        total_cost = (
            total_input_tokens / 1_000_000 * model_config["input_cost_per_million"]
            + total_output_tokens / 1_000_000 * model_config["output_cost_per_million"]
        )

        print(f"\nModel: {MODEL}")
        print(f"Context: {result['prompt_token_count']:,} / {model_config['input_token_limit']:,} tokens")
        print(f"Cost so far: ${total_cost:.6f}")
        print(f"\nAgent: {result['response_text']}")


if __name__ == "__main__":
    main()
