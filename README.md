# AI Agent (Python)

A local AI coding agent powered by Google Gemini that can read, write, and execute files within a sandboxed working directory.

## Setup

1. Install [uv](https://docs.astral.sh/uv/)
2. Install dependencies:
   ```bash
   uv sync
   ```
3. Copy `.env.example` and add your Gemini API key:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env`:
   ```
   GEMINI_API_KEY=your_key_here
   ```

## Usage

```bash
# Interactive mode
uv run main.py

# Start with an initial prompt
uv run main.py "your prompt here"

# Resume a previous session by ID
uv run main.py --resume 2026-05-25_02-37-48

# Browse saved sessions interactively
uv run main.py --history
```

The agent operates on the `./sandbox/` directory by default (configured in `config.py`). The directory is created automatically on first run.

## Tools

The agent can:
- List files and directories
- Read file contents
- Write files
- Execute Python files
- Delete files and directories

## Development

```bash
# Run tests
uv run pytest

# Lint
uv run ruff check .
```
