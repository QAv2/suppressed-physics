# Three-Axis Mercury MHD Device — Development Proposal & Proof-of-Concept Plan

**Version**: 1.0
**Date**: 2026-02-22
**Status**: Proposal — seeking collaborators, funding, and lab access
**Technical reference**: See `prototype-spec.md` (676 lines, fully tagged engineering spec)

---

## 1. Executive Summary

This document proposes the development of a bench-scale electromagnetic device: a sealed sphere of liquid mercury with a lead core, driven by three orthogonal AC magnetic coils. The physics is straightforward — Faraday induction, Lorentz force, and Archimedes buoyancy — but the specific configuration (three independent axes addressing all spatial dimensions simultaneously) has never been built or tested. Twenty-one computational experiments, including a full circularity audit, establish the baseline physics and identify what can only be resolved by hardware.

We propose a staged approach beginning with two low-cost tabletop demonstrations: **Phase A** (~$200–700) uses aluminum spheres levitated in air by eddy-current repulsion from three coils, demonstrating 3-axis centering. **Phase B** (~$500–1,200 additional) substitutes a room-temperature liquid metal (galinstan) with a buoyant glass core, directly paralleling the mercury device physics. Both are safe, visual, and use off-the-shelf components.

The full prototype spans five phases from ambient mercury MHD ($8,500–30,000) through cryogenic dynamo search, anomalous effects measurement, and plasma transition, totaling $36,000–153,000 across all phases. A detailed engineering spec, 3D model, and this document constitute the existing work product.

This document covers the device concept, simulation results, tabletop proof-of-concept plans with bills of materials, the full prototype roadmap, and an honest accounting of what is verified physics versus open hypothesis.

---

## 2. The Device Concept

### 2a. Physical Description

```
                        Coil Z (top, +16cm)
                     ╔══════════════════╗
                     ║    ┌────────┐    ║
                     ╚════╡ (bore) ╞════╝
                          │        │
          Coil X          │ sphere │          Coil Y
         (+16cm) ╔═╗  ┌──┼────────┼──┐  ╔═╗ (+16cm)
                 ║ ╠──┤  │ mercury │  ├──╣ ║
                 ║ ║  │  │  ┌──┐  │  │  ║ ║
                 ║ ║  │  │  │Pb│  │  │  ║ ║
                 ║ ║  │  │  └──┘  │  │  ║ ║
                 ║ ╠──┤  │ (core) │  ├──╣ ║
                 ╚═╝  └──┼────────┼──┘  ╚═╝
                          │        │
                     ╔════╡ (bore) ╞════╗
                     ║    └────────┘    ║
                     ╚══════════════════╝

    Three orthogonal flat pancake coils surround a hermetically
    sealed ceramic sphere filled with mercury. Each coil is offset
    16 cm from center along its axis. A lead core floats inside
    at a density-determined equilibrium position.
```

The device consists of three components: a hermetically sealed ceramic or borosilicate glass sphere (10 cm diameter) filled with liquid mercury (~7 kg), a small lead sphere (1.6 cm diameter, ~24 g) floating inside, and orthogonal magnetic coils mounted around the sphere. Two coil configurations are proposed:

#### Coil Configurations

**Configuration A: Nested Helmholtz Pairs (6 coils)**

Three Helmholtz pairs at decreasing radii, each pair at standard Helmholtz spacing (coils at ±R/2). Different radii per axis enables physical nesting without intersection.

```
                     Cross-section (YZ plane, looking down X-axis)

                     ┌─── Z pair (blue, R=22.5cm) ───┐
                     │                                 │
                     │   ┌─── Y pair (green, R=18cm) ──┐
                     │   │                              │
                     │   │   ┌── X pair (red, R=14cm) ─┐
                     │   │   │                          │
                     │   │   │      ╔════════╗         │
                     │   │   │      ║ sphere ║         │
            ─ ─ ─ ─ ○ ─ ○ ─ ○ ─ ─ ║   Pb   ║ ─ ─ ○ ─ ○ ─ ○ ─ ─
                     │   │   │      ║  core  ║         │
                     │   │   │      ╚════════╝         │
                     │   │   │                          │
                     │   │   └──────────────────────────┘
                     │   │                              │
                     │   └──────────────────────────────┘
                     │                                 │
                     └─────────────────────────────────┘

            ○ = wire bundle cross-section (~2cm dia)
            Each pair: two coil rings at ±R/2 along its axis
```

