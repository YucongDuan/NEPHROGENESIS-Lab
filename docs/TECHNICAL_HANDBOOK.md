# NEPHROGENESIS-Lab
## Energy–Information Kidney Science Workbench

Version 1.0.0 · English Technical Handbook · 26 September 2026

Companion to *A Brief History of the Kidney* by Yucong Duan and Zhongdao Wu.

An independently implemented, local-first workbench for reproducing equations, testing explicit surrogate models, inspecting evidence dependencies and preserving revisable research records.

# 1. Delivery and intended use

This release includes direct Python source, an English browser workbench, 18 chapter passports, 24 executable laboratory entries, 9 unit-explicit calculator APIs, 22 book equation regressions, an automated test suite, reproducible run examples, a wheel and source-first CI configuration. It requires Python 3.10 or newer but no runtime third-party dependency, model download, cloud account or API key.

The source manuscript supplies the questions and framing; the companion supplies new conditional implementations. This distinction is essential. A generated curve is not an experiment previously reported in the book, a low residual is not biological validation, and a local hash is not an independent source endorsement. The appropriate scope is scientific education and transparent research prototyping, not diagnosis or treatment.

The complete source release has one root directory, NEPHROGENESIS-Lab. Read README.md first. Use docs/METHODS.md for full model assumptions, docs/CHAPTER_LABS.md for the laboratory workbook, and validation/ for executed results. The software is not a replacement for reading the book; it makes selected arguments easier to reproduce and challenge.

## 1.1 First commands

```bash
python run.py verify
python -m unittest discover -s tests -v
python run.py serve --port 8765
```

Open http://127.0.0.1:8765. On Windows use py -3 in place of python when needed. The launch.bat and launch.sh helpers are included. SHOWCASE.html is a precomputed offline reading example; edited parameters must be recomputed by the Python engine.

## 1.2 Preserve a result

```bash
python run.py run transport --out runs/transport-01
python run.py verify-run runs/transport-01
python run.py replay runs/transport-01
```

The output directory must be absent or empty. The receipt identifies inputs, model/code version, outputs and ledger. Preserve its printed digest independently if whole-directory replacement is a concern. For research curves, use the fit command with examples/synthetic_curve.csv and examples/curve_source.json as the initial format examples.

# 2. Architecture and custody

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

# 3. Scientific methods and failure conditions

The following sections cover the central numerical and inferential contracts. The full methods file also treats membrane exchange, geometry, branching, repair and replacement in detail.

## 3.1. Interpretive contract

The manuscript asks for a model deliverable that reveals its problem, data, units, parameters and failure conditions rather than only its output picture (book section 15.23). It also asks whether a proposed additional information field makes a distinguishable prediction (16.24), and whether DIKWP improves a task relative to an explicit baseline (18.13). Those are the source-derived requirements. The algorithms in this release are new companion implementations; the book does not claim that these software experiments already established their scientific hypotheses.

Three statuses remain separate. A conditional equation can be mathematically correct under its assumptions. A synthetic experiment can expose consequences of a stipulated model. An empirical inference requires observations, appropriate experimental design, competing explanations and external validation. Source hashes, type labels and repeated runs cannot turn the first two into the third. Imported research observations remain operator-declared observations rather than software-certified truth.

The numerical core uses quantities at the scale of the question being asked. Molar chemical work, per-particle erasure energy, volume flow and empirical evidence status do not share one interchangeable scalar. The purpose of the semantic layer is to preserve these distinctions and permit revision, not to assign data, information, knowledge, wisdom and purpose to five anatomical structures.


## 3.2. Dimensional and semantic quantity algebra

The `Quantity` class carries a base-dimension exponent vector for length, mass, time, amount, temperature and charge. Addition requires identical dimensions and matching semantic tags. Multiplication/division adds or subtracts exponent vectors. Conversion is allowed only through an explicit registry. Unknown strings do not trigger a guessed conversion, and the implementation does not evaluate user formula strings.

An osmole and an equivalent are represented as semantic kinds associated with amount. This prevents a concentration in mmol/L from silently becoming mOsm/L, and prevents mOsm/kg from becoming mOsm/L. Determining an activity coefficient, osmotic coefficient, valence conversion or density requires an explicit additional model. Tagged algebra is intentionally restricted; the domain calculators perform their declared equations instead of pretending the registry is a complete physical-units system.

