from pathlib import Path

from depfeed.parsers.gemini import parse
from depfeed.sources import SOURCES

TEXT = (Path(__file__).parent / "fixtures/gemini.md").read_text()
L = "https://example.com/l"
ROW = "No shutdown date announced"


def rec(aff):
    return next(r for r in parse(TEXT, L) if any(aff in a for a in r.affected))


def test_count():
    assert len(parse(TEXT, L)) >= 44  # 80% of 56


def test_undated_skipped():
    assert not any("gemini-4-neon" in a for r in parse(TEXT, L) for a in r.affected)


def test_deprecated_row():
    r = rec("gemini-3-pro-preview")
    assert r.shutdown == "2026-03-09" and r.replacement == "gemini-3.1-pro-preview"
    assert r.title.startswith("Model shutdown 2026-03-09:")


def test_multiline_cell():
    r = rec("gemini-omni-1.1-flash")
    assert r.shutdown == "2026-12-03"
    assert r.replacement.endswith("automatically routing API requests to gemini-omni-1.2-flash)")


def test_agent_rows():
    assert sum(r.title.startswith("Agent shutdown") for r in parse(TEXT, L)) == 2


def test_date_added_new_record():
    i = TEXT.index("`gemini-4-neon`")
    j = TEXT.index(ROW, i)
    new = parse(TEXT[:j] + "March 1, 2027" + TEXT[j + len(ROW):], L)
    assert len(new) == len(parse(TEXT, L)) + 1
    assert next(r for r in new if any("gemini-4-neon" in a for a in r.affected)).shutdown == "2027-03-01"


def test_ids_unique():
    ids = [r.id for r in parse(TEXT, L)]
    assert len(ids) == len(set(ids))


def test_all_dated():
    assert all(r.shutdown for r in parse(TEXT, L))


def test_source_wired():
    assert {x.id: x for x in SOURCES}["gemini"].parser is parse