| Axis | Color | Radius | Coil positions | B at center (N=6, I=100A) |
|------|-------|--------|----------------|---------------------------|
| Z (outermost) | Blue | 22.5 cm | z = ±11.25 cm | 2.4 mT |
| Y (middle) | Green | 18 cm | y = ±9 cm | 3.0 mT |
| X (innermost) | Red | 14 cm | x = ±7 cm | 3.9 mT |

Helmholtz field: B = (4/5)^(3/2) × μ₀NI/R ≈ 0.716 × μ₀NI/R. Each pair produces a uniform central field along its axis. Different radii create a natural gradient across axes — the X-axis (smallest, strongest) dominates.

Nesting verification at all crossing points:
- Y wire at Z-coil plane: 16.7 cm from Z-axis (inside 22.5 cm Z-coil) — 5.8 cm clearance
- X wire at Y-coil plane: 12.8 cm from Y-axis (inside 18 cm Y-coil) — 5.2 cm clearance
- X wire at Z-coil plane: 10.9 cm from Z-axis (inside 22.5 cm Z-coil) — 11.6 cm clearance

No intersections. All clearances > 5 cm.

**Configuration B: Single Offset Pancakes (3 coils)**

Three flat annular discs (45 cm diameter, 12 cm bore), each offset 16 cm from center along its axis. Half the hardware, stronger gradients (intentional), simpler 3-channel drive electronics.

#### Configuration Comparison

| Property | A: Helmholtz Pairs | B: Single Pancakes |
|----------|--------------------|--------------------|
| Coil count | 6 (3 pairs) | 3 |
| B at center (per axis) | 2.4–3.9 mT | ~0.9 mT (offset weakens field) |
| Field uniformity | Uniform per axis (Helmholtz condition) | Strong gradient (intentional) |
| Nesting | Natural — different radii | Requires accommodation at crossings |
| Drive channels | 6 (or 3 paired) | 3 |
| Build complexity | Moderate — wire-wound toroids | Lower — flat disc coils |
| Academic recognition | Standard lab geometry | Less familiar |
| Estimated coil cost | ~$200–400 | ~$100–200 |

**Recommendation**: Configuration A (Helmholtz) for any academic or funded build — it uses a geometry that physics departments recognize, produces stronger and more uniform fields, and nests naturally. Configuration B for a minimal first build where simplicity and cost matter most. Either configuration demonstrates the same centering physics.

### 2b. Operating Principle

The physics involves four well-established mechanisms working together:

1. **Archimedes buoyancy**: Lead (11,340 kg/m³) is less dense than mercury (13,534 kg/m³). The lead core floats — it rises until the buoyant force from displaced mercury balances gravity. This determines the starting equilibrium position.

2. **Faraday induction**: Time-varying magnetic fields from the AC coils induce eddy currents in the mercury. The coupling peaks at a characteristic frequency f_d = 1/(2πμ₀σR²), which is 48.7 Hz for a 5 cm mercury sphere — textbook electromagnetics, confirmed by simulation to within 3%.

3. **Lorentz force**: The induced currents interact with the applied magnetic field (J × B), producing forces that drive structured flow in the mercury. With three orthogonal coils, this produces 3D circulation around the core.

4. **Centering gradient**: The magnetic field geometry creates a gradient that, combined with buoyancy, pushes the lead core toward a position below the geometric center. Adding axes improves centering: 3-axis holds the core at ~10.5 mm below center, 2-axis at ~15.7 mm, 1-axis at ~31.6 mm. This hierarchy is purely geometric — it follows from the field gradient topology with no exotic physics required.

### 2c. The Dynamo Path

