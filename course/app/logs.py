"""JSON logging for agent runs (prototype — not production)."""

from __future__ import annotations

import json
import os
import secrets
from datetime import datetime, timezone
from pathlib import Path

from pydantic_ai.messages import ModelMessagesTypeAdapter

LOG_DIR = Path(os.environ.get("LOGS_DIRECTORY", "logs"))
LOG_DIR.mkdir(exist_ok=True)


def _instructions_text(agent) -> str:
    parts = getattr(agent, "_instructions", None) or []
    return "\n\n".join(str(p) for p in parts)


def log_entry(agent, messages, source: str = "user"):
    tools: list[str] = []
    for ts in agent.toolsets:
        tools.extend(ts.tools.keys())
    dict_messages = ModelMessagesTypeAdapter.dump_python(messages)
    return {
        "agent_name": agent.name,
        "system_prompt": _instructions_text(agent),
        "model": str(agent.model),
        "tools": tools,
        "messages": dict_messages,
        "source": source,
    }


def serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def log_interaction_to_file(agent, messages, source: str = "user"):
    entry = log_entry(agent, messages, source)
    ts_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    rand_hex = secrets.token_hex(3)
    filename = f"{entry['agent_name']}_{ts_str}_{rand_hex}.json"
    filepath = LOG_DIR / filename
    with filepath.open("w", encoding="utf-8") as f_out:
        json.dump(entry, f_out, indent=2, default=serializer)
    return filepath
