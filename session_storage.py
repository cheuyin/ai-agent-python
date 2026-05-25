import json
import os
from datetime import datetime
from google.genai import types

SESSIONS_DIR = "./sessions"


def new_session_id() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def save_session(messages: list, session_id: str) -> None:
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    data = {
        "session_id": session_id,
        "messages": [m.model_dump(mode="json", exclude_none=True) for m in messages],
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_session(session_id: str) -> list:
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    with open(path, "r") as f:
        data = json.load(f)
    return [types.Content.model_validate(m) for m in data["messages"]]


def list_sessions() -> list[str]:
    if not os.path.exists(SESSIONS_DIR):
        return []
    return sorted(
        [f[:-5] for f in os.listdir(SESSIONS_DIR) if f.endswith(".json")],
        reverse=True,
    )