Numbers must be finite and not booleans. A logarithm accepts only a positive dimensionless ratio. The default transport example multiplies 1 nmol ATP/s by 50 kJ/mol and obtains 50 microwatts. Replacing J/mol with J is rejected. For the erasure comparison, a molar electrochemical work must be divided by Avogadro's constant before division by k_B T ln 2. Equivalently, the denominator is R T ln 2. This dimensionless result is a comparison of energy scales, not an observation of the number of bits processed by an organ.

Constants used for these calculations match the NIST 2022 CODATA listing retrieved on 26 September 2026: k_B, N_A, h and c use their exact SI definitions; G is a measured constant. The code derives R from k_B N_A. The tiny tolerance used in numerical comparisons is a floating-point test tolerance, not the uncertainty of G or the biological parameters [NIST-SI].


## 3.3. Reduced regulated compartment: state and conservation

The state vector contains volume V in L, sodium amount N in mmol, urea amount U in mmol, three cumulative outputs, three cumulative inputs and cumulative ideal coupled energy. Concentrations are N/V and U/V. Parameters whose names end in `_L_min`, `_mmol_min`, `_J_mol` and `_W` have exactly those declared units; calculator endpoints additionally use value/unit objects.

The stock equations are:

```text
dV/dt = water_input - water_output
dN/dt = sodium_input - sodium_output
dU/dt = urea_generation - urea_output
filtered_sodium = gfr * N/V
urea_output = gfr * urea_clearance_fraction * U/V
```

Here time is in minutes and `gfr` is in L/min. These are deliberately reduced process terms. Filtration and reabsorption are not independently resolved across an anatomical nephron, and plasma flow is not another compartment in this model. There is no water-solute osmotic coupling derived from a membrane free-energy functional, no oxygen-diffusion PDE and no endocrine model. The system must not be presented as a full kidney simulator.

All cumulative input and output variables are integrated using the same RK4 stages as their corresponding stock derivatives. The independently evaluated residual for each quantity is:

```text
current_stock - initial_stock - cumulative_input + cumulative_output
```

The residual is monitored at each accepted endpoint. Water, sodium and urea residuals retain separate units. A small residual checks internal numerical bookkeeping. It does not show that the assumed filtration, reabsorption or input functions are physiologically correct. The energy record is an accounted process cost, not a first-law residual for a complete organism.

A negative or non-finite state is rejected with an error instead of clipped to a small positive number. Event start and end times are inserted as integration boundaries so a piecewise constant perturbation contributes exactly its declared duration. Overlapping events add their declared inputs. Event intervals must lie inside the simulation horizon; changing the horizon may therefore require changing the default event list explicitly.


## 3.4. Control and resource assumptions

The default reference volume and sodium concentration are 14 L and 140 mmol/L. The default flows are chosen so the no-event, fixed-control scenario has a steady solution. These are teaching initial conditions, not a recommended personal target. The time-inside-box metric uses [13.5, 14.5] L and [135, 145] mmol/L as an arbitrary declared constraint box. Calling the metric a survival probability, a medical safety threshold or a viability theorem would be incorrect.

At the beginning of each step, a synthetic controller observes a volume/concentration pair. Fixed control ignores deviations. Feedback control uses the current pair. Delayed control uses the most recent stored pair no later than `t - delay`. Scrambled control samples an earlier stored pair using a seeded pseudo-random generator. Reversed control changes the sign of deviations. The implementation transforms requested water/sodium outputs into reabsorption fractions and holds those fractions over the RK4 step.

The whole solver is consequently a hybrid sampled controller, not a continuously evaluated fourth-order feedback system. Refining the step changes controller sampling as well as integration error. The tests demonstrate reduced error in a selected step-refinement comparison and fourth-order RK4 accuracy for an independent linear ODE; they do not claim uniform fourth-order convergence of the delayed controller.

Sodium-associated power uses the declared active fraction, three sodium ions per ATP and the chosen molar ATP free-energy magnitude. With reabsorbed sodium J_N in mmol/min:

```text
energy_rate_J_per_min = J_N * 0.001 * active_fraction / 3 * ATP_energy_J_per_mol
```

A resource ceiling in W is multiplied by 60 to obtain J/min, then inverted to cap the reabsorbed amount. The remainder exits the compartment. This is a mathematical resource constraint, not a mechanistic account of how a real kidney responds to ATP limitation. The remaining non-active fraction represents unmodeled coupled/passive pathways; thermodynamic feasibility of every allowed parameter combination is not established. Basal metabolism, leakage, sensor costs, mitochondrial efficiency and other energy exports are not measured or inferred.


