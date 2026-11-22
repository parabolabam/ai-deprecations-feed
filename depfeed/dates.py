import re
from datetime import date

_MONTHS = {m: i for i, m in enumerate(
    "jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}
_RE = re.compile(
    r"(?P<iso>\b(\d{4})-(\d{2})-(\d{2})\b)"
    r"|(?P<named>\b([A-Za-z]{3,9})\.? (\d{1,2}), (\d{4})\b)"
    r"|(?P<us>\b(\d{1,2})/(\d{1,2})/(\d{2})\b)")


def parse_date(s: str) -> str | None:
    s = re.sub(r"\^\d+\^", "", s.replace("**", ""))
    for m in _RE.finditer(s):
        try:
            if m["iso"]:
                y, mo, d = int(m[2]), int(m[3]), int(m[4])
            elif m["named"]:
                mo = _MONTHS.get(m[6][:3].lower())
                if mo is None:
                    continue
                y, d = int(m[8]), int(m[7])
            else:
                mo, d, y = int(m[10]), int(m[11]), 2000 + int(m[12])
            return date(y, mo, d).isoformat()
        except ValueError:
            continue
    return None
