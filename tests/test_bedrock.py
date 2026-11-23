from pathlib import Path

from depfeed.parsers.bedrock import parse
from depfeed.sources import SOURCES

TEXT = (Path(__file__).parent / "fixtures/bedrock.md").read_text()
L = "https://example.com/l"
HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"


def by(**kw):
    return [r for r in parse(TEXT, L) if all(getattr(r, k) == v for k, v in kw.items())]


def test_count():
    assert len(parse(TEXT, L)) >= 42  # 80% of 53


def test_haiku_legacy():
    r = next(r for r in by(status="Legacy") if HAIKU in r.affected)
    assert r.shutdown == "2026-11-13" and r.announced is None
    assert "2026-10-10" in r.text and "ca-central-1" in r.text


def test_jamba():
    r = next(r for r in parse(TEXT, L) if "ai21.jamba-1-5-large-v1:0" in r.affected)
    assert r.shutdown == "2026-11-26" and r.status == "Legacy"


def test_haiku_eol_reached():
    r = next(r for r in by(status="EOL reached") if HAIKU in r.affected)
    assert r.shutdown == "2026-09-10"


def test_nova_canvas():
    assert next(r for r in parse(TEXT, L) if "amazon.nova-canvas-v1:0" in r.affected).status == "EOL reached"


def test_deepseek_two_ids():
    assert any(r.affected == ["deepseek.v3-v1:0", "deepseek.v3.1"] for r in parse(TEXT, L))


def test_invariants():
    rs = parse(TEXT, L)
    assert all(r.announced is None and r.shutdown for r in rs)
    assert len({r.id for r in rs}) == len(rs)


def test_wired():
    assert next(s for s in SOURCES if s.id == "bedrock").parser is parse