At room temperature, the electromagnetic forces on the mercury are roughly 1,000× weaker than gravity — measurable with precision instruments, but not dramatic. The device becomes qualitatively different at cryogenic temperatures.

Mercury was the first superconductor ever discovered (Kamerlingh Onnes, 1911, T_c = 4.15 K). Below this temperature, its electrical conductivity increases by roughly six orders of magnitude. The magnetic Reynolds number — the ratio that determines whether a flowing conductor amplifies or dissipates magnetic fields — jumps from 0.03 (ambient) to approximately 3,089.

Above Rm ≈ 10, a flowing conductor enters the dynamo regime: induced currents generate magnetic fields that reinforce the original field, creating a self-sustaining loop. The simulation predicts approximately 864× power amplification at SC conditions — the external coils provide a seed field, and the flowing mercury amplifies it. The coils become control surfaces rather than power inputs. This is the same physics that sustains Earth's geomagnetic field, reproduced at bench scale.

---

## 3. What the Simulation Established

### 3a. Verified Results

Twenty-one experiments across SPH/MHD and PIC (particle-in-cell) simulators established the baseline physics:

- **Centering is density-driven buoyancy** (Archimedes), not exotic. The equilibrium position depends on the density difference between the core and mercury, shaped by the field gradient geometry. Identical results with or without any theoretical overlays.
- **Axis hierarchy (3 > 2 > 1)** follows directly from field geometry — more orthogonal axes means a tighter gradient cage. Quantified: 10.5 mm / 15.7 mm / 31.6 mm below center.
- **Eddy-current coupling peaks at f_d** = 1/(2πμ₀σR²), confirmed analytically and numerically to within 3% of textbook prediction.
- **Dynamo threshold at Rm ≈ 10**: Sharp transition — below threshold, induced fields decay to zero; above, they grow exponentially until back-reaction saturates. SC mercury at 4.2 K reaches Rm ≈ 3,089.
- **3D plasma rotation sustained** (Q_3d ≈ 1.0 under 3-axis drive): Charged particles maintain coherent rotation in all three planes simultaneously, a behavior impossible in viscous liquid.
- **Mercury plasma is 150× worse conductor than liquid mercury**: Spitzer conductivity analysis. Classical dynamo via plasma is not viable.
- **Cyclotron resonance is impossible at bench magnetic fields**: Hg⁺ Larmor radius at max coil field is ~21 m — 420× the sphere radius. Ions cannot complete orbits.

### 3b. What Simulation Could Not Test

The simulator cannot address the questions that motivated building the device:

- **Anomalous weight or inertial effects** — the simulator has no mechanism to produce or detect these
- **Forced Cooper pairing** in lead above T_c — requires real EM pulses at real energies
- **Real dynamo behavior** at SC conditions — the SPH model approximates but cannot reproduce superconducting MHD
- **Plasma vs. liquid mercury** behavior differences under 3-axis drive at realistic parameters
- **Any deviation from standard physics** — the simulator IS standard physics; it can only predict what standard physics predicts

### 3c. The Honesty Audit

A full code audit in February 2026 discovered two instances where theoretical assumptions had been hardcoded into the simulation, then "confirmed" by experiments that could not have produced any other result. Both were disabled, four key experiments were rerun clean, and the results were identical — the biased mechanisms had affected approach speed but not equilibrium physics. Every claim in the engineering spec is now tagged as VERIFIED, MODEL PREDICTION, HYPOTHESIS, or UNTESTED, and the audit is documented.

---

## 4. Tabletop Proof of Concept

These two demonstrations use safe, accessible materials to establish the core operating principle before committing to mercury-scale costs and safety requirements.

### 4a. Phase A: 3-Axis Electromagnetic Centering in Air

**What it demonstrates**: A small conductive sphere held in stable equilibrium at the center of three orthogonal AC magnetic fields. Turn off one axis — the sphere drifts along that axis. Restore it — the sphere re-centers. This is the device's centering mechanism made visible.

