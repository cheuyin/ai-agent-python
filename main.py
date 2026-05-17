import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key is invalid.")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    messages = [types.Content(
        role="user", parts=[types.Part(text=args.user_prompt)])]

    res = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=messages
    )

    if res.usage_metadata is None:
        raise RuntimeError("API request failed: invalid response.")

    print("Prompt tokens:", res.usage_metadata.prompt_token_count)
    print("Response tokens: ", res.usage_metadata.candidates_token_count)

    print(res.text)


if __name__ == "__main__":
    main()