## 3.5. Equal output does not identify the work

The `transport` experiment isolates one relation. Excretion is fixed at 0.1 mmol/min. Candidate filtered loads are 8 and 16 mmol/min, and secretion is excluded. Reabsorption is therefore 7.9 or 15.9 mmol/min. Under a declared active fraction of 0.6, three sodium per ATP and 50 kJ/mol ATP, ideal coupled powers are approximately 1.316667 and 2.65 W. Their difference is approximately 1.333333 W.

These numbers are generated by the scenario rather than measured from two organs. The scientific point is identifiability: identical terminal output need not determine gross internal flux. An experiment intended to test the relation in a biological preparation needs independently observed filtered load, recovery/secretory terms, relevant transport contributions and uncertainty. A counterexample to the claim that output alone identifies work is already supplied algebraically; estimating the actual work in a preparation is a separate task.


## 3.6. Signal correspondence under a matched action budget

The `signal` experiment uses a two-state task arranged in alternating blocks. A binary symmetric observation channel flips each state with a declared probability. The same observations are supplied to matched, fixed, shuffled, delayed, reversed and calibrated-remap strategies. Each action consumes a stipulated 1 J. A correctly located action recovers four toy units; an incorrectly located action recovers none.

All strategies have the same observation count and assigned action cost. The objective is to expose how mapping and timing change a task outcome without changing that chosen budget. The run does not account for total sensing/computation thermodynamics. In particular, arbitrary recovery units cannot be added to joules. The mutual-information value is the theoretical balanced-input binary-channel value 1 - H_b(error), not a numerical estimate of an independent physical field. A finite task sequence need not have exactly the same distribution as that theoretical channel assumption.

When the error exceeds one half, a decoder that knows the channel can invert its outputs. The calibrated-remap strategy is granted the declared error rate; it does not learn it from held-out observations. A favorable result therefore says nothing about the cost of learning the mapping. A stronger future experiment should estimate the decoder on training observations, reserve a separate test sequence, and measure or bound the cost of sensing and remapping. Those additions are not claimed as implemented here.


## 3.7. Identifiability and observation design

Two candidate ODEs dC/dt = G - kC have G/k = 10 mmol/L. Candidate A uses G=0.2 mmol/L/min and k=0.02/min; B uses G=0.1 and k=0.01. Starting at C0=20, the exact trajectory is C*=10 plus (C0-C*) exp(-kt). One observation at equilibrium cannot uniquely recover the two parameters. A transient can separate the declared candidates.

The design score is squared candidate separation divided by a specified observation variance. For this pair the continuous maximum lies at ln(2)/0.01 minutes; the workbench selects the best time on its finite 101-point grid. The default horizon yields a grid optimum near 70.2 minutes. This is a candidate-discrimination calculation, not a general optimizer for laboratory scheduling. It omits sampling cost, temporal noise correlation, model discrepancy and ethical constraints.

The `hypothesis` experiment compares a fixed baseline against one preregistered sinusoidal additional-effect basis. Only the extension amplitude is fitted, using even-index samples. Odd-index outcomes are held out. The known-variance Gaussian BIC expression drops a constant shared by the candidates. A separate held-out MSE is reported. The synthetic generator can inject a sinusoid, so success under that fixture is deliberately favorable to the extension. It is not evidence for a new information field. A real field proposal needs an operational field variable, units, coupling law, controls against known confounds and differential predictions before entering this interface.


## 3.8. Calibration to explicitly supplied observations

The `calibration` experiment and `fit` command accept 5–200 observations with columns `time_min,concentration_mmol_L,split`. The first observation must be a training initial condition at time zero. Times strictly increase, at least three rows are training rows and at least two are held out. The source declaration requires an identifier, kind, locator and affirmative rights statement. A declaration is retained; it is not independently verified by this software.

The fit searches a bounded rectangular grid over k and C*. It fixes C0 at the first training observation and minimizes unweighted training SSE. The default 61 by 61 grid contains 3,721 candidates. It then computes predictions and held-out MSE without refitting, and reports the initial-concentration constant predictor as a transparent baseline. A boundary optimum generates a flag rather than being silently interpreted as a precise biological rate.

This is useful for reproducing a specified low-dimensional surrogate, not diagnosing kidney function. No uncertainty interval is reported: initial-condition noise, correlated errors, structural mismatch and grid resolution are not modeled. The included exact synthetic curve is recoverable on the default grid and provides a software sanity check. Tests perturb only held-out concentrations and verify that fitted parameters do not change. Real research use should add alternative structures and data-quality analysis before treating a fitted parameter as a meaningful mechanism.


