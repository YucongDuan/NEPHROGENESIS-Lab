# Contributing

Start with a reproducible question rather than a new operating-system name. Keep each change small enough that another researcher can state its assumptions and run its tests.

Run `python -m unittest discover -s tests -v` and `python run.py verify`. A numerical change needs a regression, a domain-failure test, unit definitions, and a conservation or analytic check where applicable. Changed dynamics need a step-refinement comparison. A new evidence source needs a precise locator and a declared evidence kind. Do not promote a synthetic result to an empirical claim.

Add laboratory metadata in `nephrogenesis/experiments.py`, an English model card in `docs/METHODS.md`, and a book section anchor only after reading the relevant section. Changes to a chapter passport must preserve its source hash or explicitly update it to the new source version.

Do not upload patient identifiers, institutional credentials or proprietary book text. Do not use test fixtures to represent clinical benefits. Preserve failed runs and uncertainty when comparing models. A numerical result that does not support the expected narrative is still a useful contribution.

No external reviewer or maintainer has been appointed by this delivery. Repository maintainers must establish their own review and release permissions before public deployment.

Before producing a new reviewed release, update the version, rebuild the wheel, preserve new execution results and regenerate RELEASE_MANIFEST.json with `python scripts/build_release_manifest.py --confirm-new-inventory`. An inventory mismatch must be investigated, not silently accepted. A development pull request that changes tracked source must update the inventory deliberately.
