# Chapter-to-experiment passports

The following descriptions are original English companion material. Source chapters are identified by SHA-256 in the machine-readable passports; the book text is not reproduced.

## Chapter 1: The kidney problem: maintaining an internal world

**Question.** Can a stable concentration conceal continuous exchange?

**Method.** Run an open one-compartment balance and inspect cumulative stock-flow residuals.

**Source anchors.** Book sections 1.2, 1.5.

**Run.** `python run.py run balance --out runs/ch01`

**Exercise.** Run balance with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** Not a validated human renal digital twin.

## Chapter 2: Cosmic matter and nonequilibrium conditions

**Question.** How does a rate become an energy cost, and which costs are omitted?

**Method.** Use a dimension-checked sodium/ATP coupling equation with declared stoichiometry.

**Source anchors.** Book sections 2.5, 8.17.

**Run.** `python run.py run physical-budget --out runs/ch02`

**Exercise.** Run physical-budget with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** Excludes basal metabolism and unmodeled losses.

## Chapter 3: Boundaries, metabolism and inheritance

**Question.** What does a boundary change when total solute is conserved?

**Method.** Compare exact two-compartment passive exchange trajectories with a conserved total.

**Source anchors.** Book sections 3.2, 3.17.

**Run.** `python run.py run membrane --out runs/ch03`

**Exercise.** Run membrane with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** Fixed volumes; does not solve coupled osmosis or the origin of life.

## Chapter 4: The transport cost of multicellularity

**Question.** Why does increasing size change exchange constraints?

**Method.** Compute spherical area/volume and a conditional diffusion-time estimate across five radii.

**Source anchors.** Book sections 4.1, 4.16.

**Run.** `python run.py run geometry --out runs/ch04`

**Exercise.** Run geometry with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** Geometry is an explanatory constraint, not a historical proof of organ inevitability.

## Chapter 5: Ocean, fresh water and land: alternative histories

**Question.** How does concentrating capacity change a hypothetical water budget?

**Method.** Calculate required excreted volume at three hypothetical osmolarity limits.

**Source anchors.** Book sections 5.17, 9.17.

**Run.** `python run.py run habitats --out runs/ch05`

**Exercise.** Run habitats with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** Not measured species data or a reconstruction of evolutionary ancestry.

## Chapter 6: Building a kidney: development and geometry

**Question.** Can increasing terminal count also increase network resistance?

**Method.** Combine symmetric cylindrical segment resistances and terminal area across branching depths.

**Source anchors.** Book sections 6.16.

**Run.** `python run.py run branching --out runs/ch06`

**Exercise.** Run branching with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** Terminal branches are not automatically functional nephrons.

## Chapter 7: Filtration: selective openness

**Question.** How are blood flow, plasma flow and filtration fraction related?

**Method.** Compute RPF and filtration fraction from explicit flow measurements and hematocrit.

**Source anchors.** Book sections 7.15.

**Run.** `python run.py run filtration --out runs/ch07`

**Exercise.** Run filtration with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** Conditional arithmetic, not an eGFR diagnostic service.

## Chapter 8: Reabsorption and secretion: the energy account

**Question.** Can equal excretion hide different reabsorptive work?

**Method.** Hold excretion fixed while changing filtered load and calculate the resulting coupled power.

**Source anchors.** Book sections 8.15, 8.17, 18.8.

**Run.** `python run.py run transport --out runs/ch08`

**Exercise.** Run transport with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** Active fraction is assumed; no whole-organ calorimetry is claimed.

## Chapter 9: Concentration and dilution: water and spatial organization

**Question.** What distinguishes free-water clearance from urine volume?

**Method.** Compute osmolar and free-water clearances with volumetric osmolarity units.

**Source anchors.** Book sections 9.15.

**Run.** `python run.py run concentration --out runs/ch09`

**Exercise.** Run concentration with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** Osmolality cannot be substituted without a justified conversion.

## Chapter 10: Acid-base balance and systemic functions

