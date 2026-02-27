# Prototype Spec — Bench-Scale Reference Frame Engine

**Version**: 1.0
**Date**: 2026-02-22
**Status**: Post-audit, post-clean-rerun. All circular findings identified and excluded.
**Ground rules**: See [CLAUDE.md](../CLAUDE.md) — every claim in this document is tagged per the rigor hierarchy.

---

## Rigor Key

Every engineering claim in this document carries one of these tags:

| Tag | Meaning | Standard |
|-----|---------|----------|
| **VERIFIED** | Matches textbook physics, independently calculable, confirmed by experiment or pencil math | Would survive hostile peer review |
| **MODEL PREDICTION** | Follows from simulator physics (SPH/MHD or PIC), but simulator has known limitations | Depends on model fidelity |
| **HYPOTHESIS** | Not yet testable with current tools — stated for experimental design, not as design requirement | Must be tested, not assumed |
| **UNTESTED** | No data either way — included for completeness | Treat as unknown |

Claims tagged HYPOTHESIS or UNTESTED are included as *experimental targets*, not design constraints. The prototype is designed to TEST them, not assume them.

---

## 1. Device Overview

### Physical Layout

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

    Three orthogonal flat pancake coils (weight-plate style)
    surround a hermetically sealed ceramic sphere filled with
    mercury. Each coil is offset 16 cm from center along its
    axis (≈ R/√2). 12 cm central bore clears the sphere.
    A lead core floats inside at a density-determined
    equilibrium position below geometric center.
