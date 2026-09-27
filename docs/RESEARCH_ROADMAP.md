# Research extension roadmap without invented completion

## From teaching surrogate to mechanistic model

The next meaningful extension is not another wrapper around the same outputs. A spatial nephron model would require explicit segment geometry, luminal/interstitial/blood compartments, transport kinetics, osmotic coupling, electroneutrality and conserved species. Its validation should compare analytic limiting cases, grid/time refinement and independently reported experimental or established simulation benchmarks. The present release does not implement that model. It supplies the unit, experiment and provenance interfaces into which such a model can be added.

## From asserted evidence to usable research evidence

CSV calibration already accepts an operator-declared research curve and separates training from held-out data. Extending this to independent evidence requires dataset identity, measurement units, sampling protocol, uncertainty, exclusions and a provenance record outside the operator's assertion. Patient-specific data bring additional permission, de-identification and institutional responsibilities that this local companion does not resolve. No unrequested hospital, device, registry or cloud integration has been created.

## From illustrative information to a field hypothesis

The additional-effect experiment fits a sinusoidal basis to generated observations. It is not an independent-field model. A proposed field needs its own measurable variable, dimensions, dynamics, coupling to observed processes, controls matching known physical variables and a preregistered difference from a baseline. Once those are supplied, the hypothesis interface can encode them as a new candidate, preserve the prediction before observing a held-out result and record null or contradictory findings. A residual alone does not name its cause.

## From designed ablation to independent assessment

The software fault suite demonstrates that enabled checks catch errors designed to exercise them. Testing the stronger book question—whether DIKWP improves research judgment—requires independently assembled, blinded cases, a baseline with comparable engineering resources, predefined success/failure criteria and scoring that distinguishes documentation completeness from scientific correctness. It should preserve negative results, reviewer disagreement and task specificity. No such independent evaluation is claimed here.

## From source package to a maintained commons

Publish the expanded repository contents, not just a nested archive. Keep the kernel, chapter passports and domain models in one coherent source tree. Review a small model change through issue, test, code review and versioned release. Preserve the original run receipts when the source digest changes. Hosted CI should be run after repository publication, not inferred from the existence of a YAML file. External reproducibility should be counted only after an independent runner actually completes and reports the commands.

The user has not requested publication in this task. The delivery therefore provides the source tree, wheel, license, citation metadata and CI configuration without creating a repository, pushing commits or assigning maintainers. A publication record should use the actual destination, tag and resulting commit rather than a prewritten claim that these already exist.
