import re

from depfeed.dates import parse_date
from depfeed.records import Record, record_id

STATUS = {"Models with a scheduled EOL date": "Legacy", "Models that have reached EOL": "EOL reached"}
PAIR = re.compile(r"\*\*(.+?):\*\*\s*(.*)")
LABEL = {"Legacy date": "Legacy", "EOL date": "EOL", "Public extended access start date": "extended access"}


def _record(g: dict, status, link: str, seen: set) -> Record:
    ids = [re.sub(r"\s*\(.*?\)", "", i).strip() for i in g["id"].split(",")]
    iso = lambda s: parse_date(s) or s  # noqa: E731
    eols = [d for r in g["regions"] if (d := parse_date(r.get("EOL date", "")))]
    if not eols:
        raise ValueError(f"bedrock: no EOL date for {ids[0]}")
    shutdown = min(eols)
    parts = []
    for r in g["regions"]:
        vals = ", ".join(f"{LABEL[k]} {iso(v)}" for k, v in r.items() if k in LABEL)
        parts.append(f"{r.get('Regions', '')}: {vals}")
    rid = record_id("bedrock", ids[0])
    if rid in seen:
        rid = record_id("bedrock", ids[0], status or "", shutdown)
    seen.add(rid)
    return Record(
        id=rid, source="bedrock", kind="parsed", url=link, announced=None, shutdown=shutdown,
        affected=ids, status=status, text="; ".join(parts),
        title=f"Model EOL {shutdown}: {g.get('name', ids[0])} ({', '.join(ids)})",
    )


def parse(text: str, link: str) -> list[Record]:
    out, seen, status, g = [], set(), None, None

    def flush():
        if g and "id" in g:
            out.append(_record(g, status, link, seen))

    for line in text.splitlines():
        line = line.strip()
        if line in (f"**{k}**" for k in STATUS) or line.startswith("# "):
            flush(); g = None
            status = STATUS.get(line.strip("*"))  # "# " heading -> None
        elif re.fullmatch(r"- \*\*[^:*]+\*\*", line):
            flush(); g = {"regions": []}
        elif g is not None and line.startswith("- **"):
            for part in line[2:].split(" / "):
                m = PAIR.match(part.strip())
                if not m:
                    continue
                k, v = m.groups()
                if k == "Model name":
                    g["name"] = v
                elif k == "Model ID":
                    g["id"] = v
                elif k == "Regions":
                    g["regions"].append({"Regions": v})
                elif g["regions"]:
                    g["regions"][-1][k] = v
    flush()
    return out
