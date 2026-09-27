# Scientific methods and model cards

## 1. Interpretive contract

The manuscript asks for a model deliverable that reveals its problem, data, units, parameters and failure conditions rather than only its output picture (book section 15.23). It also asks whether a proposed additional information field makes a distinguishable prediction (16.24), and whether DIKWP improves a task relative to an explicit baseline (18.13). Those are the source-derived requirements. The algorithms in this release are new companion implementations; the book does not claim that these software experiments already established their scientific hypotheses.

Three statuses remain separate. A conditional equation can be mathematically correct under its assumptions. A synthetic experiment can expose consequences of a stipulated model. An empirical inference requires observations, appropriate experimental design, competing explanations and external validation. Source hashes, type labels and repeated runs cannot turn the first two into the third. Imported research observations remain operator-declared observations rather than software-certified truth.

The numerical core uses quantities at the scale of the question being asked. Molar chemical work, per-particle erasure energy, volume flow and empirical evidence status do not share one interchangeable scalar. The purpose of the semantic layer is to preserve these distinctions and permit revision, not to assign data, information, knowledge, wisdom and purpose to five anatomical structures.

## 2. Dimensional and semantic quantity algebra

The `Quantity` class carries a base-dimension exponent vector for length, mass, time, amount, temperature and charge. Addition requires identical dimensions and matching semantic tags. Multiplication/division adds or subtracts exponent vectors. Conversion is allowed only through an explicit registry. Unknown strings do not trigger a guessed conversion, and the implementation does not evaluate user formula strings.

An osmole and an equivalent are represented as semantic kinds associated with amount. This prevents a concentration in mmol/L from silently becoming mOsm/L, and prevents mOsm/kg from becoming mOsm/L. Determining an activity coefficient, osmotic coefficient, valence conversion or density requires an explicit additional model. Tagged algebra is intentionally restricted; the domain calculators perform their declared equations instead of pretending the registry is a complete physical-units system.

Numbers must be finite and not booleans. A logarithm accepts only a positive dimensionless ratio. The default transport example multiplies 1 nmol ATP/s by 50 kJ/mol and obtains 50 microwatts. Replacing J/mol with J is rejected. For the erasure comparison, a molar electrochemical work must be divided by Avogadro's constant before division by k_B T ln 2. Equivalently, the denominator is R T ln 2. This dimensionless result is a comparison of energy scales, not an observation of the number of bits processed by an organ.

Constants used for these calculations match the NIST 2022 CODATA listing retrieved on 26 September 2026: k_B, N_A, h and c use their exact SI definitions; G is a measured constant. The code derives R from k_B N_A. The tiny tolerance used in numerical comparisons is a floating-point test tolerance, not the uncertainty of G or the biological parameters [NIST-SI].

## 3. Reduced regulated compartment: state and conservation

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

## 4. Control and resource assumptions

The default reference volume and sodium concentration are 14 L and 140 mmol/L. The default flows are chosen so the no-event, fixed-control scenario has a steady solution. These are teaching initial conditions, not a recommended personal target. The time-inside-box metric uses [13.5, 14.5] L and [135, 145] mmol/L as an arbitrary declared constraint box. Calling the metric a survival probability, a medical safety threshold or a viability theorem would be incorrect.

At the beginning of each step, a synthetic controller observes a volume/concentration pair. Fixed control ignores deviations. Feedback control uses the current pair. Delayed control uses the most recent stored pair no later than `t - delay`. Scrambled control samples an earlier stored pair using a seeded pseudo-random generator. Reversed control changes the sign of deviations. The implementation transforms requested water/sodium outputs into reabsorption fractions and holds those fractions over the RK4 step.

The whole solver is consequently a hybrid sampled controller, not a continuously evaluated fourth-order feedback system. Refining the step changes controller sampling as well as integration error. The tests demonstrate reduced error in a selected step-refinement comparison and fourth-order RK4 accuracy for an independent linear ODE; they do not claim uniform fourth-order convergence of the delayed controller.

Sodium-associated power uses the declared active fraction, three sodium ions per ATP and the chosen molar ATP free-energy magnitude. With reabsorbed sodium J_N in mmol/min:

```text
energy_rate_J_per_min = J_N * 0.001 * active_fraction / 3 * ATP_energy_J_per_mol
```

A resource ceiling in W is multiplied by 60 to obtain J/min, then inverted to cap the reabsorbed amount. The remainder exits the compartment. This is a mathematical resource constraint, not a mechanistic account of how a real kidney responds to ATP limitation. The remaining non-active fraction represents unmodeled coupled/passive pathways; thermodynamic feasibility of every allowed parameter combination is not established. Basal metabolism, leakage, sensor costs, mitochondrial efficiency and other energy exports are not measured or inferred.

## 5. Equal output does not identify the work

