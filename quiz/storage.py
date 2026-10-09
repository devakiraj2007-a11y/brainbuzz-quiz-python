import json
from datetime import datetime
from pathlib import Path

SCORE_FILE = Path(__file__).resolve().parent.parent / "leaderboard.json"
MAX_ENTRIES = 50


def _load():
    try:
        data = json.loads(SCORE_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def _save(entries):
    try:
        SCORE_FILE.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    except OSError:
        pass


def load_leaderboard(limit=10):
    entries = sorted(_load(), key=lambda e: e.get("score", 0), reverse=True)
    return entries[:limit]


def best_score():
    top = load_leaderboard(1)
    return top[0]["score"] if top else 0


def add_score(name, score, category, correct, total):
    """Save a result and return the player's rank (1 = best)."""
    entry = {
        "name": (name or "Player")[:16],
        "score": score,
        "category": category,
        "correct": correct,
        "total": total,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    entries = _load()
    entries.append(entry)
    entries.sort(key=lambda e: e.get("score", 0), reverse=True)
    rank = next(i for i, e in enumerate(entries) if e is entry) + 1
    _save(entries[:MAX_ENTRIES])
    return rank