from pathlib import Path

from depfeed.parsers.groq import parse
from depfeed.sources import SOURCES

TEXT = (Path(__file__).parent / "fixtures/groq.md").read_text()
L = "https://example.com/l"


def test_count():
    assert len(parse(TEXT, L)) >= 32  # 80% of 40 rows


def test_known_row():
    r = next(r for r in parse(TEXT, L) if "groq/compound" in r.affected)
    assert r.announced == "2026-08-24" and r.shutdown == "2026-09-21"
    assert r.replacement is None


def test_emailed_announce():
    r = next(r for r in parse(TEXT, L) if "llama-3.1-8b-instant" in r.affected)
    assert r.announced == "2026-06-17" and r.shutdown == "2026-08-16"


def test_model_id_header():  # older "Model ID | ..." tables
    r = next(r for r in parse(TEXT, L) if "mixtral-8x7b-32768" in r.affected)
    assert r.shutdown == "2025-03-20"


def test_ids_unique():
    ids = [r.id for r in parse(TEXT, L)]
    assert len(ids) == len(set(ids))


def test_all_dated():
    assert all(r.shutdown for r in parse(TEXT, L))


def test_source_wired():
    assert next(s for s in SOURCES if s.id == "groq").parser is parse
