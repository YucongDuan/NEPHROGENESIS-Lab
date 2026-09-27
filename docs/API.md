# Python, command-line and local HTTP contracts

## Python library

```python
from nephrogenesis.calculators import calculate
from nephrogenesis.experiments import run_experiment
from nephrogenesis.ledger import write_bundle, verify_bundle, replay
from nephrogenesis.evidence import validate_graph, withdraw
from nephrogenesis.adapters import review_envelope

result = run_experiment("transport", {"active_fraction": 0.5})
receipt = write_bundle("transport", {"active_fraction": 0.5}, "runs/example")
check = verify_bundle("runs/example", receipt["receipt_digest"])
rerun = replay("runs/example")
envelope = review_envelope(result)
```

`run_experiment` returns a JSON-serializable dictionary and does not write files. `write_bundle` executes and writes an absent/empty directory. `verify_bundle` checks internal file/ledger binding and optionally a trusted external receipt digest. `replay` requires the original code/data identity and returns numerical/serialization comparisons. `validate_graph` checks the evidence contract; `withdraw` returns a copied revised graph and affected node identifiers. None of these interfaces execute user-supplied source code or contact an external service.

The controlled exception type is `nephrogenesis.common.ValidationError`. Numeric values must be finite; `True` is not accepted as numeric 1. Experiment override fields are checked against the selected experiment's defaults. `dynamics` uses its own complete parameter schema. Unknown fields are rejected rather than ignored.

## Command-line interface

| Command | Meaning |
|---|---|
| `catalog` | Return experiment identifiers, defaults and book sections. |
| `verify` | Recompute the 22 book equation checks; nonzero exit on failure. |
| `run ID --config FILE --out DIR` | Run an experiment and seal a new bundle; config is optional. |
| `demo --out DIR` | Run all 24 laboratories and create one offline report. |
| `calculate ID --config FILE --out FILE` | Run a unit-explicit equation; config/output file optional. |
| `fit --data CSV --metadata JSON --out DIR` | Convert explicit observation rows into a sealed calibration run. |
| `verify-run DIR --trusted-receipt HEX` | Check an experiment receipt; independent anchor is optional. |
| `replay DIR` | Verify and numerically recompute the stored experiment. |
| `evidence FILE --withdraw ID --out FILE` | Validate or withdraw a source in a graph; withdrawal/output optional. |
| `serve --port PORT` | Start the loopback-only interface. |

Exit 0 means the requested operation completed, not that a scientific hypothesis is true. Exit 1 signals a failed verification/replay where used; exit 2 signals invalid input or a handled operational error. Evidence invalidity is represented in the returned JSON; callers must inspect its `valid` field rather than infer scientific status from process completion alone.

## Calculator identifiers

`filtration`, `unindex`, `clearance`, `minimum_urine`, `acid`, `transport_energy`, `electrochemical`, `landauer`, `scales`.

Measurement fields use `{"value": number, "unit": string}`. Dimensionless scalar fields such as hematocrit remain explicitly named numbers. `unindex.indexed_gfr` is defined as a scalar in mL/min/1.73 m2; it is not accepted as an ordinary volume-flow `Quantity`. Dimensional input errors return a clear failure. The UI catalog exposes the accepted default field names and units for each equation-derived laboratory.

## Local HTTP API

| Method and path | Contract |
|---|---|
| `GET /api/health` | Software version and local research mode. |
| `GET /api/catalog` | Experiment metadata/defaults, including calibration. |
| `GET /api/chapters` | The 18 English chapter passports. |
| `GET /api/benchmarks` | Recomputed book regression results. |
| `POST /api/run` | Body: `{"experiment": ID, "parameters": {...}}`. |

POST requires `Content-Type: application/json` and `X-Nephro-Request: local`; Host/Origin must match the local server. Requests are capped at 32,768 bytes, so large permitted CSV research sets should use the CLI. There are no endpoints for arbitrary files, shell commands, devices, hosted notebooks or third-party accounts. Browser sessions do not persist runs. A POST result is the same experiment contract used by the CLI but does not include a newly written bundle receipt.

## Schema stability

The source release includes a stable outer experiment-request schema and a review-envelope example. Per-experiment scientific validation remains in Python, where units and numerical bounds can be checked. This is not a claim of complete JSON Schema validation for all nested model semantics. Adding a field or changing the interpretation of an existing one requires a versioned contract and new tests. The source digest intentionally changes when shipped executable code or model/catalog data change.
