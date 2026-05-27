# Local AI Coding Agent

A terminal-based AI coding agent powered by the Google Gemini API. Give it a task and it figures out the steps, reading, writing, and executing files in a sandboxed working directory until it's done.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-API-4285F4?logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

<!-- Replace with demo GIF -->
![Demo](assets/demo.gif)

---

## How It Works

The agent runs a multi-round inference loop. Each model response is inspected for tool calls, the tools are executed, and results are fed back into the context. This repeats until the model produces a final text response with no pending tool calls.

```
User prompt
    │
    ▼
┌─────────────────────────────────────┐
│           Gemini API Call           │
│                                     │
│  Response has tool calls?           │
│    Yes → execute tools → loop back  │
│    No  → return final response      │
└─────────────────────────────────────┘
    │
    ▼
Rendered response + token/cost stats
```

---

## Key Features

- **Autonomous agentic loop**: dispatches tool calls across up to 20 iterative model rounds per turn without human intervention
- **Context window management**: tracks prompt token counts each round and trims the oldest conversation turn when approaching the 1M-token limit, enabling indefinitely long sessions
- **Sandboxed execution**: all file paths validated via `os.path.commonpath` before execution; any path escaping the working directory is rejected
- **Session persistence**: full conversation histories (including tool call/response pairs) serialized to JSON and deserialized back to typed SDK objects; sessions are resumable across processes
- **Resilience**: 3-attempt exponential backoff retry on transient API failures
- **Cost tracking**: input/output tokens accumulated across all loop iterations and converted to a running dollar cost, displayed after every response

---

## Tools

The agent has access to five file system tools, all sandboxed to `./sandbox/`:

| Tool | Description |
|---|---|
| `get_files_info` | List files and directories |
| `get_file_content` | Read file contents |
| `write_file` | Write or overwrite files |
| `run_python_file` | Execute a Python script and return stdout/stderr |
| `delete_file` | Delete files or directories |

---

## Setup

**Prerequisites:** [uv](https://docs.astral.sh/uv/), a [Gemini API key](https://aistudio.google.com/apikey)

```bash
git clone https://github.com/cheuyin/ai-agent-python.git
cd ai-agent-python
uv sync
cp .env.example .env  # add your GEMINI_API_KEY
```

## Usage

```bash
uv run main.py                                  # interactive mode
uv run main.py "refactor the calculator"        # initial prompt
uv run main.py --resume 2026-05-25_02-37-48     # resume a session
uv run main.py --history                        # browse past sessions
```

---

## License

MIT
