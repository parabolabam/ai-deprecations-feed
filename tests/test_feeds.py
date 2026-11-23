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


def test_links_have_id_fragment():
    rs = [raw("a", 1)]
    item = ET.fromstring(rss(rs, TODAY, SITE, {}).encode()).find("channel/item")
    assert item.find("link").text.endswith("#a")
    assert json.loads(json_feed(rs, TODAY, SITE, {}))["items"][0]["url"].endswith("#a")


def test_status_line():
    def desc(**kw):
        r = Record(id="p", source="openai", kind="parsed", title="t", url="u",
                   announced=ago(1), **kw)
        return json.loads(json_feed([r], TODAY, SITE, {}))["items"][0]["content_text"]
    assert "Status: Deprecated" in desc(status="Deprecated")
    assert "Status:" not in desc()


def test_docs_and_source_lines():
    def desc(r):
        return json.loads(json_feed([r], TODAY, SITE, {}))["items"][0]["content_text"]
    p = Record(id="p", source="openai", kind="parsed", title="t", url="https://p",
               announced=ago(1), links=["Guide: https://x/y"])
    lines = desc(p).split("\n")
    assert "Docs: Guide: https://x/y" in lines and lines[-1] == "Source: https://p"
    r = Record(id="r", source="openai", kind="raw", title="t", url="https://p",
               text="added line", first_seen=ago(1))
    assert desc(r) == "added line\n\nSource: https://p"


def test_window_drops_undated_baseline():
    def p(id, **kw):
        return Record(id=id, source="x", kind="parsed", title="t", url="u",
                      first_seen=TODAY, baseline=True, **kw)
    assert [r.id for r in in_window([p("a"), p("b", announced=ago(10))], TODAY)] == ["b"]


def test_details_line():
    r = Record(id="p", source="openai", kind="parsed", title="t", url="u",
               announced=TODAY, text="why")
    assert "Details: why" in json.loads(json_feed([r], TODAY, SITE, {}))["items"][0]["content_text"]


def _seen_pair():
    return [raw("a", 1, seen_at="2026-11-23T10:15:00Z"), raw("b", 2)]


def test_rss_pubdate_uses_seen_at():
    items = ET.fromstring(rss(_seen_pair(), TODAY, SITE, {}).encode()).findall("channel/item")
    assert items[0].find("pubDate").text == "Mon, 23 Nov 2026 10:15:00 +0000"
    assert items[1].find("pubDate").text == "Fri, 20 Nov 2026 00:00:00 +0000"


def test_json_feed_date_published_uses_seen_at():
    a, b = json.loads(json_feed(_seen_pair(), TODAY, SITE, {}))["items"]
    assert a["date_published"] == "2026-11-23T10:15:00Z"
    assert b["date_published"] == f"{ago(2)}T00:00:00Z"
