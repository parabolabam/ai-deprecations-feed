import hashlib
import json
from dataclasses import asdict, dataclass, field, replace
from datetime import date, timedelta
from pathlib import Path
from typing import Literal

RAW_DAYS = 90


@dataclass
class Record:
    id: str
    source: str
    kind: Literal["parsed", "raw", "health"]
    title: str
    url: str
    announced: str | None = None
    shutdown: str | None = None
    affected: list[str] = field(default_factory=list)
    replacement: str | None = None
    status: str | None = None
    links: list[str] = field(default_factory=list)
    text: str | None = None
    first_seen: str | None = None
    updated: str | None = None


def record_id(*parts: str) -> str:
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:16]


def feed_date(r: Record) -> str:
    return r.announced or r.first_seen


def _content(r: Record) -> dict:
    d = asdict(r)
    d.pop("first_seen")
    d.pop("updated")
    return d


def merge(archive: list[Record], new: list[Record], today: str) -> list[Record]:
    out = {r.id: r for r in archive}
    for n in new:
        old = out.get(n.id)
        if old is None:
            out[n.id] = replace(n, first_seen=n.first_seen or today, updated=None,
                                affected=list(n.affected))
        elif _content(old) != _content(n):
            out[n.id] = replace(n, first_seen=old.first_seen, updated=today,
                                affected=list(n.affected))
    return list(out.values())


def prune(records: list[Record], today: str) -> list[Record]:
    cutoff = (date.fromisoformat(today) - timedelta(days=RAW_DAYS)).isoformat()
    return [r for r in records
            if r.kind == "parsed" or (r.first_seen or "") >= cutoff]


def load_records(path: Path) -> list[Record]:
    if not path.exists():
        return []
    return [Record(**d) for d in json.loads(path.read_text(encoding="utf-8"))["records"]]


def save_records(path: Path, records: list[Record]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rs = sorted(records, key=lambda r: r.id)
    rs.sort(key=feed_date, reverse=True)  # stable: id asc kept within equal dates
    data = {"records": [asdict(r) for r in rs]}
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
