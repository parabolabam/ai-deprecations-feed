import difflib
import re

from .records import Record, record_id

MAX_DIFF_CHARS = 4000


def diff_record(src, old: str | None, new: str, today: str) -> Record | None:
    if old is None:
        return None
    a, b = old.splitlines(), new.splitlines()
    # SequenceMatcher, not ndiff: ndiff is too slow on ~2000-line snapshots
    ops = difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
    lines = [x for tag, _, _, j1, j2 in ops if tag in ("insert", "replace")
             for x in b[j1:j2]]
    if src.keep:
        lines = [x for x in lines if re.search(src.keep, x)]
    if not lines:
        return None
    text = "\n".join(lines)
    if len(text) > MAX_DIFF_CHARS:
        text = text[:MAX_DIFF_CHARS] + "\n…(truncated)"
    return Record(id=record_id(src.id, today, text), source=src.id, kind="raw",
                  title=f"{src.name}: page changed", url=src.link, text=text)