**Physics**: Lenz's law eddy-current repulsion. A time-varying magnetic field induces currents in a conductor; those currents generate an opposing field (Lenz's law), producing a repulsive force that pushes the conductor away from the field source. With three coils arranged on orthogonal axes, the repulsive forces create a 3D potential well at the geometric center.

**Key parameters**:

The characteristic coupling frequency for a 2 cm diameter aluminum sphere:

> f_d = 1/(2πμ₀σ_Al R²) = 1/(2π × 1.257×10⁻⁶ × 3.77×10⁷ × 10⁻⁴) ≈ **34 Hz**

This is comfortably in the audio frequency range — standard amplifiers can drive the coils directly.

Skin depth in aluminum at 50 Hz:

> δ = √(2/(ωμ₀σ)) = √(2/(314 × 1.257×10⁻⁶ × 3.77×10⁷)) ≈ **11.6 mm**

Full penetration of a 2 cm sphere — the entire volume participates in eddy-current generation.

A 100-turn coil at 12 cm diameter carrying 5 A produces:

> B = μ₀NI/(2R) ≈ 1.257×10⁻⁶ × 100 × 5 / (2 × 0.06) ≈ **5.2 mT** at center

Coil impedance at 100 Hz is approximately 3–4 Ω (inductive reactance ~3 Ω plus DC resistance ~1 Ω for 22 AWG), compatible with standard 12–24 V audio amplifiers.

**Key demonstrations**:
1. Stable 3-axis centering of aluminum sphere in free air
2. Remove one axis → sphere drifts along unaddressed axis (demonstrates axis hierarchy)
3. Restore axis → sphere re-centers (demonstrates controllability)
4. Frequency sweep → observe coupling peak near 34 Hz
5. Amplitude sweep → map centering force vs. current

**Bill of Materials — Phase A**:

| Component | Specification | Qty | Est. Cost |
|-----------|--------------|-----|-----------|
| Magnet wire | 22 AWG enameled copper, 1 lb spool (~500 ft) | 1 | $16–22 |
| Coil forms | PVC pipe sections or 3D-printed, 12 cm dia | 3 | $15–40 |
| Aluminum spheres | 1–2 cm dia, solid, precision grade | 3–5 | $10–25 |
| Audio amplifiers | Class D, 50–100W per channel | 3 ch | $40–200 |
| Signal generator | 1–200 Hz sine output; 3-channel or 3× single | 1–3 | $25–250 |
| Power supply | 12–24V DC, 10A+ | 1–2 | $20–50 |
| Mounting hardware | Non-magnetic frame (wood/plastic), standoffs, connectors | 1 set | $30–80 |
| Misc | Hookup wire, banana plugs, multimeter for tuning | 1 set | $20–40 |

**Phase A Total: ~$175–710**

*Budget path (~$175–250)*: Single spool of magnet wire, PVC pipe forms, 3× cheap class-D mono amp boards ($15–20 each), phone or laptop as signal generator (free tone generator apps produce sine waves at arbitrary frequencies), basic mounting.

*Full-featured path (~$500–710)*: Proper 3-channel function generator, higher-power amplifiers with current monitoring, precision-machined coil forms, instrumented mounting frame.

**Coil configuration note**: At PoC scale (12–15 cm diameter, 100 turns thin wire), coils at different radii nest naturally as Helmholtz pairs — the same geometry as Configuration A in Section 2a. Either single-coil (Configuration B) or Helmholtz-pair (Configuration A) can be built for Phase A. Helmholtz pairs give better field uniformity at center and are standard lab equipment, making the demonstration more legible to physics audiences. The cost difference is minimal (double the wire, same amplifiers if pairs are wired in series).

**Important note**: Eddy-current levitation in air is well-established physics — this is not novel. What has not been demonstrated is the 3-axis configuration producing the centering hierarchy (3-axis > 2-axis > 1-axis) predicted by the simulation. That hierarchy is the experimentally testable claim.

### 4b. Phase B: Conductive Fluid + Core Centering

