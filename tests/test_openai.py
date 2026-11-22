from pathlib import Path

from depfeed.parsers.openai import parse
from depfeed.sources import SOURCES

TEXT = (Path(__file__).parent / "fixtures/openai.md").read_text()
L = "https://example.com/l"
FLOOR = 124  # 80% of the real count (156)


def test_parses_many():
    assert len(parse(TEXT, L)) >= FLOOR


def test_known_row():
    r = next(r for r in parse(TEXT, L) if "gpt-5-mini" in r.affected)
    assert r.shutdown == "2026-12-11" and r.announced == "2026-06-11"
    assert r.replacement == "gpt-6.1-terra"
    assert r.source == "openai" and r.kind == "parsed" and r.url == L
    assert r.title.startswith("Model shutdown 2026-12-11:")


def test_all_dated():
    assert all(r.announced or r.shutdown for r in parse(TEXT, L))


def test_all_have_notice_date():
    assert all(r.announced for r in parse(TEXT, L))


def test_ids_unique():
    ids = [r.id for r in parse(TEXT, L)]
    assert len(ids) == len(set(ids))


def test_no_tables_returns_empty():
    assert parse("# Title\ntext", L) == []


def test_ids_stable_when_replacement_edited():
    edited = TEXT.replace("`gpt-6.1-terra`", "`something-else`", 1)
    assert edited != TEXT
    assert {r.id for r in parse(edited, L)} == {r.id for r in parse(TEXT, L)}


def test_source_wired():
    assert next(s for s in SOURCES if s.id == "openai").parser is parse


def test_feature_row_wording():
    r = next(r for r in parse(TEXT, L) if "EU data residency" in r.title)
    assert r.title.startswith(
        "Feature/endpoint shutdown 2027-01-11: GPT-5.2, GPT-5.4, and GPT-5.4 mini")
    assert r.affected == [r.title.split(": ", 1)[1]]
    assert r.status == "Deprecated" and r.announced == "2026-11-18"


def test_title_prefixes():
    ps = ("Feature/endpoint shutdown", "Model shutdown", "Shutdown")
    rs = parse(TEXT, L)
    assert all(r.title.startswith(ps) for r in rs)
    assert all(any(r.title.startswith(p + " ") for r in rs) for p in ps)


def test_row_links():
    rs = parse(TEXT, "https://developers.openai.com/api/docs/deprecations")
    p = next(r for r in rs if "/v1/prompts" in r.title)
    assert p.links == ["Migration guide: https://developers.openai.com/api/docs/guides/prompting/migrate-from-prompt-object"]
    e = next(r for r in rs if "Evals dashboard" in r.title)
    assert "fine-tuning timeline: https://developers.openai.com/api/docs/deprecations#update-to-openais-self-serve-fine-tuning" in e.links
    assert sum(bool(r.links) for r in rs) == 13


def test_ids_unchanged_by_links():
    rs = parse(TEXT, "https://developers.openai.com/api/docs/deprecations")
    assert any(r.id == "3670570fd58e48cb" for r in rs)


def test_link_text_plain():
    rs = parse(TEXT, "https://developers.openai.com/api/docs/deprecations")
    t = next(r for r in rs if "/v1/audio/translations" in r.title)
    assert t.links == ["/v1/realtime/translations: https://developers.openai.com/api/docs/guides/realtime-translation"]
