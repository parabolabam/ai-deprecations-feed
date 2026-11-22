import json
from pathlib import Path

import pytest

from depfeed.parsers.openai import parse
from depfeed.parsers.tables import TableSpec, markdoc_tables, parse_tables

FIX = Path(__file__).parent / "fixtures"
L = "https://x.test/p"
COLS = {"feature": "affected", "shutdown": "shutdown", "notice": "announced"}


def run(text, **kw):
    spec = TableSpec(("feature",), COLS, "P", **kw)
    return parse_tables(text, L, "s", [spec])


def test_openai_ids_frozen():
    rs = parse((FIX / "openai.md").read_text(), "https://developers.openai.com/api/docs/deprecations")
    assert {r.id: r.title for r in rs} == json.loads((FIX / "openai_ids.json").read_text())


def test_bold_headers():
    rs = run("| **Feature** | **Shutdown date** |\n|---|---|\n| a | Jan 5, 2027 |")
    assert rs[0].shutdown == "2027-01-05" and rs[0].affected == ["a"]


def test_heading_unwrap_and_tags():
    t = "### [Jan 5, 2027: x](#a) {% id=\"x\" %}\n| Feature | Shutdown |\n|---|---|\n| a | Jan 5, 2027 |"
    r = run(t, id_fields=("section", "affected"))[0]
    assert r.title == "P 2027-01-05: Jan 5, 2027: x: a"


def test_heading_date():
    t = "### Jan 5, 2027\n| Feature |\n|---|\n| a |"
    assert run(t, heading_date="announced")[0].announced == "2027-01-05"


def test_body_announced():
    t = "## S\nNotice sent on Mar 3, 2026.\n| Feature | Shutdown |\n|---|---|\n| a | Apr 1, 2026 |"
    assert run(t, body_announced=r"sent on ([A-Za-z]+ \d+, \d{4})")[0].announced == "2026-03-03"


def test_skip_undated():
    t = "| Feature | Shutdown |\n|---|---|\n| a | No shutdown date announced |\n| b | Apr 1, 2026 |"
    assert [r.affected for r in run(t, skip_undated=True)] == [["b"]]


def test_require_date():
    with pytest.raises(ValueError):
        run("| Feature | Shutdown |\n|---|---|\n| a | soon |")


def test_markdoc_tables():
    t = "x\n{% table %}\n* A\n* B\n---\n* 1\n*\n---\n* 2\n* 3\n{% /table %}\ny"
    assert markdoc_tables(t) == "x\n| A | B |\n|---|---|\n| 1 |  |\n| 2 | 3 |\ny"