**What it demonstrates**: A buoyant core finding its equilibrium position inside a conductive liquid under electromagnetic drive — a direct tabletop analog of lead-in-mercury. Demonstrates that the centering mechanism transfers from air (Phase A) to the fluid regime.

**Why galinstan instead of mercury**: Galinstan (GaInSn eutectic: 68.5% gallium, 21.5% indium, 10% tin) is a room-temperature liquid metal that avoids mercury's toxicity and regulatory burden. It is an excellent stand-in for demonstration purposes:

| Property | Mercury | Galinstan | Comparison |
|----------|---------|-----------|------------|
| Density (kg/m³) | 13,534 | 6,440 | Galinstan lighter |
| Elec. conductivity (S/m) | 1.04 × 10⁶ | 3.46 × 10⁶ | Galinstan 3.3× better |
| Melting point | -39°C | +11°C | Both liquid at room temp |
| Toxicity | High (vapor) | Low (non-toxic) | Major safety advantage |
| Core buoyancy | Pb floats (Δρ = 2,194) | Glass floats (Δρ ≈ 3,940) | Stronger buoyancy in galinstan |
| Wets glass? | No | No (when oxide-free) | Glass containment works for both |
| Cost per 100g | ~$20–50 | ~$250–500 | Galinstan is the main expense |

**Key parameters**:

For a 5 cm diameter galinstan-filled glass vessel:

> f_d = 1/(2πμ₀σ_galinstan R²) = 1/(2π × 1.257×10⁻⁶ × 3.46×10⁶ × 6.25×10⁻⁴) ≈ **59 Hz**

Still in the audio frequency range. Galinstan's higher conductivity compensates for the smaller vessel.

A soda-lime glass marble (ρ ≈ 2,500 kg/m³) or PTFE ball (ρ ≈ 2,200 kg/m³) floats in galinstan (ρ = 6,440 kg/m³) with a density gap of ~3,940–4,240 kg/m³ — even stronger buoyancy than lead in mercury. Both materials are chemically inert with galinstan.

**Key demonstrations**:
1. Core position vs. number of active axes: 1-axis, 2-axis, 3-axis → expect measurable centering hierarchy
2. Frequency sweep → coupling peak near 59 Hz
3. Direct parallel to the mercury device physics, viewable through glass walls

**Containment note**: Galinstan aggressively wets most metals (gallium alloys with aluminum, copper, etc.) but does NOT wet clean glass, quartz, or ceramic. All containment and tooling must be glass, quartz, ceramic, or PTFE. No metal components in contact with galinstan.

**Bill of Materials — Phase B (additional to Phase A rig)**:

| Component | Specification | Qty | Est. Cost |
|-----------|--------------|-----|-----------|
| Galinstan | GaInSn eutectic, 50–200g | 1 lot | $250–1,000 |
| Glass vessel | Borosilicate sphere or cylinder, 3–5 cm inner dia, sealable | 1 | $30–80 |
| Buoyant cores | Glass marbles + PTFE balls, 0.5–1.5 cm dia | 5–10 | $10–20 |
| Glass/ceramic tooling | Pipettes, funnels, storage containers (no metal) | 1 set | $20–40 |
| Sealing supplies | Silicone stoppers, PTFE tape, UV-cure glass adhesive | 1 set | $15–30 |

**Phase B Additional: ~$325–1,170**

**Cumulative (Phase A + B): ~$500–1,880**

*Galinstan is the dominant cost.* A minimal demonstration using 50g ($250) in a 3 cm glass sphere (volume ~14 cm³, requiring ~90g) is the entry point. Larger vessels (5 cm, ~65 cm³, ~420g) provide clearer results but cost proportionally more.

---

## 5. Full Prototype Roadmap

The tabletop PoC demonstrates the principle. The full prototype tests whether the principle produces anything beyond textbook predictions. Five phases, each independently useful:

**Phase 1–2: Mercury MHD + Core Centering** ($8,500–30,000)
Sealed ceramic/glass sphere with liquid mercury and lead core, driven by three orthogonal pancake coils at 0–200 Hz, 10–100 A. Validates mercury flow under 3-axis drive, measures core centering positions against simulation predictions, establishes baseline weight measurements on precision balance. First mercury-specific results. Requires fume hood and mercury handling PPE.

