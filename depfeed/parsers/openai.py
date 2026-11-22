from functools import partial

from depfeed.parsers.tables import TableSpec, parse_tables

_COLS = {"shutdown": "shutdown", "affected": "affected", "replacement": "replacement",
         "notice": "announced", "status": "status"}

SPECS = [
    TableSpec(("shutdown", "affected model or feature"), _COLS, "Shutdown"),
    TableSpec(("shutdown", "affected feature"), _COLS, "Feature/endpoint shutdown", affected="cell"),
    TableSpec(("shutdown", "affected model"), _COLS, "Model shutdown"),
]

parse = partial(parse_tables, source="openai", specs=SPECS)
