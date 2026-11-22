import re

from depfeed.dates import parse_date
from depfeed.records import Record, record_id

_KEYS = {"shutdown": "shutdown", "affected": "affected",
         "replacement": "replacement", "notice": "announced"}


def _cells(line: str) -> list[str]:
    line = line.strip().removeprefix("|").removesuffix("|")
    return [c.strip() for c in re.split(r"(?<!\\)\|", line)]


def _plain(s: str) -> str:
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s.replace("**", ""))
    return " ".join(s.replace("`", "").split())


def _row(c: dict[str, str], link: str) -> Record:
    shutdown = parse_date(c.get("shutdown", ""))
    announced = parse_date(c.get("announced", ""))
    cell = c.get("affected", "")
    affected = re.findall(r"`([^`]+)`", cell)
    if not affected:
        affected = [a.strip() for a in _plain(cell).split(",") if a.strip()]
    rep = _plain(c.get("replacement", ""))
    title = f"{_plain(cell)} — shutdown {shutdown or c.get('shutdown', '')}"
    parts = ["openai", announced or shutdown or "", affected[0] if affected else title]
    rid = record_id(*parts)
    return Record(id=rid, source="openai", kind="parsed", title=title, url=link,
                  announced=announced, shutdown=shutdown, affected=affected,
                  replacement=None if rep in ("", "—", "-", "N/A") else rep)


def parse(text: str, link: str) -> list[Record]:
    out: list[Record] = []
    seen: set[str] = set()
    cols: dict[int, str] | None = None
    for line in text.splitlines():
        if not line.startswith("|"):
            cols = None
            continue
        cells = _cells(line)
        if cols is None:
            low = [c.lower() for c in cells]
            if any("shutdown" in c for c in low) and any("affected" in c for c in low):
                cols = {i: v for i, c in enumerate(low)
                        for k, v in _KEYS.items() if k in c}
            continue
        if all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        r = _row({cols[i]: c for i, c in enumerate(cells) if i in cols}, link)
        if r.id in seen:  # same date + first ID twice: disambiguate by full affected cell
            r.id = record_id("openai", r.announced or r.shutdown or "", r.affected[0] if r.affected else r.title, "|".join(r.affected))
        seen.add(r.id)
        out.append(r)
    return out