## 3.9. Scenario uncertainty and finite-horizon screening

`uncertainty` draws reproducible independent uniform values for GFR and active fraction from declared teaching ranges, then reruns the reduced model. It reports min, median, max and all individual outcomes. These are scenario summaries, not population estimates, posterior intervals or confidence bounds. Correlated parameter distributions are not supplied.

`viability` enumerates twelve fixed controller-gain/resource-ceiling combinations for one specified disturbance and a finite horizon. It retains energy and time inside the arbitrary constraint box as separate objectives and returns nondominated configurations. It is neither an infinite-horizon viability kernel nor a proof of robustness to unobserved disturbances. A failed domain run remains labeled as a failure instead of being assigned a favorable score.


## 3.10. Falsification and invalidation

Each experiment preserves its boundary, units and input declarations. The evidence graph additionally records kind, DIKWP role, source locator, dependencies and optional input/output contracts. The graph cannot contain a cycle, although conceptual roles may revisit D, I, K, W or P in successive nodes. Dependence on synthetic or hypothesis nodes cannot establish empirical status. A withdrawn source makes transitive dependents stale.

The `ablation` benchmark removes checks from a deliberately constructed fault set. It compares an untyped record, unit-only checks, units plus provenance, and the full contract. It exercises actual validators for incompatible units, missing source locators, a broken balance, synthetic-to-empirical promotion and stale dependencies. The favorable result for the full contract is a designed software regression, not an independent evaluation of DIKWP against human researchers or upstream software. A future blinded evaluation would need independently constructed cases, predefined scoring, observer agreement and a baseline with comparable engineering effort.


## 3.11. Reading a successful run correctly

A zero conservation residual can coexist with a wrong physiological model. A perfectly replayed run can repeat a mistaken assumption. A typed evidence graph can contain a false external source. A small held-out error on one generated dataset can reflect a favorable generator. A mathematically valid upper bound can be irrelevant to an organism's attainable state. The system is valuable precisely because it makes these distinct questions visible rather than hiding them behind one validation badge.

The appropriate successful conclusion is narrow: another reader can reproduce a selected result, locate the source framing, inspect its units and assumptions, change a declared condition, preserve the new result and identify the records that require revision. Moving from this capability to biological explanation requires additional scientific work, not a change in the software's marketing label.

# 4. Selected upstream review

## Scope and method

Review date: 26 September 2026. The review used the connected GitHub reader for repository search, current README reads and complete root-tree reads where stated. The selected set comprises NephroCarePath, NEGENESIS-OMEGA, ProofLedger, AgentTrace, PRAXIS WorldLab and SCALE. The final book manuscript and source chapters were separately examined to define companion requirements.

This is an architecture-and-delivery review grounded in public descriptions and two root trees. It is not an exhaustive audit of the author's repositories, a source-level security audit, or an empirical ranking of existing runtimes. Attempts to retrieve archived application binaries did not yield usable source in the working environment. Their internal code and tests were therefore not executed. The distinction matters: a root containing only README, LICENSE and ZIP does not establish that the ZIP has no real implementation.

Machine-readable observations are in `nephrogenesis/data/upstream_review.json`. SHA values identified as trees are Git tree objects, not commit IDs. They identify the observed path inventory but are not a claim that an entire repository history was inspected.

## NephroCarePath: complementary domain, different scientific question

The README presents DIKWP NephroCarePath OS as a kidney-care triage, treatment-preparation, rehabilitation, follow-up and AI-governance prototype. It explicitly excludes diagnosis, prescriptions, dialysis settings and transplant eligibility decisions. The observed complete root tree contains LICENSE, README.md and a 59,900-byte application ZIP. Tree SHA: `61048ab055ac1a072bd35d2f0b4cf68123611f83`; archive blob SHA: `c260ba7a4eb340be7d19cc9917871bd26ff1f63d`.

The relevant limitation is a mismatch between its documented care-workflow purpose and this book's experimental questions. A care ledger cannot, merely by being a ledger, explain why the same excretion can hide different internal transport work or how a delayed sensor changes a dynamical model. This is a scope distinction, not a claim that the existing application is defective. The new companion implements those independent mechanisms, unit contracts and numerical tests while remaining outside clinical decision support.

Source: https://github.com/YucongDuan/DIKWP-NephroCarePath-OS

