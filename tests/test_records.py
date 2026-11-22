from datetime import date, timedelta

from depfeed.records import Record, load_records, merge, prune, record_id, save_records

TODAY = "2026-11-22"


def rec(id="x", **kw):
    return Record(id=id, source="s", kind=kw.pop("kind", "parsed"), title="t", url="u", **kw)


def ago(n):
    return (date.fromisoformat(TODAY) - timedelta(days=n)).isoformat()


def test_merge_new_sets_first_seen():
    (r,) = merge([], [rec()], TODAY)
    assert r.first_seen == TODAY and r.updated is None


def test_merge_edit_updates_in_place():
    old = rec(first_seen="2026-01-01", replacement="a")
    out = merge([old], [rec(replacement="b")], TODAY)
    assert len(out) == 1
    assert out[0].replacement == "b"
    assert out[0].first_seen == "2026-01-01" and out[0].updated == TODAY


def test_merge_unchanged_keeps_updated_none():
    old = rec(first_seen="2026-01-01")
    (r,) = merge([old], [rec()], TODAY)
    assert r == old and r.updated is None


def test_merge_keeps_records_missing_from_page():
    out = merge([rec("a", first_seen="2026-01-01")], [rec("b")], TODAY)
    assert {r.id for r in out} == {"a", "b"}


def test_prune_raw_90_days():
    rs = [
        rec("old", kind="raw", first_seen=ago(91)),
        rec("new", kind="raw", first_seen=ago(89)),
        rec("edge", kind="raw", first_seen=ago(90)),
        rec("h", kind="health", first_seen=ago(91)),
        rec("p", kind="parsed", first_seen="2023-01-01"),
    ]
    assert {r.id for r in prune(rs, TODAY)} == {"new", "edge", "p"}


def test_save_load_roundtrip_stable(tmp_path):
    rs = [rec("b", announced="2026-02-01", affected=["m"]), rec("a", first_seen="2026-03-01", text="é")]
    p1, p2 = tmp_path / "x/a.json", tmp_path / "b.json"
    save_records(p1, rs)
    save_records(p2, load_records(p1))
    assert p1.read_bytes() == p2.read_bytes()
    assert load_records(tmp_path / "none.json") == []


def test_record_id_stable():
    assert record_id("a", "b") == record_id("a", "b")
    assert len(record_id("a", "b")) == 16
    assert record_id("a", "b") != record_id("a", "c")


def test_merge_keeps_baseline_no_update():
    old = rec(first_seen="2026-01-01", baseline=True)
    (r,) = merge([old], [rec()], TODAY)
    assert r == old and r.updated is None and r.baseline
    (r,) = merge([old], [rec(replacement="b")], TODAY)
    assert r.updated == TODAY and r.baseline
