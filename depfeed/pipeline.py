from collections.abc import Callable
from dataclasses import dataclass

from .diff import diff_record
from .fetch import FetchError
from .records import Record, record_id
from .sources import Source

MIN_CHARS = 500
BROKEN = {"parser_broken", "fetch_broken"}


def check(records: list[Record], prev_count: int) -> str | None:
    if not records:
        return "no records"
    if len(records) < prev_count / 2:
        return f"count dropped from {prev_count} to {len(records)}"
    for r in records:
        if not (r.announced or r.shutdown):
            return f"record without date: {r.title}"
    return None


@dataclass
class Result:
    snapshot: str | None
    parsed: list[Record] | None
    extra: list[Record]
    status: dict


def _junk(text: str, old: str | None) -> str | None:
    if len(text) < MIN_CHARS:
        return f"page too short: {len(text)} chars"
    if old and len(text) < len(old) / 2:
        return f"page shrank from {len(old)} to {len(text)} chars"
    return None


def process(src: Source, old: str | None, prev: dict | None,
            fetch: Callable[[Source], str], today: str) -> Result:
    p = prev or {}
    p_state, p_count, p_changed = p.get("state"), p.get("count", 0), p.get("changed")
    snapshot = parsed = None
    extra: list[Record] = []
    count, changed, error = p_count, p_changed, None

    try:
        text = fetch(src)
        error = _junk(text, old)
    except FetchError as e:
        text, error = None, str(e)

    if error:
        state = "fetch_broken"
    else:
        changed_now = text != old
        if changed_now:
            snapshot, changed = text, today
        if src.parser is None:
            state, count = "diff", 0
            if changed_now:
                d = diff_record(src, old, text, today)
                extra = [d] if d else []
        else:
            try:
                records = src.parser(text, src.link)
                error = check(records, p_count)
            except Exception as e:
                error = f"parser exception: {type(e).__name__}: {e}"
            if error:
                state = "parser_broken"
                if changed_now:
                    d = diff_record(src, old, text, today)
                    extra = [d] if d else []
            else:
                state, parsed, count = "ok", records, len(records)

    if state in BROKEN and p_state not in BROKEN:
        title = (f"Парсер источника {src.name} сломан" if state == "parser_broken"
                 else f"Источник {src.name} не отдаёт данные")
        extra.append(Record(id=record_id(src.id, today, title), source=src.id,
                            kind="health", title=title, url=src.link, text=error))

    since = p.get("since", today) if state == p_state else today
    return Result(snapshot, parsed, extra, {"state": state, "since": since,
                  "changed": changed, "count": count, "error": error})
