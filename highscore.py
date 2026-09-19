"""Persistent JSON-based highscore storage (top 10)."""

import json
from pathlib import Path
from typing import TypedDict
import importlib
pac_man_main_file = importlib.import_module("pac-man")


class height_score(TypedDict):
    name: str
    score: int


_FILE = Path(
    f"{pac_man_main_file.configuration.highscore_filename}.json")


def _load() -> list[height_score]:
    "Open the highscores json file and return the value in it"
    try:
        with open(_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def is_top_10(score: int) -> bool:
    """Return True if this score would make it into the top 10."""
    entries = _load()
    return len(entries) < 10 or score > min(e["score"] for e in entries)


def add_highscore(name: str, score: int) -> None:
    """Add a name/score pair, keep only the top 10, save to disk."""
    entries = _load()
    clean_name = "".join(c for c in name if c.isalnum() or c == " ")[:10]
    entries.append({"name": clean_name, "score": max(score, 0)})
    entries.sort(key=lambda e: e["score"], reverse=True)
    with open(_FILE, "w", encoding="utf-8") as f:
        json.dump(entries[:10], f, indent=2)


def get_top_10() -> list[height_score]:
    """Return the current top 10 entries."""
    return _load()
