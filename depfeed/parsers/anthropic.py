from functools import partial

from depfeed.parsers.tables import TableSpec, parse_tables

SPECS = [
    TableSpec(("retirement date", "deprecated model"),
              {"retirement": "shutdown", "deprecated model": "affected", "replacement": "replacement"},
              "Model retirement", heading_date="announced"),
    TableSpec(("parameter", "behavior"),
              {"parameter": "affected", "status": "status", "behavior": "text", "replacement": "replacement"},
              "API parameter deprecation", require_date=False),
]

parse = partial(parse_tables, source="anthropic", specs=SPECS)
