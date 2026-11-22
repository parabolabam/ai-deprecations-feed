from pathlib import Path

from depfeed.parsers.vertex import parse
from depfeed.sources import SOURCES

TEXT = (Path(__file__).parent / "fixtures/vertex.md").read_text()
L = "https://example.com/l"
ROW = "No retirement date announced"


def rec(aff):
    return next(r for r in parse(TEXT, L) if aff in r.affected)


def test_count():
    assert len(parse(TEXT, L)) >= 43  # 80% of 54


def test_known_row():
    r = rec("veo-3.0-generate-001")
    assert r.shutdown == "2026-06-30" and r.replacement == "veo-3.1-generate-001"
    assert r.title.startswith("Model retirement 2026-06-30:")


def test_undated_skipped():
    assert not any("gemini-4-hydrogen" in r.affected for r in parse(TEXT, L))


def test_feature_row():
    r = rec("Generative AI module in the Vertex AI SDK")
    assert r.affected == ["Generative AI module in the Vertex AI SDK"]
    assert r.announced == "2025-06-24" and r.shutdown == "2026-06-24"
    assert r.text.startswith("Starting on June 24, 2025")


def test_date_added_new_record():
    line = next(x for x in TEXT.splitlines() if "gemini-4-hydrogen" in x)
    assert ROW in line
    new = parse(TEXT.replace(line, line.replace(ROW, "March 1, 2027")), L)
    r = next(r for r in new if "gemini-4-hydrogen" in r.affected)
    assert len(new) == len(parse(TEXT, L)) + 1 and r.shutdown == "2027-03-01"


def test_ids_unique():
    ids = [r.id for r in parse(TEXT, L)]
    assert len(ids) == len(set(ids))


def test_all_dated():
    assert all(r.shutdown for r in parse(TEXT, L))


def test_source_wired():
    s = {x.id: x for x in SOURCES}
    assert s["vertex"].parser is parse and len(s["vertex"].urls) == 2
    assert s["vertex-partners"].parser is None and len(s["vertex-partners"].urls) == 1


def test_footnote_marker_stripped():
    rs = parse(TEXT, L)
    assert any(r.affected == ["textembedding-gecko@003"] for r in rs)
    assert not any("\\" in a for r in rs for a in r.affected)
