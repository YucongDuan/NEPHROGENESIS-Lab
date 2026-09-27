# NEPHROGENESIS-Lab

[English](README.md) · [中文](README.zh-CN.md) · [Quick start](GETTING_STARTED.md) · [Releases](https://github.com/YucongDuan/NEPHROGENESIS-Lab/releases) · [Project page](https://yucongduan.github.io/NEPHROGENESIS-Lab/)

[![Tests](https://github.com/YucongDuan/NEPHROGENESIS-Lab/actions/workflows/ci.yml/badge.svg)](https://github.com/YucongDuan/NEPHROGENESIS-Lab/actions/workflows/ci.yml)

## Energy–Information Kidney Science Workbench · v1.0.0

**A runnable, English-language research companion to _A Brief History of the Kidney_ by Yucong Duan and Zhongdao Wu.**

The central question is not merely what a kidney contains, but how an open living system maintains differences that let it continue functioning. This companion turns selected book arguments into equations, explicit assumptions, model comparisons, failure tests and reproducible records.

It is an independently implemented domain workbench, not a renamed care-routing application, a new large language model, a validated human digital twin or evidence that an independent physical information field exists.

## Start without installing dependencies

Python 3.10 or newer is required. The core uses only the Python standard library; no API key, model download, cloud account or runtime package installation is required.

```bash
python run.py verify
python -m unittest discover -s tests -v
python run.py serve --port 8765
```

Open `http://127.0.0.1:8765`. On Windows, `py -3` can replace `python`; `launch.bat` starts the local interface. On macOS or Linux, `sh launch.sh` uses `python3`. Stop the server with Ctrl+C.

The browser contains a parameter-editable experiment workbench, 18 chapter passports and 22 book equation checks. Browser output is transient; export JSON or use the CLI to preserve a complete replayable bundle. `SHOWCASE.html` is a precomputed offline reading example: it requires no server, but it does not recompute edited parameters.

## Run and preserve the science

```bash
python run.py run transport --out runs/transport-01
python run.py verify-run runs/transport-01
python run.py replay runs/transport-01
python run.py run dynamics --config examples/delayed_compartment.json --out runs/delayed-01
python run.py fit --data examples/synthetic_curve.csv --metadata examples/curve_source.json --out runs/curve-01
python run.py demo --out runs/all-labs
```

Run directories must be absent or empty. The software deliberately refuses to overwrite an existing experiment. Each run contains its complete parameters, result, model/code identity, six-event DIKWP ledger, checksums and an offline HTML report. Tabular experiments also include CSV. Save the printed receipt digest somewhere independently trusted when replacement of an entire run directory is a concern.

## What is actually implemented

| Capability | Implementation and scope |
|---|---|
| 18 book chapter laboratories | One original English passport and an executable entry per chapter, with exact section anchors and source chapter hashes. |
| 24 experiment entries | The 18 chapter entries plus contract ablation, added-effect testing, parameter ensembles, finite-horizon Pareto screening, regulated dynamics and research-curve calibration. They are not 24 anatomical kidney models. |
| 9 unit-explicit calculator APIs | Filtration, de-indexing, osmolar/free-water clearance, minimum urine, net acid excretion, transport work, electrochemical work, logical erasure comparison and conditional physical limits. |
| Conservative reduced dynamics | Water, sodium and urea stocks and cumulative input/output budgets; held-step control; explicit resource cap; no silent negative-state clipping. |
| Model discrimination | Equal-equilibrium, different-transient candidates; observation-time design score under specified noise. |
| Research data fitting | Bounded grid calibration of a one-compartment surrogate; fixed initial condition; training and held-out rows separated; boundary-optimum warning. |
| Evidence revision | Typed, acyclic dependency records; missing-source and kind checks; source withdrawal makes dependent records stale. |
| Reproducibility | Input/model/result binding, deterministic seeded generators, integrity checks, numerical recomputation and neutral review-envelope export. |
| Local English UI | No external fonts, scripts, telemetry or API requests; JSON editing/export, compatible-axis plots, tables and model limitations. |

## Three experiments that express the book's contribution

**Equal output, unequal work.** `transport` holds sodium excretion at 0.1 mmol/min and compares filtered loads of 8 and 16 mmol/min. With a declared active fraction of 0.6, 3 sodium per ATP and 50 kJ/mol ATP, the ideal coupled powers differ by approximately 1.333333 W. This is a conditional calculation, not a measurement of two kidneys.

**Equal budget, different correspondence.** `signal` gives matched, fixed, shuffled, delayed, reversed and calibrated-remap policies the same observations and the same assumed action-energy budget. Its purpose is to separate useful correspondence from message volume. Sensing/computation costs are not included, and the result is not a thermodynamic proof of a new field.

**Equal equilibrium, different mechanism.** `identifiability` uses two exact one-compartment models with the same steady concentration and different turnover rates. A transient separates them. The choice of observation time is derived from a stated candidate set and noise model, not from an unexplained score.

## Relation to the existing DIKWP portfolio

The review covers six selected public repository descriptions and two complete root trees, not every Yucong Duan repository and not an exhaustive upstream source audit. NephroCarePath documents care workflow and governance; ProofLedger documents claim/evidence support; AgentTrace documents trace custody; NEGENESIS separates order, entropy and value; SCALE separates resource objectives; PRAXIS explicitly asks for independent reproduction and source-first delivery. This project instantiates those directions in a specific scientific companion.

Some upstream applications are packaged inside ZIP files. Their archived source was not retrieved or executed in this review; absence of visible root source is not evidence that tests or implementations are absent inside the archive. No upstream runtime benchmark, defect count or claim of universal superiority is made. The precise observation/interpretation/extension distinction is recorded in `docs/UPSTREAM_REVIEW.md` and `nephrogenesis/data/upstream_review.json`.

## Repository organization

```text
nephrogenesis/          Executable Python source, data passports and English web UI
  units.py             Explicit dimensional algebra and semantic unit kinds
  calculators.py       Book-aligned equations and 22 regressions
  dynamics.py          Conservative reduced stock/flow model
  experiments.py       Chapter experiments and advanced experiments
  calibration.py       Supplied-curve training/held-out calibration
  evidence.py          Typed dependencies and revision propagation
  ledger.py            Sealed runs, integrity checks and recomputation
  adapters.py          Neutral review-envelope export, not an upstream API client
  server.py / cli.py   Local interfaces
examples/              Synthetic inputs, source declarations and invalid-input fixture
sample_runs/           Small precomputed replayable examples from this release
validation/            Actual local test, convergence and browser check results
scripts/               Release inventory verification
.github/workflows/     GitHub Actions scientific and reproducibility checks
docs/                  Methods, architecture, review, API, extension and learning guide
```

## Installation as a package

The zero-install checkout is the simplest route. The tested wheel is included in `dist/` and also supplied separately. From the source release use `python -m pip install --no-deps dist/nephrogenesis_lab-1.0.0-py3-none-any.whl`; the following command assumes the separately downloaded wheel is in the current directory. To install it into an existing environment without resolving dependencies:

```bash
python -m pip install --no-deps nephrogenesis_lab-1.0.0-py3-none-any.whl
nephrogenesis verify
nephrogenesis serve
```

Source installation uses `python -m pip install --no-deps --no-build-isolation .` and requires an already installed compatible setuptools/wheel build environment. Hosted CI and cross-platform commands are supplied; the validation report distinguishes what was actually executed locally from what remains configuration only.

## Scientific and publication boundaries

The implementation has no patient-specific dosing, diagnosis, triage, treatment recommendation, dialysis prescription, transplant eligibility decision or medical-device control. Synthetic numbers are not prevalence estimates, survival thresholds or effect sizes. A successful unit test establishes a narrow software property; it does not validate an entire physiological model. The reduced model does not solve spatial nephron transport, glomerular microstructure, acid-base chemistry, endocrine feedback or developmental gene networks.

The full book is neither reproduced nor relicensed. New code and original companion documentation use Apache-2.0. `NOTICE` explains attribution. Naming the book authors does not represent their approval of this release. Independent scientific reproduction, clinical validation and publisher acceptance are separate from software publication. See [publication records](PUBLICATION.md) and the linked GitHub Actions runs for software checks.

## Release maintenance and optional UI reproduction

For a reviewed new release, rerun the tests and rebuild its wheel, then use `python scripts/build_release_manifest.py --confirm-new-inventory`. This establishes a new inventory; never regenerate a mismatched manifest as a substitute for investigating tampering or an unintended edit. `python scripts/verify_release.py` verifies a preserved inventory.

`python scripts/check_browser_dom.py --chromium /path/to/chromium --out /path/to/new-qa-directory` reproduces the optional isolated-DOM browser checks. It requires separately installed development tools Playwright and Chromium, neither of which is a runtime dependency. It uses the actual Python experiment engine through a test bridge; HTTP route contracts are exercised separately by the standard-library tests. Do not describe this method as browser-through-HTTP end-to-end testing.

## Explore the companion collection

- [Related companion: DIKWP-HepatoGenesis-Lab](https://github.com/YucongDuan/DIKWP-HepatoGenesis-Lab)
- [Yucong Duan · DIKWP research portfolio](https://github.com/YucongDuan)
- [All projects and research areas](https://github.com/YucongDuan/YucongDuan/blob/main/REPOSITORY_DIRECTORY.md)
