# Validation and delivery status

Validation date: 26 September 2026. These are results from this implementation and environment, not planned tests or a benchmark against upstream binaries.

## Executed checks

The local standard-library unit suite passed **198 tests with zero failures/errors**. This includes the 22 independent book-regression entries, domain and invalid-input cases, mass conservation, RK4 comparison to an analytic solution, hybrid step refinement, seeded repeatability, training/held-out separation, graph contracts, source withdrawal, receipt tampering, HTML/CSV escaping and live local HTTP contracts. The source log is in `validation/unittest.log`.

All **24 default experiments** were executed, sealed and recomputed. Their complete results were numerically equal and canonically identical in this environment. The replay report is in `validation/all_experiment_replays.json`. Identical serialization here is not a promise of bitwise identity across every platform or math library; the replay command also exposes explicit numerical tolerances.

The optional development coverage tool reported **88.34% statement coverage**, **80.32% branch coverage**, and **86.27% combined coverage** of the instrumented Python package. Some CLI subprocess work is not counted by that coverage run. Coverage is not the proportion of scientific truth validated. It is not 100%, and no complete formal proof or security audit is claimed.

## Default conservation record

| Quantity | Maximum absolute residual | Unit |
|---|---:|---|
| Water stock-flow balance | 3.11973e-14 | L |
| Sodium stock-flow balance | 9.98313e-13 | mmol |
| Urea stock-flow balance | 3.55271e-13 | mmol |

The tests also exercised 30 reproducibly selected parameter combinations. These residuals are bookkeeping checks for the reduced model. They do not establish a complete energy conservation theorem, a physiologically validated trajectory or a patient-level outcome.

## Interface and installation checks

Live HTTP tests checked the health, catalog, chapter and benchmark routes, successful/invalid runs, strict Host/Origin handling, missing custom headers, wrong content types, oversized bodies, non-finite JSON, duplicate keys, unknown paths and traversal. The runtime's Chromium administrator policy blocked direct browser navigation to localhost. Visual/interaction testing therefore used an isolated owned HTML document with the actual Python engine connected through a test bridge; it did not bypass that navigation policy. All 24 experiments were driven through the English UI, with no JavaScript errors, 18 visible chapter passports and no document-wide horizontal overflow at 390-pixel width. A stale-result issue was found and corrected: changing inputs or the selected experiment now clears the prior result before rerunning. Details are in `validation/browser.json`.

The wheel was built without resolving network dependencies, installed into an isolated target directory and run from a working directory outside the source checkout. Its catalog, calibration, command-line equation checks, static package resources and replay of a source-created experiment passed. The install location and commands are recorded in `validation/wheel_validation.json` and the wheel logs. This demonstrates local package resource inclusion, not actual testing on Windows or macOS.

## What was not executed or established

The upstream ZIP application source was not retrieved or executed. There is no upstream accuracy or performance comparison. At the original 26 September package validation, hosted GitHub Actions had not run and no repository had been created. The subsequent publication is tracked separately in [PUBLICATION.md](../PUBLICATION.md); hosted results are linked by commit in GitHub Actions. There was no clinical deployment, patient-data validation, medical-device test, independent scientific review or demonstration of a new physical information field.

The English technical handbook is a delivery guide rather than a publisher-approved manual. Its DOCX is rendered and visually reviewed separately. Full book content is not redistributed. Release-manifest checks verify the shipped inventory against its manifest, not external authorship or institutional endorsement.

## Reproduce the checks

```bash
python -m unittest discover -s tests -v
python run.py verify
python run.py demo --out runs/reproduce
python run.py replay runs/reproduce/transport
python scripts/verify_release.py
```

The demo directory must be absent or empty. The release verification script checks all files listed in `RELEASE_MANIFEST.json`; development outputs and caches are not release content. Fresh-archive extraction and inventory verification are recorded in the external delivery audit after packaging, avoiding a self-referential archive hash inside the archive itself.
