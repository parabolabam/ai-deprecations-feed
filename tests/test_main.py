import json
from pathlib import Path

from depfeed.__main__ import main
from depfeed.sources import SOURCES

FIX = (Path(__file__).parent / "fixtures" / "openai.md").read_text()
OTHER = {s.id: "\n".join(f"{s.id} line {i}" for i in range(200)) for s in SOURCES}
TUE = "2026-11-24"


def run(tmp_path, today=TUE, **override):
    texts = {**OTHER, "openai": FIX, **override}
    assert main(["--data", str(tmp_path / "data"), "--site", str(tmp_path / "site"),
                 "--today", today], fetch=lambda s: texts[s.id]) == 0


def records(tmp_path):
    return json.loads((tmp_path / "data" / "deprecations.json").read_text())["records"]


def status(tmp_path):
    return json.loads((tmp_path / "data" / "status.json").read_text())


def test_e2e_first_run(tmp_path):
    run(tmp_path)
    site = tmp_path / "site"
    assert {p.name for p in site.iterdir()} == {"feed.xml", "feed.json", "deprecations.json", "status.json"}
    items = json.loads((site / "feed.json").read_text())["items"]
    st = status(tmp_path)["sources"]
    assert st["openai"]["state"] == "ok" and st["openai"]["count"] == 156
    assert [s for s in st if st[s]["state"] == "diff"].__len__() == 8
    assert not [r for r in records(tmp_path) if r["kind"] == "raw"]
    assert not [i for i in items if i["tags"][0] == "openai"
                and i["date_published"].startswith(TUE)]


def test_e2e_second_run_no_change_no_file_change(tmp_path):
    run(tmp_path)
    snap = lambda: {p: p.read_bytes() for p in (tmp_path / "data").rglob("*") if p.is_file()}
    before = snap()
    run(tmp_path)
    assert snap() == before


def test_e2e_parser_break_keeps_records(tmp_path):
    broken = FIX.replace("|", "")
    assert len(broken) >= len(FIX) / 2
    run(tmp_path)
    run(tmp_path, "2026-11-25", openai=broken)
    for day in ("2026-11-25", "2026-11-26"):
        if day == "2026-11-26":
            run(tmp_path, day, openai=broken)
        rs = [r for r in records(tmp_path) if r["source"] == "openai"]
        k = lambda kind: [r for r in rs if r["kind"] == kind]
        assert len(k("parsed")) == 156 and len(k("raw")) == 1 and len(k("health")) == 1
        assert status(tmp_path)["sources"]["openai"]["state"] == "parser_broken"


def test_e2e_diff_source_change(tmp_path):
    run(tmp_path)
    run(tmp_path, "2026-11-25", anthropic=OTHER["anthropic"] + "\nbrand new line")
    raw = [r for r in records(tmp_path) if r["kind"] == "raw" and r["source"] == "anthropic"]
    assert len(raw) == 1 and raw[0]["text"].strip() == "brand new line"


def test_heartbeat_monday(tmp_path):
    run(tmp_path, "2026-11-23")
    assert status(tmp_path)["heartbeat"] == "2026-11-23"
    t = tmp_path / "t"
    t.mkdir()
    run(t)
    assert status(t)["heartbeat"] is None


def test_e2e_switch_from_diff_no_flood(tmp_path):
    from dataclasses import replace

    from depfeed.records import Record
    from depfeed.sources import Source
    s1 = Source("x", "X", ("u",), "http://x")
    text = "\n".join(f"line {i}" for i in range(200))
    day2 = "2026-11-25"

    def rec(i, **kw):
        return Record(id=f"r{i}", source="x", kind="parsed", title=f"t{i}", url="u", **kw)

    def fn(t, link):
        return [rec(0, shutdown="2027-01-01"), rec(1, shutdown="2027-01-01"),
                rec(2, shutdown="2027-01-01"), rec(3, announced="2026-11-15")]

    def go(today, src):
        assert main(["--data", str(tmp_path / "data"), "--site", str(tmp_path / "site"),
                     "--today", today], fetch=lambda s: text, sources=[src]) == 0

    go(TUE, s1)
    go(day2, replace(s1, parser=fn))
    items = json.loads((tmp_path / "site" / "feed.json").read_text())["items"]
    assert [i["title"] for i in items if i["tags"][0] == "x"] == ["[X] t3"]
