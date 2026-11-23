import re

from depfeed.records import Record, record_id

HEAD = re.compile(r"### (\d{4}-\d{2}-\d{2}): (.+)")


def _record(shutdown: str, name: str, body: list[str], link: str) -> Record:
    text = "\n".join(body).strip()
    return Record(
        id=record_id("cohere", shutdown, name), source="cohere", kind="parsed",
        title=f"Deprecation {shutdown}: {name}", url=link, announced=None, shutdown=shutdown,
        affected=list(dict.fromkeys(re.findall(r"`([^`]+)`", text))),
        replacement=None, status=None, links=[], text=text[:1500],
    )


def parse(text: str, link: str) -> list[Record]:
    out, cur, in_hist = [], None, False

    def flush():
        if cur:
            out.append(_record(*cur, link))

    for line in text.splitlines():
        if re.match(r"#{1,2} ", line):
            flush(); cur = None
            in_hist = line.strip() == "## Deprecation History"
        elif in_hist and (m := HEAD.match(line)):
            flush(); cur = (m[1], m[2].strip(), [])
        elif cur:
            cur[2].append(line)
    flush()
    return out