## NEGENESIS-OMEGA: operationalize the energy distinction

The README emphasizes entropy-accounted operation, reconstructive memory, externality repair and plural future options. It expressly rejects conflating local order, global entropy reduction and moral value. That distinction is valuable and should not be discarded in a kidney companion.

The engineering extension is to attach unit-bearing calculations to the distinction. In this release, J/mol cannot be added to J; mmol/min cannot be mistaken for a concentration; a matched-action-budget experiment does not claim to measure total thermodynamic cost. No general “life value” scalar is derived from joules or bits. This is a specific implementation of a compatible design direction, not a comparative performance result against the unexecuted upstream runtime.

Source: https://github.com/YucongDuan/NEGENESIS-OMEGA

## ProofLedger: from source association to a testable claim boundary

The public README describes claim-to-evidence support, provenance and unsupported-claim detection. It also states limits to automatic truth verification. A scientific companion needs to preserve that restraint: attaching a citation does not establish that a numerical quantity has the right units or that a synthetic result is empirical evidence.

The new graph therefore represents evidence kinds, source locators, model input/output requirements and dependency invalidation. It blocks an empirical-status claim whose ancestry includes synthetic or hypothesis nodes. It can mark an interpretation stale when an upstream assumption is withdrawn. These checks operate on explicit declarations and do not certify the content of a paper. Because the archived source was not run, this review makes no claim about the exact text-matching algorithm, false-positive rate or source coverage of ProofLedger.

Source: https://github.com/YucongDuan/DIKWP-ProofLedger-OS

## AgentTrace: preserve replay custody, add scientific re-execution

AgentTrace's README describes semantic traces, run-level hash chains, risk events, replay packages and incident review. The runnable source is described as distributed in an application ZIP. These are adjacent to the need for a reproducible experiment record.

The companion binds a scientific protocol to code/data identity and complete numerical outputs, then actually reruns the model and compares the result. It distinguishes an unchanged log, a numerically equal recomputation and a bitwise identical serialization. This is an implemented scientific contract; it is not a claim that AgentTrace lacks all forms of re-execution. It also explicitly documents whole-chain rewriting as outside protection unless a receipt digest is preserved independently.

Source: https://github.com/YucongDuan/DIKWP-AgentTrace-OS

## PRAXIS WorldLab: follow its consolidation logic

The PRAXIS README explicitly prioritizes a small number of independently reproducible missions, source-first expansion, CI, review and release provenance rather than repository counts or stars. Its observed root tree nevertheless distributes the application in a ZIP alongside README and LICENSE. Tree SHA: `669a385c9a14e983c74448cf47cdc104c61e6a76`.

The companion follows the constructive part of that diagnosis. It is one installable domain package with all Python modules directly visible in the source archive, a common CLI, test suite, model registry and stable run format. Uploading the expanded directory would make those files directly reviewable in GitHub. Merely uploading the ZIP to a new repository would recreate the packaging limitation; the publication guide explicitly avoids that pattern. No unrequested repository creation or upstream edit has been performed.

Source: https://github.com/YucongDuan/DIKWP-PRAXIS-WorldLab-v1.0

## SCALE: preserve plural objectives and simulation status

SCALE's README describes synthetic workload/resource allocation, Pareto plans, resource passports and recovery records. It explicitly states that its demonstration does not connect to real clouds, power systems or model APIs. This is a useful example of distinguishing a reference model from a production integration.

The kidney companion transfers the multi-objective discipline to a limited maintenance experiment: enumerate a finite set of resource/control settings, retain coupled energy and time inside a declared constraint box, and compute nondominated configurations. It does not infer a clinical optimum or an infinite-horizon viability kernel. Model scope and chosen parameter ranges remain visible instead of being absorbed into a universal score.

Source: https://github.com/YucongDuan/DIKWP-SCALE-

## What has and has not been surpassed

This delivery advances the book-companion task from documented governance and workflow concepts to an executable domain kernel with direct source, unit checks, conservation records, counterfactual task variants, calibrated surrogate fitting, explicit evidence revisions and sealed recomputation. Those are concrete additions demonstrated by this release's tests.

It has not demonstrated higher biological accuracy, better clinical outcomes or better runtime performance than the upstream projects. It has not established the independent existence of an information field. It has not implemented a complete spatial kidney, a molecular dynamics engine, an evolutionary phylogeny model or a medically validated digital twin. Treating these as future scientific work preserves the value of the implementation rather than weakening it with unsupported claims.

