from depfeed.parsers.tables import TableSpec, markdoc_tables, parse_tables
from depfeed.records import Record

SPECS = [
    TableSpec(("agent", "shutdown date"),
              {"replacement": "replacement", "shutdown": "shutdown", "agent": "affected"},
              "Agent shutdown", skip_undated=True, id_fields=("affected",)),
    TableSpec(("model", "shutdown date"),
              {"replacement": "replacement", "shutdown": "shutdown", "model": "affected"},
              "Model shutdown", skip_undated=True, id_fields=("affected",)),
]


def parse(text: str, link: str) -> list[Record]:
    return parse_tables(markdoc_tables(text), link, "gemini", SPECS)