The `transport` experiment isolates one relation. Excretion is fixed at 0.1 mmol/min. Candidate filtered loads are 8 and 16 mmol/min, and secretion is excluded. Reabsorption is therefore 7.9 or 15.9 mmol/min. Under a declared active fraction of 0.6, three sodium per ATP and 50 kJ/mol ATP, ideal coupled powers are approximately 1.316667 and 2.65 W. Their difference is approximately 1.333333 W.

These numbers are generated by the scenario rather than measured from two organs. The scientific point is identifiability: identical terminal output need not determine gross internal flux. An experiment intended to test the relation in a biological preparation needs independently observed filtered load, recovery/secretory terms, relevant transport contributions and uncertainty. A counterexample to the claim that output alone identifies work is already supplied algebraically; estimating the actual work in a preparation is a separate task.

## 6. Two-compartment membrane exchange

The `membrane` experiment has two fixed volumes V_A and V_B, initial concentrations C_A0 and C_B0, and an exchange conductance k in L/min. It solves the linear passive exchange system exactly. The equilibrium concentration is the total amount divided by V_A + V_B, and the concentration difference decays at rate k(1/V_A + 1/V_B).

The mass residual V_A C_A + V_B C_B minus the initial total is checked along the trajectory. The example explains why a boundary and permeability matter to retention and exchange. It does not reconstruct the origin of life, calculate changing cell volume, or demonstrate that a primitive compartment can reproduce. Adding osmosis would require a water-flux equation, chemical potentials and explicit volume updates, with new conservation and domain tests.

## 7. Geometry, branching and alternative histories

The `geometry` experiment evaluates spherical area/volume ratios and an elementary diffusion-time scale. These answer related but different questions: surface exchange per unit volume and time to diffuse over a distance. They are not combined into a law stating that larger bodies must evolve human-like kidneys.

The `branching` experiment assumes a symmetric binary cylindrical network with fixed daughter/parent radius and length ratios. Each level contains parallel descendants. Normalized network resistance is the sum of powers of length_ratio/(2 radius_ratio^4). Terminal area scales as (2 radius_ratio^2)^depth. Increasing terminal count can therefore increase surface while worsening the resistance of particular geometries. These are conditional network calculations. Terminal count is not a nephron assay, vascular access, lineage tracing or evidence of mature organoid function.

The `habitats` experiment evaluates hypothetical concentrating capacities without assigning them to real species. It maintains the distinction between a shared water-budget constraint and a particular evolutionary history. Phylogeny, habitat exposure, nitrogen chemistry, body size and nonrenal routes would need separate data before a comparative biological argument is warranted. This choice avoids silently replacing the book's branching evolutionary account with an unsupported ladder of superiority.

## 8. Signal correspondence under a matched action budget

The `signal` experiment uses a two-state task arranged in alternating blocks. A binary symmetric observation channel flips each state with a declared probability. The same observations are supplied to matched, fixed, shuffled, delayed, reversed and calibrated-remap strategies. Each action consumes a stipulated 1 J. A correctly located action recovers four toy units; an incorrectly located action recovers none.

All strategies have the same observation count and assigned action cost. The objective is to expose how mapping and timing change a task outcome without changing that chosen budget. The run does not account for total sensing/computation thermodynamics. In particular, arbitrary recovery units cannot be added to joules. The mutual-information value is the theoretical balanced-input binary-channel value 1 - H_b(error), not a numerical estimate of an independent physical field. A finite task sequence need not have exactly the same distribution as that theoretical channel assumption.

When the error exceeds one half, a decoder that knows the channel can invert its outputs. The calibrated-remap strategy is granted the declared error rate; it does not learn it from held-out observations. A favorable result therefore says nothing about the cost of learning the mapping. A stronger future experiment should estimate the decoder on training observations, reserve a separate test sequence, and measure or bound the cost of sensing and remapping. Those additions are not claimed as implemented here.

## 9. Time, repair and replacement

The `memory` experiment explicitly stipulates a hidden state h(t)=h0 exp(-lambda t) and a response s(t)(1+h(t)). It shows what follows from that assumed history variable. It does not infer which biological substrate stores history, or distinguish ongoing exposure from a lasting cell-state change. A real identification task needs repeated perturbations and observations capable of separating those explanations (book sections 12.17 and 18.11).

The `repair` experiment compares fast and slow exponential modes representing two declared deficits. Its point is that an observed functional endpoint and an assumed structural/reserve endpoint can recover at different rates. The curves are not fitted disease trajectories. The book's distinction among cell function, connection restoration and whole-organ reserve remains a conceptual requirement rather than a claim that all three mechanisms have been simulated.

The `replacement` laboratory displays a five-function coverage vector for an invented device. A single clearance score does not automatically imply endocrine regulation or renewal. No weighted overall score is calculated, and the entries do not describe dialysis, transplantation or a commercial system. The next implementation step would be a unit-bearing test contract for each function and independently measured device results, not a more persuasive name for the synthetic entries.