# 5. Eighteen chapter laboratories

Each chapter has one executable passport. These are distinct questions and experiments, not eighteen anatomical organ models. Exact source hashes are in nephrogenesis/data/chapters.json.

| Chapter | Experiment | Reproducible question |
|---|---|---|
| 1 | balance | Can a stable concentration conceal continuous exchange? |
| 2 | physical-budget | How does a rate become an energy cost, and which costs are omitted? |
| 3 | membrane | What does a boundary change when total solute is conserved? |
| 4 | geometry | Why does increasing size change exchange constraints? |
| 5 | habitats | How does concentrating capacity change a hypothetical water budget? |
| 6 | branching | Can increasing terminal count also increase network resistance? |
| 7 | filtration | How are blood flow, plasma flow and filtration fraction related? |
| 8 | transport | Can equal excretion hide different reabsorptive work? |
| 9 | concentration | What distinguishes free-water clearance from urine volume? |
| 10 | acid | Why is urine acidity alone insufficient to determine net acid excretion? |
| 11 | signal | Can identical action budgets produce different outcomes because correspondence changes? |
| 12 | memory | How does an explicitly retained history variable change a repeated response? |
| 13 | repair | Can functional recovery outrun structural recovery? |
| 14 | replacement | Which functions remain uncovered by a hypothetical replacement design? |
| 15 | identifiability | Which transient observation distinguishes equal-equilibrium mechanisms? |
| 16 | energy-information | How must molar and per-particle energies be reconciled before comparison? |
| 17 | scales | What do conditional physical limits say, and what do they not say about an organ? |
| 18 | evidence | What should change downstream when an assumption or source is withdrawn? |

For each passport, the workbook includes method, command, source anchors, extension status, an exercise and an explicit limitation. Read docs/CHAPTER_LABS.md rather than inferring the scope from the short experiment name.
# 6. Interfaces and data contracts

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

# 7. Validation and limitations

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

# 8. Deployment, contribution and attribution

New code and original companion documentation use Apache-2.0. The book text is not bundled or relicensed. Book authorship does not imply that either author reviewed or approved this implementation. No upstream application code or ZIP is redistributed. CITATION.cff supplies software citation metadata without inventing a DOI or public repository URL.

The deployment is deliberately local and single-user. Keep the server on loopback. There is no authentication, TLS, patient record system, remote device interface or clinical action authorization. The implementation checks fixed routes, Host/Origin, request size, numeric bounds and input keys, but it is not a production hosting framework. SECURITY.md explains local persistence, request handling, escaping and the hash-chain threat model [PYTHON-HTTP].

For public source publication, upload the expanded source tree rather than only the delivery ZIP. Enable the supplied CI workflow and review results after it actually runs. Maintain one model registry and versioned contract rather than spawning unrelated repositories for every experiment. Changes to scientific code or shipped model data require new run identities; preserve previous releases for reproduction.

A new anatomical model, a real dataset adapter, an independent researcher evaluation and a falsifiable physical-field theory are separate research contributions. None can be established by renaming this reference implementation. The extension roadmap identifies their missing evidence and engineering requirements in docs/RESEARCH_ROADMAP.md. The neutral review envelope is an interchange proposal; it is not advertised as a tested native API connection to upstream systems.

# 9. Source register

[BOOK] Yucong Duan and Zhongdao Wu. A Brief History of the Kidney. User-provided final manuscript and source chapters. SHA-256 identities are in nephrogenesis/data/book_manifest.json. Source anchors are used instead of renderer-dependent page numbers. Publisher acceptance is not assumed.

[NIST-SI] National Institute of Standards and Technology. Fundamental Physical Constants, complete listing, 2022 CODATA adjustment. Retrieved 26 September 2026. https://physics.nist.gov/cuu/Constants/Table/allascii.txt

[PYTHON-HTTP] Python Software Foundation. http.server: HTTP servers, official documentation. Retrieved 26 September 2026. https://docs.python.org/3/library/http.server.html

[UPSTREAM] Six public repository descriptions and two complete root trees, reviewed 26 September 2026. URLs, observed scope, review limits and tree identifiers are listed in section 4 and nephrogenesis/data/upstream_review.json. Archived application source was not executed.

[IMPLEMENTATION] NEPHROGENESIS-Lab contributors. Version 1.0.0. Newly generated conditional equations, synthetic fixtures, model code and original English documentation in this release. Local execution results are in validation/. No independent clinical or field-physics validation is claimed.
