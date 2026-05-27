# AI Agent Python — Claude Code Instructions

## Project Overview
A local AI coding agent powered by Google Gemini with a Rich-based TUI. The agent can read, write, and execute files within a sandboxed working directory (`./sandbox/`).

## Architecture

```
main.py            — Entry point, REPL loop, context trimming, cost tracking
config.py          — Model name, pricing configs, system prompt, constants
call_function.py   — Tool registry and function dispatch
render.py          — Rich-based console rendering (banner, panels, stats)
session_storage.py — JSON-based session persistence (save/load/list)
tools/             — Individual tool implementations
  get_files_info.py
  get_file_content.py
  run_python_file.py
  write_file.py
  delete_file.py
tests/             — pytest unit tests for each tool
sandbox/           — Agent's working directory (gitignored, auto-created)
sessions/          — Saved conversation sessions (gitignored)
```

## Common Commands

```bash
# Install dependencies
uv sync

# Run the agent (interactive)
uv run main.py

# Run with an initial prompt
uv run main.py "your prompt here"

# Resume a previous session
uv run main.py --resume 2026-05-25_02-37-48

# Browse and pick a session interactively
uv run main.py --history

# Run tests
uv run pytest

# Lint
uv run ruff check .
```

## Environment

Requires a `.env` file (see `.env.example`):
```
GEMINI_API_KEY=your_key_here
```

## Key Conventions
- All tool functions accept `working_directory` as their first arg (injected by `call_function.py`); never hardcode paths in tools
- Tool schemas use `google.genai.types.FunctionDeclaration`
- Sessions are stored as JSON lists of `types.Content` objects, serialized via `model_dump`
- Context trimming drops the oldest user+model turn when `prompt_token_count > MAX_CONTEXT_TOKENS`
- Pricing is tracked per-session and displayed in the stats panel after each response
