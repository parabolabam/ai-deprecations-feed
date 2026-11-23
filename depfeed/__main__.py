import argparse
import json
import os
import shutil
import sys
from collections.abc import Callable
from dataclasses import replace
from datetime import date, datetime, timezone
from pathlib import Path

from depfeed.feeds import json_feed, rss
from depfeed.fetch import fetch_source
from depfeed.pipeline import process
from depfeed.records import load_records, merge, prune, save_records
from depfeed.sources import SOURCES, Source


def main(argv: list[str] | None = None,
         fetch: Callable[[Source], str] = fetch_source,
         sources: list[Source] = SOURCES) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data")
    ap.add_argument("--site", default="site")
    ap.add_argument("--today", default=datetime.now(timezone.utc).date().isoformat())
    ap.add_argument("--now", default=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    a = ap.parse_args(argv)
    data, site, today = Path(a.data), Path(a.site), a.today
    site_url = os.environ.get("SITE_URL", "http://localhost").rstrip("/")

    status_path = data / "status.json"
    status = (json.loads(status_path.read_text(encoding="utf-8")) if status_path.exists()
              else {"heartbeat": None, "sources": {}})
    records = load_records(data / "deprecations.json")

    for src in sources:
        snap = data / "snapshots" / f"{src.id}.md"
        old = snap.read_text(encoding="utf-8") if snap.exists() else None
        res = process(src, old, status["sources"].get(src.id), fetch, today)
        if res.snapshot is not None:
            snap.parent.mkdir(parents=True, exist_ok=True)
            snap.write_text(res.snapshot, encoding="utf-8")
        parsed = ([replace(r, baseline=True) for r in res.parsed] if res.baseline
                  else (res.parsed or []))
        records = merge(records, parsed + res.extra, today, now=a.now)
        status["sources"][src.id] = res.status

    records = prune(records, today)
    if date.fromisoformat(today).weekday() == 0:
        status["heartbeat"] = today

    save_records(data / "deprecations.json", records)
    status_path.write_text(
        json.dumps(status, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

    site.mkdir(parents=True, exist_ok=True)
    names = {s.id: s.name for s in sources}
    (site / "feed.xml").write_text(rss(records, today, site_url, names), encoding="utf-8")
    (site / "feed.json").write_text(json_feed(records, today, site_url, names), encoding="utf-8")
    for f in ("deprecations.json", "status.json"):
        shutil.copyfile(data / f, site / f)

    for s in sources:
        st = status["sources"][s.id]
        print(f"{s.id} {st['state']} {st['count']} {st['error'] or ''}".rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
