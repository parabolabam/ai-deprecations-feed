import json
import xml.etree.ElementTree as ET
from datetime import date, timedelta

from depfeed.feeds import in_window, json_feed, rss
from depfeed.records import Record

TODAY = "2026-11-22"
SITE = "https://example.com"


def ago(n):
    return (date.fromisoformat(TODAY) - timedelta(days=n)).isoformat()


def raw(id, days, **kw):
    return Record(id=id, source="openai", kind="raw", title="T " + id, url="http://x/" + id,
                  text="body", first_seen=ago(days), **kw)


def test_window():
    assert [r.id for r in in_window([raw("a", 100), raw("b", 200)], TODAY)] == ["a"]


def test_window_uses_announced():
    r = Record(id="p", source="openai", kind="parsed", title="t", url="u",
               announced="2023-05-01", first_seen=TODAY)
    assert in_window([r], TODAY) == []


def test_window_sorted_desc():
    rs = [raw("b", 10), raw("a", 10), raw("c", 5), raw("d", 20)]
    assert [r.id for r in in_window(rs, TODAY)] == ["c", "a", "b", "d"]


def test_rss_parses():
    rs = [raw("a", 1), Record(id="p", source="openai", kind="parsed", title="t", url="u",
                              announced=ago(2), affected=["m1"])]
    root = ET.fromstring(rss(rs, TODAY, SITE, {"openai": "OpenAI"}).encode())
    items = root.findall("channel/item")
    assert len(items) == 2
    g = items[0].find("guid")
    assert g.text == "a" and g.get("isPermaLink") == "false"
    assert items[0].find("title").text.startswith("[OpenAI]")
    assert "Shutdown: not set" in items[1].find("description").text


def test_json_feed_valid():
    rs = [raw("a", 1, updated=ago(0)), raw("b", 2)]
    d = json.loads(json_feed(rs, TODAY, SITE, {}))
    assert d["version"] == "https://jsonfeed.org/version/1.1"
    a, b = d["items"]
    assert a["date_modified"] == f"{TODAY}T00:00:00Z" and "date_modified" not in b
    assert a["tags"] == ["openai", "raw"]