**Phase 3: Cryogenic Dynamo Search** ($13,000–38,000 additional)
Adds cryostat to cool mercury below 4.15 K (superconducting transition). Tests whether the predicted ~864× field amplification occurs — whether the system enters the self-sustaining dynamo regime. The most consequential single experiment: if it works, the coils become control surfaces and the device generates its own operating field. This is the same dynamo physics that sustains Earth's magnetic field.

**Phase 4: Anomalous Effects Search** ($8,200–60,500 additional)
Systematic measurement campaign: upgraded precision balance (±0.1 mg), 3-axis accelerometer, spectrum analyzer, and if accessible, a relative gravimeter (±1 μGal). Looking for any measurable deviation from standard physics — weight anomaly, inertial anomaly, unexpected EM emissions. The expected result is null. A positive result would be significant.

**Phase 5: Plasma Transition** ($6,200–24,000 additional)
High-voltage pulse (Marx generator or capacitor bank, 150 kV–1 MV) ionizes mercury to plasma state in argon pre-fill atmosphere. Tests whether plasma mercury responds differently to 3-axis drive than liquid mercury — the simulator predicts distinct coupling mechanisms. Requires two-person operation and HV safety protocols.

**Cumulative Cost Summary**:

| Configuration | Estimate |
|---------------|----------|
| PoC only (Phase A + B) | $500–1,900 |
| Phase 1–2 (ambient liquid MHD) | $8,500–30,000 |
| + Phase 3 (cryogenic dynamo) | $21,500–68,000 |
| + Phase 4 (anomalous effects) | $29,700–128,500 |
| + Phase 5 (plasma transition) | $35,900–152,500 |

Phases 3 and 5 are independent — either can be built first. Phase 4 benefits from both but can begin with Phase 1–2 data alone.

---

## 6. Verified Physics vs. Open Hypotheses

This is the honest accounting. Every claim falls into one of two columns.

| What We Know (Verified / Textbook) | What We Hypothesize (Untested) |
|---|---|
| Eddy-current levitation via Lenz's law — demonstrated since 1920s | Dynamo amplification at the predicted ~864× level |
| Mercury properties: ρ = 13,534 kg/m³, σ = 1.04×10⁶ S/m, T_c = 4.15 K (CRC Handbook, Onnes 1911) | Any anomalous weight or inertia effect |
| Lead floats in mercury (Δρ = 2,194 kg/m³) | Forced Cooper pairing in Pb above T_c |
| Dynamo effect: demonstrated in Riga (2000), Karlsruhe (2000), and VKS (2007) liquid-metal experiments | Plasma vs. liquid mercury producing qualitatively different effects |
| SC mercury since 1911 — oldest known superconductor | Non-standard frequency or amplitude sensitivities |
| Eddy-current coupling peaks at f_d = 1/(2πμ₀σR²) — textbook EM | Consciousness-EM coupling (theoretical, far-future) |
| 3-axis field geometry produces tighter centering than 2- or 1-axis — confirmed by simulation and field geometry analysis | Reference frame decoupling or modification of local spacetime metric |
| Mercury plasma is 150× worse conductor than liquid — Spitzer/Saha | Any effect that cannot be explained by classical EM + gravity + buoyancy |

**What we are NOT claiming**: This project does not claim anti-gravity, propulsion, or any validated exotic physics. The device is designed to systematically test whether such effects exist under these specific conditions. A null result — standard physics only, no anomalies — is a valid and publishable outcome.

---

## 7. Historical & Theoretical Context

Six independent research lines spanning 65+ years converge on a common architecture: intense electromagnetic energy applied to a conductive medium in a configuration addressing multiple spatial dimensions. The convergence is either coincidence or evidence that the underlying principle is real and repeatedly rediscovered.

