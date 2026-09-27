# Operator guide and reproducible study sessions

## 1. First successful run

Extract the source release into a normal writable directory. Paths containing spaces are supported. Open a terminal there and run `python run.py verify`. The output should contain 22 successful equation checks. Run `python -m unittest discover -s tests -v` for the broader software suite. The executed count and environment are recorded in `validation/VALIDATION.json`; do not confuse the test suite with clinical validation.

Start `python run.py serve --port 8765` and open the printed loopback address. The browser initially selects the hidden-work experiment. Change one parameter, press Run, and inspect its metric cards, table and limitations. A red error is an input-contract failure rather than a successful experiment. Reset returns to the declared default. Export JSON saves the browser result. Browser runs are not automatically archived; the CLI should be used for a reproducible record.

The precomputed `SHOWCASE.html` can be opened directly when no Python environment is available. It demonstrates actual outputs produced by the release and includes the complete result data in expandable sections. It is a reading artifact, not an offline JavaScript substitute for the Python numerical engine.

## 2. Session A: see the unobserved work

Read book sections 8.15, 8.17 and 18.8. Run `python run.py run transport --out runs/work-a`. Inspect `table.csv`: the two rows have equal excretion and different reabsorption. Explain exactly why the chosen energy assumptions produce a difference. Then create a JSON configuration with a different active fraction and run it into a new empty directory.

The expected invariants are the excretion equality and the relation filtered minus reabsorbed equals excreted. The power difference is not invariant to stoichiometry or active fraction. The task is complete only when the interpretation specifies what was held fixed and what was changed. A claim that the experiment measured actual energy consumption in a kidney exceeds the run's evidence.

Use `python run.py verify-run runs/work-a` to check its internal integrity and `python run.py replay runs/work-a` to recompute it. The latter should report both numerical agreement and whether serialization is identical. Save the printed receipt digest separately when the run is part of an auditable research exchange.

## 3. Session B: correspondence is not just message count

Run `python run.py run signal --config examples/matched_signal.json --out runs/signal-a`. Compare matched, fixed, shuffled and delayed strategies without changing the observations or action budget. Now increase `error_probability` above 0.5 and inspect reversed and calibrated-remap performance. Explain why knowing an inverted mapping differs from receiving an accurate raw observation.

The experiment's signal sequences and recovery units are invented. Its purpose is to make the book's functional-information question operational. It does not measure complete sensing energy or infer subjective experience. In a report, retain the theoretical binary-channel information, the realized task accuracy and the stated energy budget as separate quantities.

## 4. Session C: distinguish a mechanism rather than collect another endpoint

Run `python run.py run identifiability --out runs/design-a`. Both mechanisms end at the same equilibrium but traverse different transients. Inspect the observation-time score and derive its meaning from the assumed noise variance. Change the noise standard deviation: the preferred time on the grid may remain unchanged even while the discrimination strength decreases. This distinction separates the shape of an optimal measurement design from its achievable certainty.

Next run `python run.py run hypothesis --config examples/registered_extension.json --out runs/extension-a`. The model basis and split are fixed before amplitude estimation. Do not choose a new basis after viewing held-out residuals and continue calling the old test held out. Such a change creates a new exploratory experiment and needs a new independent evaluation set.

## 5. Session D: supply a research curve

The example CSV contains a generated concentration-time curve with explicit train/test labels. Execute:

```bash
python run.py fit --data examples/synthetic_curve.csv --metadata examples/curve_source.json --out runs/fit-a
python run.py replay runs/fit-a
```

For an authorized non-identifying research dataset, preserve the exact column header `time_min,concentration_mmol_L,split`. Do not rename another unit to these labels. Convert units explicitly first and document the conversion in the source locator or an associated record. Data must contain 5–200 rows, strictly increasing times, a training time-zero initial condition, at least three training rows and two test rows.

The metadata identifies whether the data are synthetic or operator-declared research observations and confirms rights to use them. It does not make the observations independently verified. If the fitted optimum reaches a grid boundary, extend the scientifically justified parameter range or reconsider the model in a new run. Do not report a boundary flag as a precise parameter estimate or treat low test error as a diagnosis.

## 6. Session E: resource limits and historical controls

Run `python run.py run dynamics --config examples/delayed_compartment.json --out runs/delayed-a`. Compare with a default feedback run saved separately. Inspect cumulative water, sodium and urea residuals as well as final concentrations. A controller can keep one endpoint closer to the chosen box while spending more of the specified transport budget. Resource-cap operation may also change the entire concentration trajectory.

Run `uncertainty` to vary declared parameters, and `viability` to enumerate gain/budget combinations. Interpret an ensemble spread as a scenario spread, not a population confidence interval. Interpret a Pareto point as nondominated within the tested set, not globally optimal. The finite horizon and known disturbance are part of the conclusion.

## 7. Session F: retract an assumption cleanly

Validate `examples/evidence_graph.json` using the evidence command. Then run:

```bash
python run.py evidence examples/evidence_graph.json --withdraw synthetic-flux --out runs/withdrawal.json
```

The withdrawal marks the input withdrawn and dependent conversion, calculation, interpretation and revised question stale. It does not erase the earlier record. Replacing a source with a new version requires a new explicit record and rerun; it is not equivalent to changing a URL while leaving dependent claims marked current.

The `ablation` experiment is a teaching exercise about these checks. Its cases were designed to contain specified faults and are not a blinded evaluation of researchers. A credible independent evaluation would use unseen cases and a comparable baseline rather than extending these fixtures until one method wins.

## 8. Typical failures and recovery

“Unknown unit” means the registry has no justified conversion. Supply a supported unit or add a reviewed dimensional definition with tests; do not bypass the validator. “Event interval outside the horizon” means that shortening a dynamic experiment left its default disturbance outside the new time window. Provide a consistent event list. “Output directory must be absent or empty” protects the previous run; choose a new directory.

“Model/code identity changed” means the current executable release no longer matches the recorded one. Reuse the original release for reproduction or create a new versioned experiment. “State left the positive compartment domain” is an explicit solver/model-domain failure. Shorter steps may clarify a numerical issue, but changing the step cannot justify a physically unsuitable scenario.

If the browser cannot connect, verify that the terminal server is still running and that the address uses the same port. A foreign Host/Origin is deliberately rejected. This local design is not intended to be made public by editing a bind address. No password or patient data should be inserted into a configuration file merely to overcome an interface error.
