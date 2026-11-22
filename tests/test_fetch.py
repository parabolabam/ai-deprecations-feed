import http.client
import io
import os
import urllib.error
from email.message import Message

import pytest

from depfeed import fetch as F
from depfeed.fetch import FetchError, fetch, fetch_source, normalize
from depfeed.sources import SOURCES


class Resp:
    def __init__(self, body, ctype="text/markdown"):
        self.body = body.encode()
        self.headers = {"Content-Type": ctype}

    def read(self):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def test_normalize_idempotent():
    s = "a\t&amp;quot;b&amp;quot;\n\n\n  c   d  \n"
    out = normalize(s)
    assert normalize(out) == out
    assert '"' in out and "&quot;" not in out


def test_normalize_strips_front_matter_and_whitespace():
    assert normalize("---\nms.date: 1\n---\n  a   b \n\n c") == "a b\nc"


def test_normalize_ignore():
    assert normalize("x\nLast updated 2026\ny", (r"^Last updated",)) == "x\ny"


def test_fetch_rejects_html(monkeypatch):
    monkeypatch.setattr(F.urllib.request, "urlopen",
                        lambda *a, **k: Resp("<!DOCTYPE html><html></html>", "text/html; charset=utf-8"))
    with pytest.raises(FetchError):
        fetch("https://example.com/x")


def test_fetch_retries_once_on_503(monkeypatch):
    calls = []

    def fake(*a, **k):
        calls.append(1)
        if len(calls) == 1:
            raise urllib.error.HTTPError("u", 503, "x", Message(), io.BytesIO())
        return Resp("# ok")

    monkeypatch.setattr(F.urllib.request, "urlopen", fake)
    monkeypatch.setattr(F.time, "sleep", lambda s: None)
    assert fetch("https://example.com/x") == "# ok"
    assert len(calls) == 2


def test_fetch_retries_on_connection_reset(monkeypatch):
    calls = []

    def fake(*a, **k):
        calls.append(1)
        if len(calls) == 1:
            raise ConnectionResetError("reset")
        return Resp("# ok")

    monkeypatch.setattr(F.urllib.request, "urlopen", fake)
    monkeypatch.setattr(F.time, "sleep", lambda s: None)
    assert fetch("https://example.com/x") == "# ok"
    assert len(calls) == 2


def test_fetch_incomplete_read_raises_fetcherror(monkeypatch):
    calls = []

    def fake(*a, **k):
        calls.append(1)
        raise http.client.IncompleteRead(b"")

    monkeypatch.setattr(F.urllib.request, "urlopen", fake)
    monkeypatch.setattr(F.time, "sleep", lambda s: None)
    with pytest.raises(FetchError):
        fetch("https://example.com/x")
    assert len(calls) == 2


def test_sources_ids_unique_and_ten():
    assert len(SOURCES) == 10
    assert len({s.id for s in SOURCES}) == 10


@pytest.mark.skipif(not os.getenv("LIVE"), reason="network")
@pytest.mark.parametrize("src", SOURCES, ids=lambda s: s.id)
def test_live_sources(src):
    assert len(fetch_source(src)) > 500
