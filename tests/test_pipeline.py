from dataclasses import replace

from depfeed.fetch import FetchError
from depfeed.pipeline import check, process
from depfeed.records import Record
from depfeed.sources import Source

T = "2026-01-10"
OLD = "\n".join(f"line {i}" for i in range(200))
NEW = OLD + "\nnew line"
DIFF_SRC = Source("s", "S", ("u",), "http://l")


def rec(title="t", announced="2026-01-01", shutdown=None):
    return Record(id=title, source="s", kind="parsed", title=title, url="u",
                  announced=announced, shutdown=shutdown)


def parser_returning(n):
    return replace(DIFF_SRC, parser=lambda text, link: [rec(f"t{i}") for i in range(n)])


def ok(text):
    return lambda src: text


def prev(state, count=10, since="2026-01-01", error=None):
    return {"state": state, "since": since, "changed": "2026-01-01",
            "count": count, "error": error}


def kinds(res):
    return [r.kind for r in res.extra]


def test_check_rules():
    assert check([], 0) == "no records"
    assert check([rec()], 10) == "count dropped from 10 to 1"
    assert check([rec(), rec("x", announced=None)], 0) == "record without date: x"
    assert check([rec(), rec("y", announced=None, shutdown="2026-02-01")], 0) is None


def test_fetch_error_keeps_snapshot_and_emits_health():
    def boom(src):
        raise FetchError("HTTP 500")
    r = process(DIFF_SRC, OLD, prev("diff", 0), boom, T)
    assert r.snapshot is None and r.parsed is None
    assert r.status["state"] == "fetch_broken" and r.status["error"] == "HTTP 500"
    assert kinds(r) == ["health"]
    assert r.extra[0].title == "Источник S не отдаёт данные"


def test_shrunk_page_is_fetch_broken():
    r = process(DIFF_SRC, "x" * 2000, None, ok("y" * 900), T)
    assert r.status["state"] == "fetch_broken" and r.snapshot is None
    assert r.status["error"] == "page shrank from 2000 to 900 chars"


def test_too_short_page_is_fetch_broken():
    r = process(DIFF_SRC, None, None, ok("z" * 100), T)
    assert r.status["state"] == "fetch_broken" and r.snapshot is None
    assert r.status["error"] == "page too short: 100 chars"


def test_unchanged_diff_source_skips():
    r = process(DIFF_SRC, OLD, prev("diff", 0), ok(OLD), T)
    assert r.extra == [] and r.snapshot is None and r.parsed is None
    assert r.status["state"] == "diff"


def test_unchanged_parser_source_reparses():
    r = process(parser_returning(3), OLD, prev("ok", 3), ok(OLD), T)
    assert r.status["state"] == "ok" and len(r.parsed) == 3
    assert r.extra == [] and r.snapshot is None


def test_recovery_from_fetch_broken_same_text():
    r = process(DIFF_SRC, OLD, prev("fetch_broken", 0), ok(OLD), T)
    assert r.status["state"] == "diff" and r.extra == [] and r.status["error"] is None


def test_parser_ok():
    r = process(parser_returning(3), OLD, prev("ok", 3), ok(NEW), T)
    assert len(r.parsed) == 3 and r.snapshot == NEW and r.extra == []
    assert r.status["state"] == "ok" and r.status["count"] == 3
    assert r.status["changed"] == T and r.status["error"] is None


def test_parser_zero_records_breaks():
    r = process(parser_returning(0), OLD, prev("ok"), ok(NEW), T)
    assert r.parsed is None and r.snapshot == NEW
    assert r.status["state"] == "parser_broken" and r.status["count"] == 10
    assert r.status["error"] == "no records"
    assert kinds(r) == ["raw", "health"]
    assert r.extra[1].title == "Парсер источника S сломан"


def test_parser_drop_half_breaks():
    r = process(parser_returning(4), OLD, prev("ok"), ok(NEW), T)
    assert r.parsed is None and r.status["state"] == "parser_broken"
    assert r.status["error"] == "count dropped from 10 to 4"


def test_parser_exception_breaks():
    def bad(text, link):
        raise ValueError("oops")
    r = process(replace(DIFF_SRC, parser=bad), OLD, prev("ok"), ok(NEW), T)
    assert r.status["state"] == "parser_broken"
    assert r.status["error"] == "parser exception: ValueError: oops"


def test_health_only_on_transition():
    r = process(parser_returning(0), OLD, prev("parser_broken"), ok(NEW), T)
    assert r.status["state"] == "parser_broken" and kinds(r) == ["raw"]


def test_unchanged_keeps_parser_broken():
    r = process(parser_returning(0), OLD, prev("parser_broken", error="no records"),
                ok(OLD), T)
    assert r.status["state"] == "parser_broken" and r.status["error"] == "no records"
    assert r.extra == [] and r.snapshot is None


def test_parser_broken_survives_fetch_blip():
    src = parser_returning(0)
    r1 = process(src, OLD, prev("ok"), ok(NEW), T)
    assert r1.status["state"] == "parser_broken"

    def boom(s):
        raise FetchError("HTTP 500")
    r2 = process(src, OLD, r1.status, boom, T)
    assert r2.status["state"] == "fetch_broken"
    r3 = process(src, NEW, r2.status, ok(NEW), T)
    assert r3.status["state"] == "parser_broken"


def test_parser_added_to_existing_snapshot():
    r = process(parser_returning(3), OLD, prev("diff", 0), ok(OLD), T)
    assert r.status["state"] == "ok" and r.parsed is not None
    assert r.status["count"] == len(r.parsed)


def test_parser_fixed_with_unchanged_page():
    r = process(parser_returning(10), OLD, prev("parser_broken", error="x"), ok(OLD), T)
    assert r.status["state"] == "ok" and r.extra == []


def test_first_run_diff_source():
    r = process(DIFF_SRC, None, None, ok(OLD), T)
    assert r.snapshot == OLD and r.extra == []
    assert r.status["state"] == "diff" and r.status["changed"] == T


def test_since_kept_when_state_same():
    r = process(DIFF_SRC, OLD, prev("diff", 0, since="2025-12-01"), ok(NEW), T)
    assert r.status["since"] == "2025-12-01"
    r = process(DIFF_SRC, OLD, prev("fetch_broken", 0, since="2025-12-01"), ok(NEW), T)
    assert r.status["since"] == T


def test_pipeline_first_parse_is_baseline():
    assert process(parser_returning(3), OLD, None, ok(NEW), T).baseline
    assert process(parser_returning(3), OLD, prev("diff", 0), ok(NEW), T).baseline
    assert not process(parser_returning(80), OLD, prev("ok", 156), ok(NEW), T).baseline