- **Podkletnov (1992)**: Rotating superconducting disc (YBCO) under AC magnetic field. Reported 0.3–2.1% weight reduction above the disc. Published in Physica C (peer-reviewed). Replication by Hathaway (1999) found no effect — suggesting extreme parameter sensitivity or error. Single-axis configuration.

- **Clemens Patent (2023)**: Counter-rotating mercury plasmas with thorium dioxide dopant, activated by high-voltage pulse (>1 MV). Claims gravity/inertia nullification. Specifies argon pre-fill, boron carbide neutron shielding. Two-axis (counter-rotating) configuration.

- **Pais Patents (2016–2018)**: Filed by the US Navy. High-frequency rotation of charged media in conical geometry. Claims "inertial mass reduction." Accompanied by Navy chief technology officer attestation of operational significance.

- **DIRDs (2007–2012)**: 38 Defense Intelligence Reference Documents produced under the Pentagon's AAWSAP/AATIP program. Topics include vacuum metric engineering (Puthoff), warp drive feasibility, and advanced propulsion concepts. One remains classified.

- **Die Glocke (1944–45)**: Alleged Nazi program involving counter-rotating cylinders of mercury-thorium compound ("Xerum 525") under high-voltage fields. Historical provenance disputed but the described architecture matches the convergence pattern.

- **Vimana texts (ancient)**: Sanskrit texts describing mercury vortex propulsion in sealed chambers with electromagnetic activation. Cultural context makes technical interpretation uncertain, but the described elements align with the pattern.

**This convergence motivates the work but does not validate it.** The prototype is designed to test, not to assume. Historical claims and patents provide design parameters worth exploring, not conclusions to accept. If every measurement returns a null result consistent with standard physics, that outcome is published honestly. The purpose of the prototype is to generate data, not to confirm a narrative.

---

## 8. Next Steps & Collaboration

### Timeline

- **Phase A (3-axis air centering)**: 1–2 weeks build, under $700. Can begin immediately.
- **Phase B (conductive fluid + core)**: 2–4 weeks after Phase A, under $1,200 additional. Requires galinstan procurement.
- **Phase 1–2 (mercury prototype)**: 2–3 months, $8,500–30,000. Requires lab with fume hood.
- **Phase 3+ (cryogenic / anomalous / plasma)**: Incremental from established Phase 1–2 baseline.

### What Already Exists

- 21 simulation experiments (SPH/MHD + PIC), fully audited for circularity
- 676-line engineering specification with every claim tagged by rigor level
- 3D model of the 3-coil geometry (Blender)
- This development proposal
- Documented ground rules enforcing intellectual honesty (CLAUDE.md)

### What's Needed

- **Phase A–B**: Minimal — one person, a workbench, off-the-shelf components, and 3–6 weeks
- **Phase 1–2**: Funding ($8.5–30K), lab access (fume hood rated for mercury vapor), one engineer familiar with EM coil design or MHD
- **Phase 3+**: Cryogenics expertise, high-voltage engineering, institutional support (university lab or equivalent)

### What makes this worth pursuing

The configuration is specific, the physics is testable, and the cost of finding out is modest. Phase A–B costs less than a weekend hobby project and demonstrates real, visible electromagnetic centering. Phase 1–2 costs less than a used car and produces the first mercury data under 3-axis drive — a configuration that has never been experimentally characterized. Even if every result matches standard physics predictions exactly, that data has value: it retires the hypothesis cleanly rather than leaving it untested.

The alternative to building it is continuing to speculate about it. The tabletop PoC is the cheapest available path from speculation to data.

---

## Appendix: Reference Documents

| Document | Contents |
|----------|----------|
| `prototype-spec.md` | Full engineering specification — geometry, materials, BOM, protocols, rigor tags |
| `device-vision.md` | Architecture overview, initialization sequence, operating principle |
| `parameter-space.md` | Engineering parameters, dynamo threshold data |
| `configurations.md` | 3-axis vs counter-rotation analysis |
| `convergence-analysis.md` | Six-line convergence argument with cross-framework table |
| `CLAUDE.md` | Ground rules — rigor hierarchy, anti-circularity rules, known limitations |

All source documents available on request.