## 10. Identifiability and observation design

Two candidate ODEs dC/dt = G - kC have G/k = 10 mmol/L. Candidate A uses G=0.2 mmol/L/min and k=0.02/min; B uses G=0.1 and k=0.01. Starting at C0=20, the exact trajectory is C*=10 plus (C0-C*) exp(-kt). One observation at equilibrium cannot uniquely recover the two parameters. A transient can separate the declared candidates.

The design score is squared candidate separation divided by a specified observation variance. For this pair the continuous maximum lies at ln(2)/0.01 minutes; the workbench selects the best time on its finite 101-point grid. The default horizon yields a grid optimum near 70.2 minutes. This is a candidate-discrimination calculation, not a general optimizer for laboratory scheduling. It omits sampling cost, temporal noise correlation, model discrepancy and ethical constraints.

The `hypothesis` experiment compares a fixed baseline against one preregistered sinusoidal additional-effect basis. Only the extension amplitude is fitted, using even-index samples. Odd-index outcomes are held out. The known-variance Gaussian BIC expression drops a constant shared by the candidates. A separate held-out MSE is reported. The synthetic generator can inject a sinusoid, so success under that fixture is deliberately favorable to the extension. It is not evidence for a new information field. A real field proposal needs an operational field variable, units, coupling law, controls against known confounds and differential predictions before entering this interface.

## 11. Calibration to explicitly supplied observations

The `calibration` experiment and `fit` command accept 5–200 observations with columns `time_min,concentration_mmol_L,split`. The first observation must be a training initial condition at time zero. Times strictly increase, at least three rows are training rows and at least two are held out. The source declaration requires an identifier, kind, locator and affirmative rights statement. A declaration is retained; it is not independently verified by this software.

The fit searches a bounded rectangular grid over k and C*. It fixes C0 at the first training observation and minimizes unweighted training SSE. The default 61 by 61 grid contains 3,721 candidates. It then computes predictions and held-out MSE without refitting, and reports the initial-concentration constant predictor as a transparent baseline. A boundary optimum generates a flag rather than being silently interpreted as a precise biological rate.

This is useful for reproducing a specified low-dimensional surrogate, not diagnosing kidney function. No uncertainty interval is reported: initial-condition noise, correlated errors, structural mismatch and grid resolution are not modeled. The included exact synthetic curve is recoverable on the default grid and provides a software sanity check. Tests perturb only held-out concentrations and verify that fitted parameters do not change. Real research use should add alternative structures and data-quality analysis before treating a fitted parameter as a meaningful mechanism.

## 12. Scenario uncertainty and finite-horizon screening

`uncertainty` draws reproducible independent uniform values for GFR and active fraction from declared teaching ranges, then reruns the reduced model. It reports min, median, max and all individual outcomes. These are scenario summaries, not population estimates, posterior intervals or confidence bounds. Correlated parameter distributions are not supplied.

`viability` enumerates twelve fixed controller-gain/resource-ceiling combinations for one specified disturbance and a finite horizon. It retains energy and time inside the arbitrary constraint box as separate objectives and returns nondominated configurations. It is neither an infinite-horizon viability kernel nor a proof of robustness to unobserved disturbances. A failed domain run remains labeled as a failure instead of being assigned a favorable score.

## 13. Falsification and invalidation

Each experiment preserves its boundary, units and input declarations. The evidence graph additionally records kind, DIKWP role, source locator, dependencies and optional input/output contracts. The graph cannot contain a cycle, although conceptual roles may revisit D, I, K, W or P in successive nodes. Dependence on synthetic or hypothesis nodes cannot establish empirical status. A withdrawn source makes transitive dependents stale.

The `ablation` benchmark removes checks from a deliberately constructed fault set. It compares an untyped record, unit-only checks, units plus provenance, and the full contract. It exercises actual validators for incompatible units, missing source locators, a broken balance, synthetic-to-empirical promotion and stale dependencies. The favorable result for the full contract is a designed software regression, not an independent evaluation of DIKWP against human researchers or upstream software. A future blinded evaluation would need independently constructed cases, predefined scoring, observer agreement and a baseline with comparable engineering effort.

## 14. Reading a successful run correctly

A zero conservation residual can coexist with a wrong physiological model. A perfectly replayed run can repeat a mistaken assumption. A typed evidence graph can contain a false external source. A small held-out error on one generated dataset can reflect a favorable generator. A mathematically valid upper bound can be irrelevant to an organism's attainable state. The system is valuable precisely because it makes these distinct questions visible rather than hiding them behind one validation badge.

The appropriate successful conclusion is narrow: another reader can reproduce a selected result, locate the source framing, inspect its units and assumptions, change a declared condition, preserve the new result and identify the records that require revision. Moving from this capability to biological explanation requires additional scientific work, not a change in the software's marketing label.
