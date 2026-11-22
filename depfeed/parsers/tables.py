import re
from dataclasses import dataclass
from urllib.parse import urljoin

from depfeed.dates import parse_date
from depfeed.records import Record, record_id


@dataclass(frozen=True)
class TableSpec:
    match: tuple[str, ...]
    columns: dict[str, str]
    prefix: str
    affected: str = "ids"  # "ids" | "cell" | "model_version"
    heading_date: str | None = None  # "announced" | "shutdown"
    body_announced: str | None = None
    skip_undated: bool = False
    require_date: bool = True
    id_fields: tuple[str, ...] = ("announced", "affected")


def _cells(line: str) -> list[str]:
    line = line.strip().removeprefix("|").removesuffix("|")
    return [c.strip() for c in re.split(r"(?<!\\)\|", line)]


def _plain(s: str) -> str:
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s.replace("**", ""))
    return " ".join(s.replace("`", "").split())


def _links(cells: list[str], page: str) -> list[str]:
    out: list[str] = []
    for cell in cells:
        for text, url in re.findall(r"\[([^\]]*)\]\(([^)\s]+)\)", cell):
            url = page + url if url.startswith("#") else urljoin(page, url)
            entry = f"{_plain(text)}: {url}"
            if entry not in out:
                out.append(entry)
    return out


def markdoc_tables(text: str) -> str:
    out: list[str] = []
    rows: list[list[str]] | None = None
    for line in text.splitlines():
        if rows is None:
            if line.strip().startswith("{% table"):
                rows = [[]]
            else:
                out.append(line)
        elif line.strip().startswith("{% /table"):
            for i, r in enumerate(x for x in rows if x):
                out.append("| " + " | ".join(r) + " |")
                if i == 0:
                    out.append("|" + "---|" * len(r))
            rows = None
        elif line.strip() == "---":
            rows.append([])
        elif line.startswith("*"):
            rows[-1].append(line[1:].strip())
    return "\n".join(out)


def _heading(line: str) -> str:
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line.lstrip("#"))
    return " ".join(re.sub(r"{%.*?%}", "", s).split())


def parse_tables(text: str, link: str, source: str, specs: list[TableSpec]) -> list[Record]:
    out: list[Record] = []
    seen: set[str] = set()
    spec: TableSpec | None = None
    cols: dict[int, str] = {}
    open_ = False
    section, body = "", ""
    for line in text.splitlines():
        if not line.startswith("|"):
            open_ = False
            if line.startswith("#"):
                if line.startswith(("## ", "### ")):
                    section, body = _heading(line), ""
            else:
                body += line + "\n"
            continue
        cells = _cells(line)
        if not open_:
            open_ = True
            low = [_plain(c).lower() for c in cells]
            spec = next((s for s in specs
                         if all(any(k in c for c in low) for k in s.match)), None)
            if spec:
                cols = {}
                for i, c in enumerate(low):
                    f = next((v for k, v in spec.columns.items() if k in c), None)
                    if f:
                        cols[i] = f
            continue
        if spec is None or all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        c = {cols[i]: v for i, v in enumerate(cells) if i in cols}
        shutdown = parse_date(c.get("shutdown", ""))
        announced = parse_date(c.get("announced", ""))
        if spec.heading_date:
            if spec.heading_date == "announced":
                announced = parse_date(section)
            else:
                shutdown = parse_date(section)
        if spec.body_announced and not announced:
            m = re.search(spec.body_announced, body)
            if m:
                announced = parse_date(m.group(1))
        cell = c.get("affected", "")
        if spec.affected == "cell":
            affected = [_plain(cell)]
        elif spec.affected == "model_version":
            v = _plain(c.get("version", ""))
            affected = [_plain(cell) if v in ("", "—") else f"{_plain(cell)} {v}"]
        else:
            affected = [a.rstrip("\\*") for a in re.findall(r"`([^`]+)`", cell)] or [
                a.strip() for a in _plain(cell).split(",") if a.strip()]
        when = shutdown or c.get("shutdown", "").replace("**", "")
        sec = section + ": " if "section" in spec.id_fields else ""
        aff = ", ".join(affected) if spec.affected == "model_version" else _plain(cell)
        title = f"{spec.prefix} {when}: {sec}{aff}" if when else f"{spec.prefix}: {sec}{aff}"
        if spec.skip_undated and not shutdown:
            continue
        if spec.require_date and not (announced or shutdown):
            raise ValueError(f"row without date: {title}")
        rep = _plain(c.get("replacement", ""))
        r = Record(id="", source=source, kind="parsed", title=title, url=link,
                   announced=announced, shutdown=shutdown, affected=affected,
                   replacement=None if rep in ("", "—", "-", "N/A") else rep,
                   status=_plain(c.get("status", "")) or None,
                   text=_plain(c.get("text", "")) or None, links=_links(cells, link))

        def val(f: str) -> str:
            if f == "announced":
                return announced or shutdown or ""
            if f == "affected":
                return affected[0] if affected else title
            if f == "section":
                return section
            return getattr(r, f) or ""
        vals = [val(f) for f in spec.id_fields]
        r.id = record_id(source, *vals)
        if r.id in seen:  # duplicate: disambiguate by full affected list
            r.id = record_id(source, *vals, "|".join(affected))
        seen.add(r.id)
        out.append(r)
    return out