**Question.** Why is urine acidity alone insufficient to determine net acid excretion?

**Method.** Add ammonium and titratable acid and subtract urinary bicarbonate loss.

**Source anchors.** Book sections 10.15.

**Run.** `python run.py run acid --out runs/ch10`

**Exercise.** Run acid with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** Not a diagnostic or treatment recommendation.

## Chapter 11: Sensing, control and DIKWP

**Question.** Can identical action budgets produce different outcomes because correspondence changes?

**Method.** Compare matched, fixed, shuffled, delayed, reversed and calibrated-remap policies on one sequence.

**Source anchors.** Book sections 11.19, 16.22, 16.23.

**Run.** `python run.py run signal --out runs/ch11`

**Exercise.** Run signal with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** Only action budgets are matched; total sensing/computation cost is not measured.

## Chapter 12: Time, memory and aging

**Question.** How does an explicitly retained history variable change a repeated response?

**Method.** Compare two identical challenge protocols with different assumed hidden-state histories.

**Source anchors.** Book sections 12.5, 12.17, 18.11.

**Run.** `python run.py run memory --out runs/ch12`

**Exercise.** Run memory with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** The latent state is assumed rather than identified from observations.

## Chapter 13: Injury, disease and repair

**Question.** Can functional recovery outrun structural recovery?

**Method.** Compare explicitly chosen fast and slow exponential recovery modes.

**Source anchors.** Book sections 13.5, 13.15.

**Run.** `python run.py run repair --out runs/ch13`

**Exercise.** Run repair with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** No empirical prognosis, repair mechanism or regeneration claim follows.

## Chapter 14: Replacement, regeneration and the artificial kidney

**Question.** Which functions remain uncovered by a hypothetical replacement design?

**Method.** Expose coverage of five functions without compressing them into a single score.

**Source anchors.** Book sections 14.17, 18.14.

**Run.** `python run.py run replacement --out runs/ch14`

**Exercise.** Run replacement with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** Numbers describe an invented device, not an existing dialysis or transplant intervention.

## Chapter 15: Mathematics, causality and a computable kidney

**Question.** Which transient observation distinguishes equal-equilibrium mechanisms?

**Method.** Compare two exact one-compartment trajectories and maximize a declared noise-normalized separation.

**Source anchors.** Book sections 15.4, 15.8, 15.19.

**Run.** `python run.py run identifiability --out runs/ch15`

**Exercise.** Run identifiability with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** Choice is conditional on the candidate set and specified observation noise.

## Chapter 16: Energy and information: two descriptions

**Question.** How must molar and per-particle energies be reconciled before comparison?

**Method.** Reproduce the Avogadro conversion and logical-erasure comparison with dimensional algebra.

**Source anchors.** Book sections 16.12.

**Run.** `python run.py run energy-information --out runs/ch16`

**Exercise.** Run energy-information with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** A dimensionless ratio is not a measured count of biologically processed bits.

## Chapter 17: Scales, boundaries and possible life

**Question.** What do conditional physical limits say, and what do they not say about an organ?

**Method.** Compute Planck scales, light travel time and an information bound within a declared weak-gravity range.

**Source anchors.** Book sections 17.5, 17.7, 17.9.

**Run.** `python run.py run scales --out runs/ch17`

**Exercise.** Run scales with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** Bounds do not establish spacetime discreteness or actual kidney memory capacity.

## Chapter 18: Open theories, experiments and the ultimate question

**Question.** What should change downstream when an assumption or source is withdrawn?

**Method.** Validate a typed evidence graph and propagate withdrawal through all dependent nodes.

**Source anchors.** Book sections 18.13, 18.20.

**Run.** `python run.py run evidence --out runs/ch18`

**Exercise.** Run evidence with defaults; change one declared parameter; preserve both receipts; report which assumption explains the difference.

**Failure test.** Identify an observation, unit mismatch or conservation failure that would invalidate the stated interpretation.

**Boundary.** Logical validity does not establish source truth; the associated ablation is a designed software fixture.
