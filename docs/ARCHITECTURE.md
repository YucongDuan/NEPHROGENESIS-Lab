# Architecture and extension contracts

## The executable-book boundary

The system sits between a scientific manuscript and a research workflow. It does not sit between a clinician and a medical device. The manuscript supplies questions, conceptual distinctions and specific equation examples. A chapter passport connects a numbered book section to a newly implemented experiment, its source-file hash, its method and its limitation. The executable code then states the scenario assumptions and produces a typed result. This separation prevents software output from being attributed to the book as if it were an already reported empirical finding.

The core dependency direction is:

```text
book source manifest + chapter passports
                |
                v
experiment contract -> strict inputs -> units / model / fit
                |                         |
                |                         v
                +------------------ numerical result
                                           |
                                           v
                              evidence-kind interpretation
                                           |
                                           v
                              run ledger + local receipt
                                           |
                                           v
                              integrity check + recomputation
```

The graph depicts software dependencies, not five irreversible DIKWP stages. Purpose may be revised after interpretation. A new question is a new node or experiment version rather than an overwrite of the old record.

## Components and ownership

`common.py` provides error types, finite-number checks, canonical JSON and digests. It rejects duplicate keys in local JSON files so a configuration has one unambiguous reading. `units.py` implements deliberately limited dimensional algebra. `calculators.py` contains equations and fixed book regressions. `dynamics.py` advances stocks and cumulative flows; it does not depend on the UI. `experiments.py` registers bounded laboratory entry points and attaches book anchors. `calibration.py` validates supplied observations and performs the held-out fit.

`evidence.py` validates a declared dependency graph and propagates withdrawal. It neither retrieves papers nor uses a language model to decide truth. `ledger.py` binds the exact protocol and output and checks numerical re-execution. `reporting.py` produces an escaped, self-contained HTML report. `server.py` is an optional local interface, while `cli.py` is the reproducible automation interface. `adapters.py` exports a neutral review envelope. Static assets and data passports are shipped with the Python package.

All core operations work without external packages or network access. Development tools used to measure coverage, drive Chromium or render the handbook are not runtime dependencies. Their execution results are described separately in the validation report. A wheel bundles the same source modules and resources. It is not a compiled scientific backend, and installation is optional.

## Experiment result contract

Every result identifies the experiment, exact parameters, source sections and status. Most experiments expose `metrics`, `rows`, `series` and `notes`; equation calculators expose `outputs` and `assumptions`. Series include x/y units. Both browser and offline reports overlay only series whose axes have identical unit labels. Reports do not silently compare litres and mmol/L on one unlabelled axis.

`dynamics` additionally retains the full simulation configuration and trajectory. `calibration` retains supplied observations, source declaration, residuals and the training-objective profile. `evidence` retains before/after records. The schema is intentionally small and explicit. A new model should not insert unannounced fields whose names imply empirical validation or treatment authority.

## Run identity and custody

An experiment bundle consists of `protocol.json`, `result.json`, `ledger.jsonl`, `report.html`, optional `table.csv` and `receipt.json`. The protocol contains software version and the digest of executable Python plus shipped model/catalog data. Six chained events bind question, inputs, semantic context, execution, limits and next question. The receipt hashes all listed files and the final ledger entry.

Recomputation first checks file integrity, then requires the current model/code digest to match the protocol. It executes the saved parameters and compares the complete JSON structure. Floating values use relative tolerance 1e-10 and absolute tolerance 1e-12; the result also reports whether canonical serialization is identical. This permits numerical comparison to be distinguished from bitwise equality. Replaying after an intentional code change requires retaining the old release or creating a new versioned experiment, not suppressing the identity check.

The hash of the receipt can be preserved independently. Without that external anchor, a party able to rewrite the whole directory can also regenerate an internally consistent receipt. Neither an unkeyed chain nor the SHA-256 release manifest supplies authorship authentication, a trusted timestamp or a scientific endorsement. This trust model is part of the delivered contract, not an omitted caveat.

## Local interface and persistence

The server exposes only fixed asset paths and a handful of JSON endpoints. It serves no directory listing or arbitrary files, binds loopback, rejects foreign Host/Origin values and requires a custom header for execution. HTTP requests are bounded to 32 KiB; each experiment also has numerical work limits. Browser runs remain in memory and must be exported by the user. The CLI is used to create disk bundles.

There is no background scheduling, external model call, account connection, automatic source download or device command. Existing directories are not overwritten. No SQLite server or cloud database is required. This reduces setup cost but does not supply institutional identity management or multi-user governance. Institutions should build a separately reviewed service layer before sharing access remotely.

## Interoperability without invented compatibility

The neutral `review_envelope(report)` function exports parameters, assumptions, book sections, result digest and D/I/K/W/P records. It can be mapped to a claim ledger, action ledger or agent trace system. It does not claim to implement the actual on-wire schema of ProofLedger, AgentTrace, PRAXIS or SCALE. Those upstream archived schemas were not obtained in this review. A direct adapter needs the actual versioned schema, test fixtures, loss handling and round-trip tests before its compatibility can be advertised.

This is the practical path beyond isolated prototypes: use one small scientific kernel with stable artifacts and make integration claims only where a tested contract exists. New experiments can be added in the same repository without creating a new top-level “OS” for each chapter. The complete source and CI configuration are now maintained in the public GitHub repository. See [publication records](../PUBLICATION.md) for the publication check and links to hosted workflow results.
