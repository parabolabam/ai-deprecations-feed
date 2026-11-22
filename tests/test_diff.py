import time

from depfeed.diff import MAX_DIFF_CHARS, diff_record
from depfeed.sources import Source

KEEP = r"(?i)end of life|deprecat|retire|sunset|shut ?down"


def src(keep=None):
    return Source("xai", "xAI", ("u",), "https://x.ai/l", keep=keep)


def test_diff_first_run_none():
    assert diff_record(src(), None, "a\nb", "2026-01-01") is None


def test_diff_added_lines_only():
    r = diff_record(src(), "keep\nremoved", "keep\nadded", "2026-01-01")
    assert r.text == "added" and "removed" not in r.text
    assert r.kind == "raw" and r.title == "xAI: page changed" and r.url == "https://x.ai/l"


def test_diff_only_removals_none():
    assert diff_record(src(), "a\nb", "a", "2026-01-01") is None


def test_diff_unchanged_none():
    assert diff_record(src(), "a\nb", "a\nb", "2026-01-01") is None


def test_diff_keep_filter():
    new = "a\nNew grok-5 pricing\ngrok-3 end of life on Jan 1, 2027"
    r = diff_record(src(KEEP), "a", new, "2026-01-01")
    assert r.text == "grok-3 end of life on Jan 1, 2027"
    assert diff_record(src(KEEP), "a", "a\nNew pricing", "2026-01-01") is None


def test_diff_cap():
    r = diff_record(src(), "a", "a\n" + "x" * 10_000, "2026-01-01")
    assert len(r.text) <= MAX_DIFF_CHARS + len("\n…(truncated)")
    assert r.text.endswith("…(truncated)")


def test_diff_large_input_fast():
    old = [f"line {i}" for i in range(3000)]
    new = list(old)
    for i in range(0, 3000, 300):
        new[i] = f"changed {i}"
    t = time.time()
    r = diff_record(src(), "\n".join(old), "\n".join(new), "2026-01-01")
    assert time.time() - t < 2
    assert r.text.count("\n") == 9
