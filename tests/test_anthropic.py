from pathlib import Path

from depfeed.parsers.anthropic import parse
from depfeed.sources import SOURCES

TEXT = (Path(__file__).parent / "fixtures/anthropic.md").read_text()
L = "https://example.com/l"
P = "API parameter deprecation"


def test_count():
    assert len(parse(TEXT, L)) >= 17  # 80% of 21: 20 model rows + 1 parameter row


def test_known_row():
    r = next(r for r in parse(TEXT, L) if "claude-sonnet-4-5-20250929" in r.affected)
    assert r.announced == "2026-09-30" and r.shutdown == "2026-11-30"
    assert r.replacement == "claude-sonnet-5-5"
    assert r.title.startswith("Model retirement 2026-11-30:")


def test_parameter_row():
    [r] = [r for r in parse(TEXT, L) if r.title.startswith(P)]
    assert "temperature" in r.title and r.text
    assert r.announced is None and r.shutdown is None


def test_model_status_skipped():
    assert not [r for r in parse(TEXT, L) if "claude-fable-5-2" in r.affected]


def test_ids_unique():
    ids = [r.id for r in parse(TEXT, L)]
    assert len(ids) == len(set(ids))


def test_all_dated_or_skipped():
    assert all(r.announced or r.shutdown for r in parse(TEXT, L) if not r.title.startswith(P))


def test_source_wired():
    assert next(s for s in SOURCES if s.id == "anthropic").parser is parse
