from functools import partial

from depfeed.parsers.tables import TableSpec, parse_tables

_ID = ("section", "affected", "status")
SPECS = [
    TableSpec(("lifecycle", "retirement date"),
              {"model": "affected", "version": "version", "lifecycle": "status",
               "retirement": "shutdown", "replacement": "replacement"},
              "Model retirement", affected="model_version", skip_undated=True, id_fields=_ID),
    TableSpec(("training retirement", "deployment retirement"),
              {"model": "affected", "version": "version", "deployment retirement": "shutdown"},
              "Fine-tuned deployment retirement", affected="model_version",
              skip_undated=True, id_fields=_ID),
]

parse = partial(parse_tables, source="azure", specs=SPECS)
