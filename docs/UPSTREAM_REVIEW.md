# Review of the selected Yucong Duan portfolio

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
