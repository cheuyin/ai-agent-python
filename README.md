# AI Agent (Python)

A local AI coding agent powered by Google Gemini that can read, write, and execute files within a working directory.

## Setup

1. Install [uv](https://docs.astral.sh/uv/)
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_key_here
   ```

## Usage

```bash
uv run main.py "your prompt here"
uv run main.py "your prompt here" --verbose
```

The agent operates on the `./sandbox/` directory by default (configured in `config.py`).

## Tools

The agent can:
- List files and directories
- Read file contents
- Write files
- Execute Python files
- Delete files and directories
