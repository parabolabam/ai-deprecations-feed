from pathlib import Path

from depfeed.parsers.azure import parse
from depfeed.sources import SOURCES

TEXT = (Path(__file__).parent / "fixtures/azure.md").read_text()
L = "https://example.com/l"
ROW = "| codex-mini | 2025-05-16 | Deprecated | 2026-11-17 | — |"


def rec(text, aff):
    return next(r for r in parse(text, L) if r.affected == [aff] and r.title.startswith("Model retirement"))


def test_count():
    assert len(parse(TEXT, L)) >= 138  # 80% of 173 (169 - 2 undated + 6 fine-tuned)


def test_known_row():
    r = rec(TEXT, "codex-mini 2025-05-16")
    assert r.status == "Deprecated" and r.shutdown == "2026-11-17" and r.replacement is None
    assert r.title.startswith("Model retirement 2026-11-17: Azure OpenAI: codex-mini 2025-05-16")


def test_lifecycle_change_new_id():
    assert ROW in TEXT
    assert rec(TEXT.replace(ROW, ROW.replace("Deprecated", "GA")), "codex-mini 2025-05-16").id \
        != rec(TEXT, "codex-mini 2025-05-16").id


def test_retirement_change_same_id():
    r = rec(TEXT.replace(ROW, ROW.replace("2026-11-17", "2026-12-17")), "codex-mini 2025-05-16")
    assert r.id == rec(TEXT, "codex-mini 2025-05-16").id and r.shutdown == "2026-12-17"


def test_fine_tuned():
    r = next(r for r in parse(TEXT, L)
             if r.title.startswith("Fine-tuned deployment retirement") and r.affected == ["gpt-4.1 2025-04-14"])
    assert r.shutdown == "2027-10-14" and r.status is None
    assert r.id != rec(TEXT, "gpt-4.1 2025-04-14").id


def test_undated_skipped():
    assert not any(r.affected == ["Mistral-Large-3 1"] for r in parse(TEXT, L))


def test_ids_unique():
    ids = [r.id for r in parse(TEXT, L)]
    assert len(ids) == len(set(ids))


def test_all_dated():
    assert all(r.shutdown for r in parse(TEXT, L))


def test_source_wired():
    assert next(s for s in SOURCES if s.id == "azure").parser is parse
