# Suppressed Physics R&D — Ground Rules

These rules are NON-NEGOTIABLE. They override any instinct to be agreeable, helpful, or validating.

## 1. Never validate what hasn't been tested

- If a hypothesis is INPUT to the simulator, it CANNOT be claimed as OUTPUT.
- Distinguish: "the model assumes X" vs "the model predicts X" vs "the model validates X."
- A result that follows directly from an assumption is NOT a finding. It's a tautology.
- When reporting results, explicitly state which assumptions produced them.

## 2. Do not make the illogical logical

- If the math doesn't work, say so. Don't soften it, don't hedge toward "but maybe."
- If a hypothesis fails a test, report the failure cleanly before exploring alternatives.
- Negative results are results. A flat frequency sweep IS the finding.
- Never adjust the analysis to rescue a hypothesis. Adjust the hypothesis to fit the analysis.

## 3. Rigor hierarchy

For every claim, categorize it:
- **Verified**: Matches textbook physics, independently calculable, no model assumptions needed
- **Model prediction**: Follows from simulator physics, but simulator has known limitations
- **Hypothesis**: Not yet testable with current tools — state what WOULD test it
- **Circular**: Baked into the model as an assumption — CANNOT be claimed as validated

When presenting results, ALWAYS state which category applies.

## 4. Known simulator limitations

The SPH/MHD module:
- HAS eddy-current induction physics: η(ω) = ωτ_d/(1+(ωτ_d)²), skin depth P(r,R,δ)
- Frequency coupling VERIFIED analytically (exp 20): peaks at f_d within 3%
- BUT: EM induction force is ~1000× weaker than gravity at bench scale (5cm, ambient σ)
- SPH internal dynamics (pressure, boundaries, damping) mask the EM signal at bench scale
- Has NO induced magnetic field feedback below dynamo threshold
- Core dynamics previously contained hardcoded RS boost (now has disable flag)
- CANNOT meaningfully test: EM-driven flow at bench-scale ambient σ (force too weak)

The PIC plasma module:
- Is honest single-particle physics (Boris pusher is verified)
- Has NO collective effects (no particle-particle interaction)
- CANNOT test: collective plasma modes, wave propagation, instabilities

## 5. What IS validated (as of 2026-02-22, post clean reruns)

- **3D plasma rotation** (Q_3d ≈ 1.0): Real PIC physics, Boris pusher verified
- **Dynamo threshold** (Rm ≈ 10): Real SPH physics, sharp transition, RS-independent (confirmed clean rerun)
- **Cyclotron resonance impossible at bench B**: Pencil math, textbook Biot-Savart
- **Eddy-current coupling η(ω)**: Analytical peak at f_d = 1/(2πμ₀σR²), verified (exp 20)
- **Faraday induction monotonic** (∝ f^0.87): Real PIC, no resonance peak
- **Centering = density physics**: Clean reruns (exp 1,3,5) identical with/without RS mechanisms. Equilibrium driven by Δρ from mercury (Archimedes) + field gradient geometry. RS coupling factor only scaled approach speed, not final position.
- **Axis hierarchy (3>2>1)**: Real field geometry, confirmed identical in clean rerun (exp 3)

## 6. What is NOT validated (as of 2026-02-22)

- RS frequency formula (was circular — hardcoded, then "confirmed"; flat when disabled)
- RS amplitude ratios producing physical effects (exp 21: no effect found)
- RS coupling factor affecting equilibrium (clean reruns: zero effect on final positions)
- Any frequency preference in MHD (flat when RS boost removed)
- Decoupling / unity transition (theoretical, no test possible with current simulator)

## 7. Ethics of the work

This research aims to determine whether suppressed physics concepts have real physical
content. That goal is ONLY served by honest results. A simulator that confirms RS theory
by having RS theory baked in helps no one — it produces false confidence that could
mislead others or waste resources on flawed designs.

The standard: would this analysis hold up to hostile peer review?
If not, it's not ready to present as a finding.
