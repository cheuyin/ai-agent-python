import os
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key is invalid.")

    client = genai.Client(api_key=api_key)

    res = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )

    if res.usage_metadata is None:
        raise RuntimeError("API request failed: invalid response.")

    print("Prompt tokens:", res.usage_metadata.prompt_token_count)
    print("Response tokens: ", res.usage_metadata.candidates_token_count)

    print(res.text)


if __name__ == "__main__":
    main()
