from google.genai import types

MODEL = "gemini-3.5-flash"
THINKING_LEVEL = types.ThinkingLevel.MEDIUM
MAX_CHARS = 10000
WORKING_DIR = "./sandbox/"
MAX_ITERS = 20
MAX_CONTEXT_TOKENS = 500_000

MODEL_CONFIGS = {
    "gemini-3.5-flash": {
        "input_cost_per_million": 1.50,
        "output_cost_per_million": 9.00,
        "input_token_limit": 1_000_000,
    },
}
SYSTEM_PROMPT = """
You are a helpful AI agent.

You can perform the following operations:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
- Delete files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
