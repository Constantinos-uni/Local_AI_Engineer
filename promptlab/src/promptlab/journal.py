"""promptlab.journal — the append-only experiment log.

One JSON object per line (JSONL). Append-friendly: we open in "a" mode,
write one line, close. No database server, no migrations — just a text
file every tool on earth can read.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_JOURNAL = Path("experiments.jsonl")


def append_experiment(exp_dict: dict, path: Path = DEFAULT_JOURNAL) -> None:
    """Append one experiment to the journal, stamped with UTC time.

    `exp_dict` comes from lab.experiment_to_dict(). We add the timestamp
    here so the engine never has to care about clocks.
    """
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        **exp_dict,
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def read_history(limit: int = 10, path: Path = DEFAULT_JOURNAL) -> list[dict]:
    """Return the last `limit` experiments, oldest first.

    Reading the whole file just to show the tail is fine at this scale —
    even 10,000 experiments is only a few MB. If that changes, Chapter 16
    (SQLite) is the upgrade path.
    """
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines[-limit:] if line.strip()]