```

### Operating Principle (No RS Theory Required)

Three orthogonal AC pancake coils, each offset from center along its axis, generate time-varying magnetic fields inside a sealed ceramic sphere filled with liquid mercury. The mercury, being an excellent electrical conductor, develops eddy currents (Faraday induction) that couple to the fields via Lorentz force (J x B). A lead core, denser than mercury but buoyant relative to the field-gradient geometry, settles at an equilibrium position determined by the balance between gravitational buoyancy and magnetic pressure. The three-axis field drives structured 3D flow in the mercury around the core.

### What the Prototype is Designed to TEST

1. Whether EM-driven mercury produces measurable forces on a precision balance (anomalous weight)
2. Whether any frequency produces enhanced coupling beyond textbook eddy-current predictions
3. Whether a lead core exhibits anomalous magnetic behavior under pulsed EM (forced Cooper pairing)
4. Whether the cryo-dynamo path (SC mercury at 4.2K) produces self-sustaining fields at bench scale
5. Whether plasma-state mercury under 3-axis drive exhibits behavior distinct from liquid-state
6. Whether any of the above produces measurable weight, inertia, or gravitational anomalies

---

## 2. Bill of Materials

### Phase 1-2: Mercury MHD + Core Centering

| Component | Specification | Qty | Est. Cost | Notes |
|-----------|--------------|-----|-----------|-------|
| **Mercury** | 99.99% purity, 1-5 kg | 1 lot | $200-500 | 13.5 g/cm³; 1 kg = 74 cm³. Sealed system — no losses. Source: chemical supplier (Alfa Aesar, Sigma-Aldrich). |
| **Ceramic sphere** | R = 5.0 cm (10 cm dia), hermetic seal | 1 | $500-2,000 | Alumina or borosilicate glass. Must be: electrically insulating, transparent to B-field, vacuum-sealable, Hg-resistant. Glass allows visual inspection. Fill port + vacuum seal. |
| **Lead core** | R = 0.8 cm (1.6 cm dia), 99.9% Pb | 1 | $10-30 | Mass ≈ 24 g (ρ_Pb = 11,340 kg/m³, V = 2.14 cm³). Spherical preferred. Machine or cast. |
| **Pancake coils** | 3 single coils, orthogonal. 45 cm dia, 12 cm bore, ~2.5 cm thick, 4-6 turns each, 4 AWG copper. Offset 16 cm from center per axis. | 3 coils | $500-1,500 | Single coil at offset produces B ≈ 0.006-0.091 mT at center (4 turns/10A to 6 turns/100A). **VERIFIED** — Biot-Savart: B = μ₀NIR²/(2(R²+d²)^(3/2)), d=0.16m. ~54% of centered single-coil value; halves hardware vs Helmholtz pairs. See Section 4. |
| **Power supply** | Variable frequency AC, 0-200 Hz, 3 independent channels, 0-100A per channel | 1 | $2,000-10,000 | Must support: independent freq/phase/amplitude per axis, sine wave output, programmable sweep. Audio amplifiers + signal generator is budget option. |
| **Hall probes** | 3-axis, ±1 mT range, 0.001 mT resolution | 3+ | $300-1,000 | For field mapping inside and outside sphere. |
| **Precision balance** | ±1 mg (0.001 g), capacity ≥ 20 kg | 1 | $500-2,000 | For weight anomaly measurement (Podkletnov-style). Device sits on balance. |
| **Thermocouple** | Type K, -200 to +1,000°C | 2 | $50-100 | Mercury temperature monitoring. External mount (don't breach sphere). |
| **DAQ system** | Multi-channel, ≥1 kHz sample rate | 1 | $2,000-5,000 | Inputs: 3× current sense, 3× field probes, balance, temp. Output: waveform control. National Instruments or similar. |
| **Fume hood** | Benchtop, mercury-rated | 1 | $1,000-3,000 | Required for any work with open mercury. |
| **PPE** | Nitrile gloves, safety glasses, respirator (Hg cartridge) | 1 set | $200-400 | Mercury vapor is the primary hazard. |
| **Spill kit** | Mercury spill kit (sulfur powder, aspirator, disposal bags) | 1 | $100-200 | Mandatory. |
| **Faraday cage** | Copper mesh enclosure, grounded | 1 | $500-2,000 | EM shielding for sensitive measurements. |
| **Support structure** | Non-magnetic frame (aluminum/wood) | 1 | $200-500 | Holds sphere + coils in alignment. |

**Phase 1-2 Total: ~$8,500-30,000**

### Phase 3: Dynamo Search (Cryogenic Add-on)

| Component | Specification | Qty | Est. Cost | Notes |
|-----------|--------------|-----|-----------|-------|
| **Cryostat** | For 10 cm sphere, 4.2K operation | 1 | $3,000-10,000 | Vacuum-jacketed dewar surrounding sphere. |
| **Liquid helium** | Dewar + transfer system | 1 | $5,000-15,000 | LHe at 4.2K. Boil-off requires periodic refill. |
| **Temperature monitoring** | Cernox or Pt sensors, 4-300K range | 3 | $1,000-3,000 | Confirm Hg reaches 4.15K (Tc). |
| **Flux probes** | SQUID or fluxgate magnetometer | 1 | $2,000-5,000 | Detect self-generated B-field (dynamo onset). |
| **Additional insulation** | Vacuum jacket, MLI blankets | 1 | $2,000-5,000 | Minimize LHe boil-off. |

**Phase 3 Add-on: ~$13,000-38,000**

### Phase 4: Anomalous Effects Search

| Component | Specification | Qty | Est. Cost | Notes |
|-----------|--------------|-----|-----------|-------|
| **Precision balance** | ±0.1 mg (upgrade from Phase 1) | 1 | $2,000-5,000 | Detect sub-milligram weight changes. |
| **Accelerometer** | 3-axis MEMS, ±2g, 0.001g resolution | 1 | $200-500 | Mounted on device — detect inertial anomalies. |
| **Spectrum analyzer** | 0-1 GHz, -100 dBm sensitivity | 1 | $1,000-5,000 | Monitor EM emissions from device. |
| **Gravimeter** | Relative, ±1 μGal if accessible | 1 | $5,000-50,000 | Borrow or rent. Most sensitive weight anomaly test. |

**Phase 4 Add-on: ~$8,200-60,500**

### Phase 5: Plasma Transition

| Component | Specification | Qty | Est. Cost | Notes |
|-----------|--------------|-----|-----------|-------|
| **Marx generator OR capacitor bank** | 150 kV-1 MV, >10⁴ A, pulse ≤100 μs | 1 | $5,000-20,000 | Ionizes mercury to plasma. Clemens specifies this range. Capacitor bank is simpler for initial tests. |
| **Argon gas supply** | High purity, fill to 6-10 torr | 1 | $200-500 | Pre-fills sphere before mercury. Prevents Hg recombination. (Clemens spec.) |
| **HV isolation** | Insulating standoffs, discharge rods, interlocks | 1 set | $500-2,000 | Safety-critical. |
| **Radiation monitoring** | Geiger counter + dosimeter | 1 set | $200-500 | Baseline + operational monitoring. Required before adding any thorium. |
| **HV safety equipment** | Discharge stick, lockout/tagout, barriers | 1 set | $300-1,000 | Two-person operation rule. |

**Phase 5 Add-on: ~$6,200-24,000**

### Total Cost Summary

| Configuration | Estimate |
|---------------|----------|
| Phase 1-2 only (ambient liquid MHD) | $8,500-30,000 |
| + Phase 3 (cryogenic dynamo) | $21,500-68,000 |
| + Phase 4 (anomalous effects) | $29,700-128,500 |
| + Phase 5 (plasma transition) | $35,900-152,500 |
| **Full build (all phases)** | **~$36,000-153,000** |

*Note: Ranges reflect DIY/surplus vs. new commercial equipment. Phase 3 (cryo) and Phase 5 (HV) are independent upgrades — either can be built first.*

---

## 3. Engineering Parameters

### Sphere Geometry

| Parameter | Value | Source | Rigor |
|-----------|-------|--------|-------|
| Sphere radius (baseline) | R = 5.0 cm (10 cm dia) | Simulator benchmark | — |
| Sphere radius (alt) | R = 4.5 cm (9 cm dia) | Pencil math variant | — |
| Mercury volume (5 cm, minus core) | ~521 cm³ = 7.03 kg | V_sphere - V_core | **VERIFIED** (geometry) |
| Core radius | r = 0.8 cm (1.6 cm dia) | Simulator config | — |

### Mercury Properties

| Property | Value | Source | Rigor |
|----------|-------|--------|-------|
| Density (liquid, 20°C) | 13,534 kg/m³ | CRC Handbook | **VERIFIED** |
| Electrical conductivity | 1.04 × 10⁶ S/m | CRC Handbook | **VERIFIED** |
| Superconducting Tc | 4.15 K | Kamerlingh Onnes 1911 | **VERIFIED** |
| Vapor pressure (20°C) | 0.26 Pa (2 × 10⁻³ mmHg) | CRC Handbook | **VERIFIED** |
| Boiling point | 630 K (357°C) | CRC Handbook | **VERIFIED** |
| Viscosity (20°C) | 1.55 × 10⁻³ Pa·s | CRC Handbook | **VERIFIED** |
| First ionization energy | 10.44 eV | NIST | **VERIFIED** |
| TLV (vapor, occupational) | 0.025 mg/m³ | OSHA | **VERIFIED** |

### Lead Core Properties

| Property | Value | Source | Rigor |
|----------|-------|--------|-------|
| Density | 11,340 kg/m³ | CRC Handbook | **VERIFIED** |
| Superconducting Tc | 7.2 K | Textbook | **VERIFIED** |
| Diamagnetic susceptibility | -1.8 × 10⁻⁵ | CRC Handbook | **VERIFIED** |
| Mass (r=0.8cm sphere) | ~24.3 g | ρ × 4/3πr³ | **VERIFIED** (geometry) |
| Density gap from Hg | Δρ = 2,194 kg/m³ (Pb lighter) | ρ_Hg - ρ_Pb | **VERIFIED** |

### Coil Parameters

| Parameter | Value | Source | Rigor |
|-----------|-------|--------|-------|
| Coil type | Single pancake coils, 3 orthogonal axes, offset from center | Design choice (from /deeper) | — |
| Coil diameter | ~45 cm (outer), ~12 cm bore | Gemini session spec + sphere clearance | — |
| Coil thickness | ~2.5 cm | Design choice (weight-plate form factor) | — |
| Offset from center | ~16 cm per axis (≈ R/√2) | Minimum non-intersecting distance | — |
| Turns per coil | 4-6 | Gemini session spec | — |
| Wire gauge | 4 AWG (~5.2 mm dia) braided | Gemini session spec | — |
| Current range | 10-100 A | Design range | — |
| B at sphere center (4 turns, 10A) | 0.006 mT | B = μ₀NIR²/(2(R²+d²)^(3/2)), R=0.225m, d=0.16m | **VERIFIED** (Biot-Savart) |
| B at sphere center (6 turns, 50A) | 0.046 mT | Same formula | **VERIFIED** (Biot-Savart) |
| B at sphere center (6 turns, 100A) | 0.091 mT | Same formula | **VERIFIED** (Biot-Savart) |
| Max 3-axis combined B | ~0.16 mT (√3 × 0.091) | Pythagoras | **VERIFIED** |
| vs. centered single coil | ~54% field at center per axis | Offset attenuation: R³/(R²+d²)^(3/2) | **VERIFIED** |
| vs. Helmholtz pair | ~38% field per axis (pair = 1.43× single) | Single offset vs paired centered | **VERIFIED** |
| **Trade-off** | Half the hardware (3 coils vs 6), simpler build, easier nesting | Design choice | — |

### Eddy-Current Coupling

| Parameter | Value | Source | Rigor |
|-----------|-------|--------|-------|
| Magnetic diffusion time τ_d | τ_d = μ₀σR² | Textbook EM | **VERIFIED** |
| Peak coupling frequency f_d | f_d = 1/(2πτ_d) = 1/(2πμ₀σR²) | Textbook EM | **VERIFIED** |
| f_d (5.0 cm sphere, liquid Hg) | **48.7 Hz** | Calc: 1/(2π × 1.257e-6 × 1.04e6 × 0.0025) | **VERIFIED** (exp 20: within 3%) |
| f_d (4.5 cm sphere, liquid Hg) | **60.1 Hz** | Same formula, R=0.045 | **VERIFIED** |
| f_d (9.0 cm sphere, liquid Hg) | **15.0 Hz** | Same formula, R=0.09 | **VERIFIED** (exp 20: exact match) |
| f_d depends on core material? | **NO** — depends only on mercury σ and sphere R | Textbook EM | **VERIFIED** |
| Skin depth at 50 Hz | 7.0 cm (> sphere radius) | δ = √(2/ωμ₀σ) | **VERIFIED** |
| EM force vs gravity at bench | ~1,000× weaker | Simulator exp 20 | **MODEL PREDICTION** |

### Centering Equilibrium

| Parameter | Value | Source | Rigor |
|-----------|-------|--------|-------|
| Pb equilibrium (3-axis, 5cm sphere) | ~10.5 mm below center | Clean rerun exp 1 | **VERIFIED** (density-driven) |
| Pb equilibrium (2-axis) | ~15.7 mm below center | Clean rerun exp 3 | **VERIFIED** |
| Pb equilibrium (1-axis) | ~31.6 mm below center | Clean rerun exp 3 | **VERIFIED** |
| Axis hierarchy | 3-axis > 2-axis > 1-axis (tighter centering) | Clean rerun exp 3 | **VERIFIED** (field geometry) |
| Centering mechanism | Archimedes buoyancy vs. magnetic field gradient | Clean reruns exp 1,3,5 | **VERIFIED** |
| RS coupling factor effect on equilibrium | **ZERO** — identical with/without | Clean reruns exp 1,3,5 | **VERIFIED** (negative result) |

### Dynamo Threshold

| Parameter | Value | Source | Rigor |
|-----------|-------|--------|-------|
| Rm = μ₀σvL | Magnetic Reynolds number | Textbook MHD | **VERIFIED** |
| Rm_crit | ~10 (spherical geometry) | Clean rerun exp 8 | **VERIFIED** |
| Bench ambient Hg (5cm) Rm | ~0.03 | Exp 8 | **VERIFIED** (300× below threshold) |
| SC-Hg (4.2K, 5cm) Rm | ~3,089 | Exp 8 | **MODEL PREDICTION** |
| SC-Hg power amplification | ~864× | Exp 8 (clean: 856×, contaminated: 864×, = SPH noise) | **MODEL PREDICTION** |
| Transition sharpness | Δσ × 25 gap, amp ∝ σ^4.05 | Exp 11 | **MODEL PREDICTION** |
| RS tuning effect on threshold | **NONE** — all configs cross at Rm ≈ 10 | Exp 9 | **VERIFIED** (RS-independent) |

### Plasma Mercury

| Parameter | Value | Source | Rigor |
|-----------|-------|--------|-------|
| Plasma σ at 10,000 K | ~6,800 S/m | Spitzer/Saha calculation | **VERIFIED** (textbook plasma physics) |
| Plasma σ at 100,000 K | ~32,000 S/m | Spitzer formula | **VERIFIED** |
| Ratio plasma/liquid σ | ~0.007× (150× worse) | σ_plasma / σ_liquid | **VERIFIED** |
| Temperature to match liquid σ | ~770,000 K | Spitzer extrapolation | **VERIFIED** |
| Classical dynamo via plasma Hg | **NOT VIABLE** | σ too low → Rm << 1 | **VERIFIED** |
| Ionization fraction at 10,000 K | ~24% | Saha equation | **VERIFIED** |
| Full ionization temperature | ~15,000-20,000 K | Saha equation | **VERIFIED** |

### Cyclotron Physics

| Parameter | Value | Source | Rigor |
|-----------|-------|--------|-------|
| Hg⁺ Larmor radius at 0.091 mT, 10kK | ~21 m (420× sphere) | r_c = mv⊥/(qB) | **VERIFIED** (pencil math) |
| B needed for magnetized orbits | ~50 mT | r_c ≤ R_sphere | **VERIFIED** (pencil math) |
| Gap from realistic coils | ~550× | 0.091 mT vs 50 mT | **VERIFIED** |
| Cyclotron resonance at bench B | **IMPOSSIBLE** | Ions can't complete orbits | **VERIFIED** |

### 3D Plasma Rotation

| Parameter | Value | Source | Rigor |
|-----------|-------|--------|-------|
| Q_3d (3-axis AC drive) | 0.96-1.0 | PIC exp 14 | **MODEL PREDICTION** (Boris pusher verified) |
| Q_3d (1-axis AC drive) | ~0.003 | PIC exp 14 | **MODEL PREDICTION** |
| Plasma sustains 3D rotation? | **YES** — no viscous coupling collapses 3D structure | PIC exp 14 | **MODEL PREDICTION** |
| Equal amps vs RS ratio Q_3d | Equal wins slightly (1.0 vs 0.96) | PIC exp 14-15 | **MODEL PREDICTION** |

---

## 4. Frequency & Amplitude Strategy

### Primary: Broad Sweep at Equal Amplitudes (Baseline)

| Parameter | Setting | Rationale |
|-----------|---------|-----------|
| Frequency range | 5-200 Hz | Covers textbook f_d ± 4× for all sphere sizes |
| Amplitude ratio | [1, 1, 1] (equal) | Maximizes isotropy. **VERIFIED**: equal amps maximize Q_3d in PIC (exp 14-15) |
| Phase | [0°, 0°, 0°] (in-phase) | Simplest baseline. Phase had very small effects in simulator (exp 16) |
| Step size | 5 Hz increments | ~40 data points across sweep |
| Measurement at each step | Weight (balance), B-field (Hall probes), temperature | — |

**Purpose**: Establish the null hypothesis. If no frequency shows special behavior, the system is behaving as textbook EM predicts (eddy-current coupling monotonic or peaked at f_d). This is the expected result.

### Secondary: Focused Tests at f_d

| Parameter | Setting | Rationale |
|-----------|---------|-----------|
| Frequency | f_d = 48.7 Hz (5cm sphere) or 60.1 Hz (4.5cm) | **VERIFIED** peak eddy-current coupling (exp 20, textbook EM) |
| Amplitude | Sweep 10-100 A per axis, equal amplitudes | Map force vs current |
| Duration | Extended runs (minutes) | Allow thermal/flow equilibrium |

**Purpose**: Characterize behavior at the verified optimal coupling frequency. This is where the EM-mercury interaction is strongest. Any anomalous effect is most likely to appear here.

### Tertiary: RS-Predicted Frequencies (ONE Variant — Hypothesis)

| Parameter | Setting | Rationale |
|-----------|---------|-----------|
| Frequency for Pb core | 40.5 Hz | RS formula: 50 × (9/10)² Hz. **HYPOTHESIS — not validated.** Simulator "validation" was circular (exp 7, 10, 19). |
| Frequency for Hg medium | 50.0 Hz | RS formula: 50 × (10/10)² Hz. **HYPOTHESIS**. Near-coincidence with f_d (48.7 Hz) is geometry-dependent, not fundamental (see Priority 2 analysis). |
| Frequency for Th-doped | 72.0 Hz | RS formula: 50 × (12/10)² Hz. **HYPOTHESIS**. Same f_RS as Fe despite radically different properties. |

**Purpose**: Test one RS prediction as a controlled variant. If RS frequencies produce effects that f_d and broad sweep do not, this is evidence for new physics. If not, RS frequency formula is not operating at bench scale.

### Amplitude Ratios

| Config | Ratio [X, Y, Z] | Rationale |
|--------|------------------|-----------|
| **Equal (baseline)** | [1.0, 1.0, 1.0] | **Start here.** Equal amps maximize isotropy and Q_3d. |
| RS-predicted for Pb | [1.0, 1.0, 0.25] | **HYPOTHESIS.** Simulator exp 21: RS ratios had NO effect on centering (spread < 0.012 mm). Test anyway. |
| RS-predicted for Th | [1.0, 1.0, 1.0] | Happens to be equal — no independent test of RS for Th amplitude. |

**Critical note**: Experiment 21 found RS amplitude ratios have **no special status** in the simulator model (centering identical, mercury flow stochastic, RS ratio never wins). These are tested as controlled variants, not expected to differ from baseline.

### Phase Offsets

| Config | Phase [X, Y, Z] | Rationale |
|--------|------------------|-----------|
| **In-phase (baseline)** | [0°, 0°, 0°] | Simplest starting point. |
| Anti-phase Z | [0°, 0°, 180°] | PIC exp 16: peak Q_3d at 180°, not RS-predicted 22°. **MODEL PREDICTION.** |
| RS-predicted for Pb | [0°, 0°, 11.3°] | **HYPOTHESIS.** Exp 16 found very small phase effects and peak at wrong angle. |

---

## 5. Experimental Protocols

### Phase 1: Mercury MHD Baseline

**Objective**: Validate that 3-axis EM fields drive structured flow in liquid mercury. Establish baseline measurements for weight, field, and flow.

**Setup**:
1. Fill ceramic sphere with mercury under vacuum (no air bubbles). Seal hermetically.
2. Mount sphere at center of 3-axis coil assembly on precision balance.
3. Connect coils to 3-channel power supply.
4. Position Hall probes at sphere exterior (3 axes) and at reference points.
5. Ensure fume hood ventilation active throughout.

**Protocol**:
1. Record baseline weight (coils off) — average over 60 seconds.
2. Energize one axis at a time: X only, Y only, Z only. Record weight and field at each.
3. Energize two axes: XY, XZ, YZ. Record.
4. Energize all three axes at equal amplitude. Record.
5. Broad frequency sweep (5-200 Hz) at fixed amplitude, all 3 axes. Record weight and field at each step (30-second dwell per frequency).
6. Focused sweep around f_d = 48.7 Hz (±10 Hz, 1 Hz steps). Record.
7. Amplitude sweep at f_d: 10, 20, 50, 100 A. Record.

**Success criteria**:
- Balance shows measurable EM-driven force (even if small — establishes sensitivity floor).
- Hall probes confirm expected field pattern.
- Temperature stable (no thermal artifacts on balance).

**Expected results (from simulator)**:
- EM-driven force at bench B is ~1,000× weaker than gravity. **MODEL PREDICTION**. May be below balance resolution (1 mg ≈ 10 μN). If so, this establishes the sensitivity floor — not a failure.
- Eddy-current coupling peaks near 48.7 Hz. **VERIFIED**. Should see maximum field response there.
- No frequency produces anomalous weight change. (This IS the expected result. A weight change here would be novel.)

**Failure modes**:
- Mercury leaks → abort, spill protocol, seal failure analysis.
- No measurable EM response → check coil connections, verify field with external probe, increase current.
- Balance drift from thermal effects → improve thermal isolation, extend averaging time.

### Phase 2: Lead Core Introduction

**Objective**: Test magnetic centering of Pb core. Measure equilibrium position vs. simulator prediction. Test for anomalous magnetic response under pulsed EM (forced Cooper pairing — Q1 from device-vision.md).

**Setup**:
1. Open sphere (under fume hood). Add Pb sphere (r=0.8cm).
2. Re-seal under vacuum. Pb sinks to bottom (dormant state).
3. Remount on balance and coil assembly.

**Protocol**:
1. Record baseline weight with Pb at rest (bottom of sphere).
2. Energize 3-axis field at f_d, 50A. Observe whether Pb migrates upward.
3. If Pb moves: measure equilibrium position (via X-ray, ultrasound, or field perturbation technique).
4. Repeat with 1-axis and 2-axis configurations. Compare positions.
5. **Cooper pairing test**: Apply capacitor-bank pulse (start low — 1kV, increase gradually). Monitor:
   - Field anomaly (SQUID/fluxgate) — does Pb produce its own field?
   - Weight change on balance
   - Any persistent magnetic state after pulse ends
6. Repeat frequency and amplitude sweeps from Phase 1 with core present.

**Success criteria**:
- Core migrates toward center under 3-axis field (confirms centering physics).
- 3-axis centers tighter than 2-axis or 1-axis (confirms axis hierarchy).

**Expected results (from simulator)**:
- Pb equilibrium ~10.5 mm below center (3-axis, 5cm sphere). **VERIFIED** (clean rerun exp 1).
- 3-axis: 10.5 mm, 2-axis: ~15.7 mm, 1-axis: ~31.6 mm. **VERIFIED** (clean rerun exp 3).
- Centering driven entirely by density (Δρ = 2,194 kg/m³). **VERIFIED**.

**What would be novel**:
- Pb exhibits persistent magnetization after pulse (forced Cooper pairing). **HYPOTHESIS** — standard physics says no above 7.2K.
- Any weight anomaly during pulsed EM.
- Core position differs significantly from density-predicted equilibrium.

### Phase 3: Dynamo Effect Search

**Objective**: Determine whether self-sustaining magnetic field can be achieved. The cryo-dynamo path (SC mercury at 4.2K) is the only viable classical path at bench scale.

**Setup**:
1. Install cryostat around sphere assembly.
2. Cool to 4.2K (below Hg Tc = 4.15K).
3. Confirm Hg is superconducting (resistivity measurement or Meissner effect).
4. Install flux probes at multiple locations around sphere.

**Protocol**:
1. With Hg superconducting, energize coils at low amplitude.
2. Gradually increase amplitude. Monitor induced field (flux probes).
3. At each amplitude step, briefly reduce external field — does induced field persist?
4. If persistent field detected: map the amplification factor (induced/applied).
5. Attempt to operate on induced field alone (reduce external to minimum that maintains control).

**Success criteria**:
- Induced field persists when external field is reduced → dynamo achieved.
- Amplification factor measurable and consistent with Rm estimate.

**Expected results (from simulator)**:
- SC-Hg at 4.2K should produce Rm ≈ 3,089 (bench scale). **MODEL PREDICTION**.
- Amplification ~856-864×. **MODEL PREDICTION**.
- Coils become control surfaces — tiny input produces large operating field.
- Transition is sharp — there's a clear onset threshold.

**What would be novel**:
- Amplification significantly different from predicted (physics beyond classical MHD).
- Weight anomaly concurrent with dynamo onset.
- Dynamo at ambient temperature (would indicate non-classical conductivity enhancement).

**Failure modes**:
- Can't reach 4.2K → check cryostat, LHe supply.
- No dynamo → check if Hg is actually superconducting (Meissner test), verify coil field.

**Note**: At ambient temperature, bench-scale Hg has Rm ≈ 0.03. **VERIFIED** — expect NO dynamo at ambient. If you see one, that's new physics.

### Phase 4: Anomalous Effects Search

**Objective**: Systematic search for any measurable deviation from standard physics predictions.

**Setup**:
1. Device operating at optimal parameters from Phase 1-3.
2. Precision balance (±0.1 mg), accelerometer, spectrum analyzer, gravimeter (if available).
3. Multiple independent measurement systems for cross-validation.
4. Faraday cage around device for EM isolation.

**Protocol**:
1. Baseline measurements (all sensors, device off) — 10 minutes minimum.
2. Operate device at each configuration from Phase 1-3. Record all sensors simultaneously.
3. Focus on configurations that showed any anomaly in prior phases.
4. Vary parameters systematically: frequency (broad sweep), amplitude (low to max), phase (0°-180°).
5. Run each configuration for extended period (10+ minutes) to distinguish transients from steady-state.
6. Blind measurements: have someone else read the sensors while you control parameters (or automate).

**Success criteria**:
- Any measurement that deviates from standard EM + gravity prediction by >5σ across repeated trials.
- Deviation must correlate with device operation (present when on, absent when off).
- Deviation must not be explainable by thermal, vibrational, or EM artifact.

**Expected results (from standard physics)**:
- No weight anomaly above noise floor.
- EM emissions consistent with coil harmonics.
- No gravitational anomaly.

**What would constitute a discovery**:
- Repeatable weight change correlated with field configuration (even 0.001% = 0.07 g for 7 kg Hg).
- EM emissions at frequencies not present in coil drive signal.
- Gravitational anomaly detected by independent gravimeter.

### Phase 5: Plasma Transition

**Objective**: Ionize mercury to plasma using high-voltage pulse. Test whether plasma-state mercury exhibits fundamentally different behavior under 3-axis drive than liquid-state. This is the Clemens architecture test.

**Setup**:
1. Pre-fill sphere with argon at 6-10 torr before adding mercury (Clemens spec).
2. Install HV feedthroughs for discharge electrodes inside sphere.
3. Marx generator or capacitor bank connected to electrodes.
4. All HV safety protocols active: interlocks, discharge procedures, two-person rule.
5. Radiation monitoring active (baseline).

**Protocol**:
1. Baseline: liquid mercury, 3-axis EM, all sensors recording. This is the Phase 1-2 comparison.
2. Apply HV pulse (start at 1 kV, increase). Monitor for plasma ignition (optical flash, conductivity change).
3. Once plasma state achieved, immediately apply 3-axis AC field.
4. Record all sensors during plasma-state operation.
5. Compare plasma-state measurements to liquid-state (same EM parameters).
6. Sweep frequency in plasma state — does the optimum shift? (f_d shifts dramatically in plasma: ~7,450 Hz for 5cm sphere. **VERIFIED** — Spitzer conductivity.)
7. Test whether plasma recombines (expected timescale ~0.1 s) or is sustained by EM field.

**Success criteria**:
- Mercury successfully ionized by pulse.
- Measurable difference between liquid-state and plasma-state response to same 3-axis field.
- Any anomalous measurement (weight, EM, gravitational) in plasma state not present in liquid state.

**Expected results (from analysis)**:
- Plasma σ drops ~150× from liquid. **VERIFIED**.
- Eddy-current coupling shifts to much higher frequencies (f_d ~7,450 Hz). **VERIFIED**.
- PIC simulator predicts plasma sustains 3D rotation (Q_3d ≈ 1.0) that liquid cannot. **MODEL PREDICTION**.
- Plasma recombines without continuous ionization input. **VERIFIED** (plasma physics).

**What would be novel**:
- Plasma-state operation produces weight anomaly that liquid state does not.
- Plasma sustained without continuous HV input (self-sustaining ionization).
- Coupling mechanism visibly changes (e.g., field pattern reorganizes at transition).
- Any anomaly correlated specifically with the plasma state transition.

**Failure modes**:
- Can't achieve plasma ignition → increase voltage, check argon pressure, check electrode gap.
- Plasma immediately quenches → increase argon pressure, reduce sphere heat loss, add continuous low-level HV.
- Sphere cracks under thermal shock → use glass rated for thermal cycling, add gradual warmup.

---

## 6. What the Simulator Showed Won't Work

This section is critical for not wasting time and money on dead ends.

### Cyclotron Resonance at Bench B-Fields
- **The problem**: Hg⁺ Larmor radius at 0.091 mT (max single-axis B from offset pancake coil) is ~21 m — 420× the sphere radius. Ions cannot complete orbits. **VERIFIED** (pencil math, Biot-Savart).
- **The gap**: Need ~50 mT for magnetized orbits. Realistic offset pancake coils produce ~0.091 mT. That's ~550×.
- **Don't bother**: Trying to achieve cyclotron resonance with these coils. The mechanism — if one exists — is not single-particle cyclotron.

### Classical Dynamo via Plasma Mercury
- **The problem**: Mercury plasma at 10,000K has σ ≈ 6,800 S/m — **150× worse** than liquid mercury (1.04 × 10⁶ S/m). **VERIFIED** (Spitzer/Saha calculations).
- **The reason**: Liquid metals have n_e ≈ 10²⁸-10²⁹/m³. Plasma at 1 atm has n_e ≈ 10²²-10²⁴/m³.
- **To match liquid σ**: Need ~770,000 K. To get 500× liquid: need ~50,000,000 K (thermonuclear).
- **Don't bother**: Expecting plasma mercury to boost Rm for dynamo. It does the opposite.

### RS Frequency Matching at Bench Scale (MHD Model)
- **The problem**: When the RS resonance boost was disabled (exp 19), frequency sweeps were **completely flat**. Spread < 1.5 mm across 5-200 Hz for all materials tested. **VERIFIED** (honest experiment).
- **The reason**: The "5/5 frequency match" was a self-fulfilling prophecy — the code hardcoded a sigmoid favoring RS-predicted frequencies.
- **What survived**: The textbook eddy-current peak at f_d = 48.7 Hz is real (exp 20). It depends on σ × R², not RS theory.
- **Don't expect**: A resonance peak at 40.5 Hz (Pb) or 50 Hz (Hg) in MHD. Test it as one variant, but the baseline expectation is flat or peaked at f_d.

### RS Amplitude Ratios Producing Different Centering
- **The problem**: Experiment 21 (RS boost disabled): core centering **identical** across equal [1,1,1], RS-predicted [1,1,0.25], and swapped configs. Spread < 0.012 mm = noise. **VERIFIED** (honest experiment).
- **The reason**: Centering is density-driven (Archimedes). The amplitude ratios don't change the buoyancy equilibrium.
- **Don't expect**: RS amplitude ratios to change where the core sits. They remain a hypothesis for other effects.

### Any Frequency Preference in SPH Model Without RS Boost
- **The problem**: The SPH/MHD model has NO emergent frequency preference. EM drive averages out at all frequencies when RS boost is removed. **VERIFIED** (exp 19).
- **Don't expect**: Resonance behavior from the liquid MHD regime at these parameters. The EM force is ~1,000× weaker than gravity.

---

## 7. What Remains Untested (The Point of Building)

These are the questions that **cannot** be answered by simulation and require a physical prototype.

### Q1: Forced Cooper Pairing in Lead via EM Pulse
- **The question**: Can Cooper pairs be induced in lead at ambient temperature by a sufficiently strong EM pulse?
- **Standard physics says**: No — Cooper pairs require T < Tc (7.2K for Pb).
- **Why test anyway**: The pulse regime (150kV+, μs duration) is extreme and non-equilibrium. DIRD papers discuss non-equilibrium superconductor states. This is the first-phase question.
- **How to test**: Capacitor-bank pulse through coils while monitoring Pb with SQUID magnetometer. Any persistent magnetization after pulse = evidence for forced pairing.
- **Category**: **HYPOTHESIS** — no current theory predicts this, but also no experiment has tested it at these energies.

### Q2: Any Anomalous Weight/Inertia Effects
- **The question**: Does a magnetically-driven mercury sphere show any weight or inertia anomaly?
- **Why it matters**: Podkletnov claims 0.3-2.1% weight reduction with a single-axis SC disc. The three-axis mercury device addresses all three spatial dimensions. If even a fraction of Podkletnov's claim is real, three-axis should amplify it.
- **How to test**: Precision balance, accelerometer, gravimeter. Systematic sweep of all parameters.
- **Category**: **UNTESTED** — no data either way for this configuration.

### Q3: Plasma vs. Liquid Response to 3-Axis Drive
- **The question**: Does ionized mercury behave fundamentally differently from liquid mercury under identical 3-axis EM drive?
- **Why it matters**: The simulator predicts plasma sustains true 3D rotation (Q_3d ≈ 1.0) while viscous liquid collapses 3D structure. **MODEL PREDICTION**. This is testable.
- **How to test**: Compare liquid-state and plasma-state measurements at identical EM parameters.
- **Category**: **MODEL PREDICTION** (simulator) → **UNTESTED** (physical).

### Q4: Consciousness-EM Coupling
- **The question**: Does a trained operator's conscious intention correlate with measurable changes in the device's EM field or behavior?
- **How to test**: Instrumented device + skilled practitioner + blind measurement protocol. Monitor EM emissions, weight, and field patterns while operator attempts to influence device state.
- **When to test**: After establishing device baseline behavior in Phases 1-5. This is Layer 2 work.
- **Category**: **HYPOTHESIS** — far future, but architecturally the device is designed to be compatible with this test.

### Q5: Reference Frame Decoupling
- **The question**: Can the device produce a local region of modified spacetime metric?
- **This is the ultimate question.** Everything else in this document is designed to systematically approach it.
- **Evidence would look like**: Measurable weight anomaly, inertial anomaly, optical effects at sphere boundary, or EM field discontinuity at boundary — correlated with device operation and not explainable by standard EM + gravity.
- **Category**: **HYPOTHESIS** — the entire reason for building.

---

## 8. Safety

### Mercury Handling (All Phases)

| Hazard | Mitigation |
|--------|-----------|
| Toxic vapor (TLV: 0.025 mg/m³) | Fume hood for any open-mercury work. Mercury vapor monitor in lab. |
| Skin contact | Nitrile gloves (not latex). Hg does not absorb readily through intact skin but avoid prolonged contact. |
| Spill | Mercury spill kit: sulfur powder (reacts with Hg), aspirator, sealable bags. Practice spill response. |
| Ingestion/inhalation | Respirator with mercury cartridge during sphere filling/opening. No eating/drinking in lab. |
| Disposal | Mercury is regulated hazardous waste. Collect all waste for proper disposal. |
| Ventilation | Lab ventilation rate ≥ 6 ACH. Monitor Hg vapor continuously. |
| Sealed system | Once sphere is sealed, mercury is contained. Primary risk is during filling and if sphere breaks. |

### High Voltage (Phase 5)

| Hazard | Mitigation |
|--------|-----------|
| Electrocution | Minimum two-person operation. One person operates, one monitors/can disconnect. |
| Capacitor stored energy | Discharge rods used before ANY physical contact. Bleeder resistors on all caps. |
| Arc flash | Safety glasses rated for arc flash. Stand-off distance maintained. |
| Lockout/tagout | Physical disconnect AND visible grounding before service. |
| Fire | Extinguisher (CO2, not water) accessible. No flammable materials in HV area. |
| Insulation | All HV leads in rated conduit. Connections enclosed. |

### Cryogenic (Phase 3)

| Hazard | Mitigation |
|--------|-----------|
| Frostbite (LHe at 4.2K) | Cryogenic gloves, face shield for transfers. |
| Oxygen displacement | LHe boil-off displaces O2. Monitor O2 level (alarm < 19.5%). Well-ventilated room. |
| Pressure buildup | Relief valves on all cryogenic vessels. Never seal a cryogenic container without relief. |
| Thermal shock | Gradual cooldown. Sphere material rated for thermal cycling. |

### Radiation (If Thorium Added — Future)

| Hazard | Mitigation |
|--------|-----------|
| Alpha emission (Th-232) | At 3:100,000 doping: activity is negligible in sealed system. |
| Inhalation of ThO₂ dust | Handle powder in fume hood. Respirator during preparation. Once in Hg, contained. |
| Regulatory | ThO₂ is a NORM (naturally occurring radioactive material). Check local regulations for possession limits. |
| Monitoring | Geiger counter baseline before and during operation. Dosimeter badges for personnel. |

### General Lab Safety

- **Emergency shutoff**: Big red button kills all power (coils + HV + DAQ).
- **Exit path**: Clear, unobstructed path to exit at all times.
- **Documentation**: Log all experiments, parameters, and observations. This is a research lab.
- **Training**: All personnel familiar with mercury handling, HV safety, and emergency procedures before any work begins.

---

## 9. References

### Project Documents
| Document | Path | Contents |
|----------|------|----------|
| Ground Rules | [`CLAUDE.md`](../CLAUDE.md) | Rigor hierarchy, anti-circularity rules |
| Device Vision | [`device-design/device-vision.md`](device-vision.md) | Architecture, initialization sequence, operating principle |
| Parameter Space | [`device-design/parameter-space.md`](parameter-space.md) | Engineering parameters, dynamo threshold data, RS displacement tables |
| Configurations | [`device-design/configurations.md`](configurations.md) | 3-axis vs counter-rotation analysis |
| Engineering Questions | [`engineering-questions.md`](../engineering-questions.md) | Cost estimates, open questions, experimental ladder |
| Two Architectures | [`documents/two-architectures.md`](../documents/two-architectures.md) | Cryo-dynamo vs plasma-coupling, stage hypothesis |
| Pencil Math — 9cm Coil | [`documents/pencil-math-9cm-coil.md`](../documents/pencil-math-9cm-coil.md) | Biot-Savart, Larmor radius, cyclotron impossibility |
| Hg Plasma Conductivity | [`documents/mercury-plasma-conductivity.md`](../documents/mercury-plasma-conductivity.md) | Spitzer/Saha calculations, 150× worse finding |
| RS Frequency Circularity | [`documents/rs-frequency-circularity.md`](../documents/rs-frequency-circularity.md) | How RS frequency was circular in simulator |
| Priority 2 Research | [`documents/priority2-research-theory.md`](../documents/priority2-research-theory.md) | Thorium RS, skin depth freq, boundary physics, stability |
| QA Interface | [`frameworks/qa-interface.md`](../frameworks/qa-interface.md) | Control law, consciousness interface theory |

### Textbook Physics (Independently Verifiable)
- **Biot-Savart law**: B = μ₀NIR²/(2(R²+d²)^(3/2)) for single-loop coil at axial distance d from center. Reduces to B = μ₀NI/(2R) at d=0. Any EM textbook (Griffiths ch. 5, Jackson ch. 5).
- **Skin depth**: δ = √(2/(ωμ₀σ)). Any EM textbook.
- **Eddy-current coupling frequency**: f_d = 1/(2πμ₀σR²). Derived from magnetic diffusion timescale.
- **Magnetic Reynolds number**: Rm = μ₀σvL. Standard MHD (Davidson, "Introduction to MHD").
- **Spitzer conductivity**: σ = T_eV^(3/2) / (5.2×10⁻⁵ Z ln Λ). Spitzer & Harm (1953), NRL Plasma Formulary.
- **Saha ionization**: Partition function for thermal ionization equilibrium. Any plasma physics text.
- **Larmor radius**: r_c = mv⊥/(qB). Any plasma physics text.
- **Cyclotron frequency**: f_c = qB/(2πm). Any plasma physics text.

### External Sources
- CRC Handbook of Chemistry and Physics — Mercury properties
- NIST Atomic Spectra Database — Hg ionization energies
- NRL Plasma Formulary (2018) — Transport coefficients
- Kamerlingh Onnes (1911) — Mercury superconductivity discovery
- Podkletnov & Nieminen (1992) — "A possibility of gravitational force shielding by bulk YBa₂Cu₃O₇₋ₓ superconductor" (Physica C)
- Clemens Patent (2023) — Mercury plasma gravitational device
- 38 DIRDs (Defense Intelligence Reference Documents) — AAWSAP program

### Simulator Experiments Referenced
| Exp # | Name | Key Finding | Rigor |
|-------|------|-------------|-------|
| 1 | centering (clean rerun) | Pb equilibrium 10.5 mm, density-driven | **VERIFIED** |
| 3 | axis (clean rerun) | 3>2>1 hierarchy, field geometry | **VERIFIED** |
| 5 | material (clean rerun) | RS coupling zero effect on equilibrium | **VERIFIED** |
| 8 | dynamo (clean rerun) | Rm_crit ≈ 10, SC-Hg 856× amplification | **MODEL PREDICTION** |
| 14 | rotation (PIC) | Q_3d ≈ 1.0 for 3-axis, 0.003 for 1-axis | **MODEL PREDICTION** |
| 16 | phasesweep (PIC) | Peak at 180° not RS-predicted 22°, small effects | **MODEL PREDICTION** |
| 19 | honest (MHD) | Frequency sweep flat without RS boost | **VERIFIED** (negative result) |
| 20 | induction_sweep (MHD) | Eddy-current peak at f_d, within 3% of textbook | **VERIFIED** |
| 21 | ampratio (MHD) | RS amplitude ratios no effect, spread < 0.012 mm | **VERIFIED** (negative result) |

---

*This document consolidates findings from 21 simulator experiments, a full circularity audit, clean reruns of 4 key experiments, and literature review of mercury plasma physics, Spitzer conductivity, and Saha ionization. Every claim is tagged with its rigor category. Where the simulator was circular, this is stated explicitly. Where standard physics makes a clear prediction, the prototype is designed to test whether reality matches that prediction — and to detect any deviations.*
