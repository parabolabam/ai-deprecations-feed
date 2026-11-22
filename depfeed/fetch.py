from __future__ import annotations

import html
import re
import time
import urllib.error
import urllib.request

from depfeed.sources import Source

HEADERS = {
    "User-Agent": "ai-deprecations-feed (+https://github.com/parabolabam/ai-deprecations-feed)",
    "Accept": "text/markdown, text/plain;q=0.9",
}


class FetchError(Exception):
    pass


def _get(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        ctype = r.headers.get("Content-Type", "") or ""
        body = r.read().decode("utf-8", errors="replace")
    if ctype.lower().startswith("text/html") or body.lstrip().lower().startswith(("<!doctype", "<html")):
        raise FetchError(f"{url}: got HTML, not markdown")
    return body


def fetch(url: str) -> str:
    for attempt in (0, 1):
        try:
            return _get(url)
        except urllib.error.HTTPError as e:
            if e.code != 429 and e.code < 500:
                raise FetchError(f"{url}: HTTP {e.code}") from e
            err: Exception = e
        except (urllib.error.URLError, TimeoutError) as e:
            err = e
        if attempt == 0:
            time.sleep(2)
    raise FetchError(f"{url}: {err}") from err


def normalize(text: str, ignore: tuple[str, ...] = ()) -> str:
    while (u := html.unescape(text)) != text:
        text = u
    lines = text.splitlines()
    if next((l for l in lines if l.strip()), "").strip() == "---":
        i = next(i for i, l in enumerate(lines) if l.strip())
        end = next((j for j in range(i + 1, len(lines)) if lines[j].strip() == "---"), None)
        if end is not None:
            lines = lines[end + 1:]
    out = (" ".join(l.split()) for l in lines)
    return "\n".join(l for l in out if l and not any(re.search(p, l) for p in ignore))


def fetch_source(src: Source) -> str:
    return normalize("\n".join(fetch(u) for u in src.urls), src.ignore)
