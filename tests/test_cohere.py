from pathlib import Path

from depfeed.parsers.cohere import parse
from depfeed.sources import SOURCES

TEXT = (Path(__file__).parent / "fixtures/cohere.md").read_text()
L = "https://example.com/l"


def test_count():
    assert len(parse(TEXT, L)) == 5


def test_embed_aya():
    r = next(r for r in parse(TEXT, L) if r.shutdown == "2026-04-04")
    assert {"embed-english-v2.0", "c4ai-aya-expanse-8b"} <= set(r.affected)
    assert r.text.startswith("Effective April 4th, 2026")


def test_stops_at_best_practices():
    rs = parse(TEXT, L)
    assert len(rs) == 5 and not any("Best Practices" in r.title for r in rs)


def test_invariants():
    rs = parse(TEXT, L)
    assert all(r.announced is None and len(r.text) <= 1500 for r in rs)
    assert len({r.id for r in rs}) == len(rs)


def test_wired():
    assert next(s for s in SOURCES if s.id == "cohere").parser is parse
