from functools import partial

from depfeed.parsers.tables import TableSpec, parse_tables

SPECS = [
    TableSpec(("shutdown date", "replacement"),
              {"replacement": "replacement", "shutdown": "shutdown", "model": "affected"},
              "Model shutdown",
              body_announced=r"(?i)\bon (\w+ \d{1,2}, \d{4}), we (?:announced|emailed)"),
]

parse = partial(parse_tables, source="groq", specs=SPECS)
