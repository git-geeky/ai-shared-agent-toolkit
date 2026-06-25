"""Optional private restore overlay for public agent toolkit examples."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping


RESTORE_FILE_ENV = "AI_SHARED_TOOLKIT_RESTORE_FILE"


def default_restore_path() -> Path:
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "ai-shared-agent-toolkit" / "restore.local.json"
    return Path.home() / ".config" / "ai-shared-agent-toolkit" / "restore.local.json"


def load_restore_config(env_var: str = RESTORE_FILE_ENV) -> dict[str, Any]:
    explicit = os.environ.get(env_var)
    path = Path(explicit).expanduser() if explicit else default_restore_path()
    if not path.exists():
        if explicit:
            raise FileNotFoundError(f"{env_var} points to a missing file")
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("restore file must be a JSON object")
    return dict(payload)


def output_path_for_tool(tool: str, restore: Mapping[str, Any] | None = None) -> Path | None:
    payload = restore if restore is not None else load_restore_config()
    outputs = payload.get("outputs", {}) if isinstance(payload, Mapping) else {}
    if not isinstance(outputs, Mapping):
        raise ValueError("restore outputs must be a JSON object")
    value = outputs.get(tool)
    return Path(str(value)).expanduser() if value else None

