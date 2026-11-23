import json
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from email.utils import format_datetime

from depfeed.records import Record, feed_date

WINDOW_DAYS = 183
TITLE = "AI model deprecations"
DESC = "Deprecation and retirement announcements from AI providers"


def in_window(records: list[Record], today: str) -> list[Record]:
    cutoff = (date.fromisoformat(today) - timedelta(days=WINDOW_DAYS)).isoformat()
    rs = sorted(records, key=lambda r: r.id)
    rs = [r for r in rs if feed_date(r) >= cutoff and not (r.baseline and not r.announced)]
    rs.sort(key=feed_date, reverse=True)  # stable: id asc kept within equal dates
    return rs


def _title(r: Record, names: dict[str, str]) -> str:
    return f"[{names.get(r.source, r.source)}] {r.title}"


def _desc(r: Record) -> str:
    if r.kind == "parsed":
        return "\n".join([
            f"Affected: {', '.join(r.affected)}",
            f"Shutdown: {r.shutdown or 'not set'}",
            *([f"Status: {r.status}"] if r.status else []),
            f"Replacement: {r.replacement or 'none'}",
            *([f"Details: {r.text}"] if r.text else []),
            *[f"Docs: {x}" for x in r.links],
            f"Source: {r.url}",
        ])
    return f"{r.text or ''}\n\nSource: {r.url}"


def _dt(iso: str) -> datetime:
    return datetime.combine(date.fromisoformat(iso), datetime.min.time(), tzinfo=timezone.utc)


def _pub(r: Record) -> datetime:
    return datetime.fromisoformat(r.seen_at) if r.seen_at else _dt(feed_date(r))


def rss(records: list[Record], today: str, site_url: str, names: dict[str, str]) -> str:
    root = ET.Element("rss", version="2.0")
    ch = ET.SubElement(root, "channel")
    for tag, text in [("title", TITLE), ("link", site_url), ("description", DESC),
                      ("lastBuildDate", format_datetime(_dt(today)))]:
        ET.SubElement(ch, tag).text = text
    for r in in_window(records, today):
        it = ET.SubElement(ch, "item")
        ET.SubElement(it, "title").text = _title(r, names)
        ET.SubElement(it, "link").text = f"{r.url}#{r.id}"
        ET.SubElement(it, "guid", isPermaLink="false").text = r.id
        ET.SubElement(it, "pubDate").text = format_datetime(_pub(r))
        ET.SubElement(it, "description").text = _desc(r)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode()


def json_feed(records: list[Record], today: str, site_url: str, names: dict[str, str]) -> str:
    items = []
    for r in in_window(records, today):
        item = {"id": r.id, "url": f"{r.url}#{r.id}", "title": _title(r, names),
                "content_text": _desc(r), "date_published": r.seen_at or f"{feed_date(r)}T00:00:00Z"}
        if r.updated:
            item["date_modified"] = f"{r.updated}T00:00:00Z"
        item["tags"] = [r.source, r.kind]
        items.append(item)
    feed = {"version": "https://jsonfeed.org/version/1.1", "title": TITLE,
            "home_page_url": site_url, "feed_url": f"{site_url}/feed.json", "items": items}
    return json.dumps(feed, indent=1, ensure_ascii=False) + "\n"
