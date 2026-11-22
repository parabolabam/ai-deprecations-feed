from functools import partial

from depfeed.parsers.tables import TableSpec, parse_tables

SPECS = [
    # replacement keys first: "Replacement model ID" also contains "model id"
    TableSpec(("model id", "retirement date"),
              {"replacement": "replacement", "recommended upgrade": "replacement",
               "model id": "affected", "retirement": "shutdown"},
              "Model retirement", skip_undated=True, id_fields=("affected",)),
    TableSpec(("feature", "deprecated date"),
              {"feature": "affected", "deprecated": "announced", "shutdown": "shutdown",
               "details": "text"},
              "Feature shutdown", affected="cell", skip_undated=True, id_fields=("affected",)),
]

parse = partial(parse_tables, source="vertex", specs=SPECS)
