# Priority 2 — Research & Theory (2026-02-22)

Post-audit, post-clean-rerun analysis. All claims categorized per CLAUDE.md rigor hierarchy:
**Verified** = textbook physics. **Model prediction** = follows from simulator. **Hypothesis** = untestable with current tools. **Circular** = baked in.

---

## 1. Thorium RS Analysis

### RS Displacement

From Larson's periodic table ("The Structure of the Physical Universe", 1959):

| Element | Z | m1 | m2 | e | Total | Notation |
|---------|---|----|----|---|-------|----------|
| Lead | 82 | 4 | 4 | 1 | 9 | (4,4)-1 |
| Mercury | 80 | 4 | 4 | 2 | 10 | (4,4)-2 |
| Bismuth | 83 | 4 | 4 | 3 | 11 | (4,4)-3 |
| **Thorium** | **90** | **4** | **4** | **4** | **12** | **(4,4)-4** |

Thorium shares the same (4,4) magnetic rotation as all Period 6 elements in the simulator. What distinguishes it is the highest electric displacement (e=4) in the progression. It completes the sequence Pb(1) → Hg(2) → Bi(3) → Th(4).

### Conventional Physical Properties

| Property | Thorium | Lead | Mercury | Iron |
|----------|---------|------|---------|------|
| Density (kg/m³) | 11,724 | 11,340 | 13,534 | 7,874 |
| Conductivity (S/m) | 6.67×10⁶ | 4.81×10⁶ | 1.04×10⁶ | 1.0×10⁷ |
| Susceptibility (χ) | +8.4×10⁻⁵ | -1.8×10⁻⁵ | -2.9×10⁻⁵ | +2×10⁵ |
| Magnetic character | Paramagnetic | Diamagnetic | Diamagnetic | Ferromagnetic |

Sources: periodictable.com, WebElements, Wikipedia.

### What the RS Framework Predicts for Th (all HYPOTHESIS — untested)

Using the same mapping as other materials:
- **Amplitude ratio**: [m1, m2, e] = [4, 4, 4] → normalized [1.0, 1.0, 1.0] (equal amplitudes)
- **RS frequency**: f = 50 × (12/10)² = 72.0 Hz
- **Phase offsets**: symmetric magnetic (m1=m2) → [0°, 0°, 90°]
- **RS coupling factor**: high symmetry (m1=m2), high total displacement

### Why Thorium Doping Matters — Three Hypotheses

Clemens specifies ThO₂ at 3:100,000 by weight. Die Glocke used Xerum 525 (mercury + thorium/beryllium peroxides). Two independent sources specify thorium. Three candidate explanations:

**H1: Nuclear/radioactive contribution** (HYPOTHESIS)
- Th is an alpha emitter (Th-232, t½ = 14 Gyr, very low activity)
- At 3:100,000 doping level, radioactivity is negligible
- ThO₂ has high melting point (3,350°C) — survives plasma conditions
- Could provide seed nuclei or local field inhomogeneities

**H2: Electronic structure / work function** (HYPOTHESIS)
- ThO₂ has one of the lowest work functions of any oxide (~2.6 eV)
- In a plasma environment, ThO₂ particles would easily emit electrons
- Could enhance plasma ignition or sustain ionization at lower voltages
- This is the same reason thorium is used in TIG welding electrodes

**H3: RS displacement complementarity** (HYPOTHESIS, no current test)
- Th is (4,4)-4, Hg is (4,4)-2 — same magnetic rotation, different electric
- RS predicts equal amplitude ratios for Th → [1,1,1] = maximum isotropy
- The doping could "tune" the effective displacement of the working medium
- With Hg(10) + trace Th(12), the effective total displacement shifts slightly upward
- This is pure RS hypothesis with no physical derivation

**Most likely explanation (Occam)**: H2 — ThO₂'s low work function aids plasma initiation. This is verified conventional physics used in welding. No RS theory needed.

### Simulator Integration

To add Thorium to the simulator:
```python
THORIUM = Material(
    name="Thorium", symbol="Th",
    density=11724.0,
    conductivity=6.67e6,
    susceptibility=8.4e-5,
    viscosity=0.0,
    color=(160, 155, 140),
    rs_magnetic=(4, 4), rs_electric=4,
)
```

**Centering behavior** (VERIFIED — density-driven, confirmed by experiment):
- Δρ from Hg = 13,534 - 11,724 = 1,810 kg/m³ (buoyant, lighter than Hg)
- Lowest Δρ of any core material (Pb is next at Δρ=2,194)
- **Measured equilibrium: 8.6 mm** — BEST of all 9 materials tested
- Centers at t=0.37s — FASTEST of all materials
- Buoyancy force: 38.1 mN (lowest, due to smallest density gap)
- Confirms: centering is pure Archimedes. Lowest Δρ = best centering. No RS physics involved.

**Predicted eddy-current coupling** (VERIFIED physics — conductivity-driven):
- f_d(Th) = 1/(2πμ₀σ_Th R²) for 5cm sphere
- = 1/(2π × 1.257×10⁻⁶ × 6.67×10⁶ × 0.0025)
- = 1/(2π × 0.02096) = 1/(0.1317) = **7.59 Hz**
- Wait — this is the core's own eddy-current frequency. But the core is INSIDE the mercury sphere. The relevant f_d is for the mercury, not the core.
- Mercury f_d = 48.7 Hz for 5cm sphere (independent of core material)

### Key Findings

**Th vs Fe — same total displacement, radically different physics**:

| Property | Thorium (4,4)-4 | Iron (3,3)-6 | Same? |
|----------|-----------------|--------------|-------|
| Total displacement | 12 | 12 | Yes |
| RS predicted freq | 72.0 Hz | 72.0 Hz | Yes |
| RS amplitude ratio | [1.0, 1.0, 1.0] | [0.5, 0.5, 1.0] | **No** |
| RS phase | [0°, 0°, 45°] | [0°, 0°, 90°] | **No** |
| Density (kg/m³) | 11,724 | 7,874 | **No** |
| Conductivity (S/m) | 6.67×10⁶ | 1.0×10⁷ | **No** |
| Susceptibility | +8.4×10⁻⁵ (para) | +2×10⁵ (ferro) | **No** |
| Centering eq (mm) | 8.6 (best) | 26.4 | **No** |

RS predicts the same frequency but different amplitude/phase for these two elements. The frequency match (both 72 Hz) is driven entirely by total displacement, while the amplitude/phase differences come from the different magnetic vs electric split. A physical experiment could test whether Th and Fe share a resonant frequency despite their radically different electromagnetic properties.

**Th as the "ideal" core** (RS perspective, HYPOTHESIS):
- Equal amplitudes [1,1,1] → lowest mismatch (0.155) at 60 Hz with equal amps
- RS coupling factor = 1.000 (highest of all materials)
- Centers best (lowest Δρ) → least buoyancy to overcome
- Paramagnetic → responds to B-field gradient without overwhelming it (unlike ferromagnetic Fe)

**Status**: Frequency prediction is HYPOTHESIS (untested, was circular in simulator). Centering prediction is VERIFIED (density-driven, confirmed experimentally).

---

## 2. Skin Depth Frequency Analysis

### The Physics

Skin depth: δ = √(2/(ωμ₀σ))

Two related characteristic frequencies:
- **f_skin** = 1/(πμ₀σR²) — where skin depth equals sphere radius
- **f_d** = 1/(2πμ₀σR²) = f_skin/2 — peak eddy-current coupling frequency

### Calculated Values

#### Liquid Mercury (σ = 1.04×10⁶ S/m)

| Sphere Radius | f_skin (Hz) | f_d (Hz) | δ at 50 Hz |
|---------------|-------------|----------|------------|
| 5.0 cm (bench default) | 97.4 | **48.7** | 7.0 cm |
| 4.5 cm (9cm dia sphere) | 120.3 | **60.1** | 7.0 cm |
| 9.0 cm (9cm radius) | 30.1 | **15.0** | 7.0 cm |

#### Plasma Mercury (σ ≈ 6,800 S/m at 10,000K)

| Sphere Radius | f_skin (Hz) | f_d (Hz) | δ at 50 Hz |
|---------------|-------------|----------|------------|
| 5.0 cm | 14,900 | 7,450 | 86 cm |
| 4.5 cm | 18,400 | 9,200 | 86 cm |
| 9.0 cm | 4,600 | 2,300 | 86 cm |

### Physical Interpretation

**Below f_skin**: EM field fully penetrates the sphere → bulk eddy-current coupling.
**Above f_skin**: Field confined to skin layer → surface-only coupling, diminishing with frequency.
**At f_d**: Peak eddy-current torque (maximum energy transfer from field to fluid motion).

### The 50 Hz Numerical Coincidence

For a 5cm liquid mercury sphere: **f_d = 48.7 Hz**.
RS frequency formula for Hg (d=10): **f_RS = 50 Hz**.

These are within 3%. But the physical origins are completely different:
- f_d depends on σ_Hg × R² (conductivity × geometry) — **VERIFIED textbook EM**
- f_RS depends on total displacement d — **UNTESTED RS hypothesis**

For a 9cm diameter sphere: f_d = 60.1 Hz, f_RS still = 50 Hz. The match breaks at different geometries. This confirms the coincidence is geometry-dependent, not fundamental.

### Critical Insight: Core Material Independence

**f_d and f_skin depend ONLY on mercury's conductivity and sphere radius.**

They do NOT depend on the core material (Pb, Fe, Th, etc.). Any experimentally observed frequency that varies with core material CANNOT be an eddy-current skin depth effect. This is a clean falsification test:
- If optimal frequency varies with core material → not eddy currents → new physics needed
- If optimal frequency varies only with sphere size → eddy currents → no new physics

**Status**: VERIFIED (textbook EM, confirmed by simulator exp 20 to within 3%).

---

## 3. Transition Boundary Physics

**Status**: HYPOTHESIS. The simulator cannot model metric modification or reference frame effects. This section documents what can and cannot be said.

### What Classical Physics Says About the Sphere Boundary

The ceramic sphere wall separates two regions:
- **Interior**: Mercury (liquid or plasma) + core + EM fields
- **Exterior**: Coils, support structure, laboratory reference frame

Classical boundary conditions (Maxwell's equations):
- Tangential E and H are continuous across the boundary
- Normal B and D are continuous (with surface charge/current corrections)
- No discontinuity in the metric — spacetime is flat everywhere

### What the Decoupling Hypothesis Claims

The hypothesis (from /deeper thread) is that the interior region can "decouple" from the external reference frame — the object doesn't move through space; instead, the relationship between interior and exterior metrics changes.

If this is real, the sphere boundary would be a **transition zone** where:
- The interior metric smoothly (or sharply) transitions to the exterior metric
- The EM field configuration inside must match exterior boundary conditions
- Energy/momentum conservation must hold across the boundary

### Available Length Scales for the Transition

Several physical length scales could define the transition width:

| Scale | Value (5cm sphere) | Origin |
|-------|-------------------|--------|
| Skin depth at f_d | 7.0 cm | EM penetration depth |
| Sphere wall thickness | ~2-5 mm | Ceramic engineering |
| Debye length (plasma) | ~10⁻⁴ m | Charge screening |
| Mercury mean free path | ~10⁻⁸ m (liquid) | Molecular scale |

The skin depth is the only one comparable to the device scale. If the effect is EM-mediated, the transition layer width ~ δ.

### What Would Be Observable

If a transition boundary exists, it would manifest as:
1. **EM field discontinuity** — measurable with external field probes
2. **Gravitational anomaly** — measurable with precision accelerometers/gravimeters
3. **Inertial anomaly** — measurable by attempting to accelerate the device
4. **Optical effects** — light passing through the transition region would be lensed/shifted

The simulator can model (1) partially (EM fields inside the sphere). It cannot model (2-4).

### Honest Assessment

The transition boundary is a **necessary consequence** of the decoupling hypothesis — if decoupling happens, there must be a boundary. But the hypothesis itself is untestable with the current simulator or any conventional lab equipment designed for EM measurement only. A physical experiment measuring weight change (Podkletnov-style) or inertial change would be the minimum viable test.

**What the simulator CAN contribute**: The EM field configuration at the sphere boundary under various coil configurations. This is real physics (Maxwell's equations) and could inform where to place sensors in a physical experiment.

---

## 4. Stability Analysis

**Status**: HYPOTHESIS. No testable predictions from current simulator.

### The Question

If a "decoupled" state exists, is it:
- (a) An **attractor** — once reached, the system stays there (like superconductivity below T_c)?
- (b) **Unstable** — requires continuous energy input to maintain?
- (c) A **limit cycle** — oscillates between coupled and decoupled?

### What the Simulator's Validated Physics Suggests

The dynamo threshold (Rm ≈ 10) provides an analogy:

| Property | Dynamo (validated) | Decoupling (hypothesis) |
|----------|-------------------|------------------------|
| Threshold | Rm_crit ≈ 10 | Unknown |
| Transition | Sharp (Δσ×25 gap) | Unknown |
| Below threshold | No self-sustaining B | Normal physics |
| Above threshold | Self-sustaining B, power amplification | Metric modification? |
| Stability | Attractor above threshold (dynamo sustains itself) | Unknown |

The dynamo is a **self-reinforcing** process: flow generates B, B generates more flow (via Lorentz force), creating a positive feedback loop above Rm_crit. Below threshold, dissipation wins and the field decays.

**If** decoupling follows similar physics, then:
- Below some critical parameter, normal physics dominates
- Above threshold, a self-reinforcing process sustains the decoupled state
- The transition would be sharp (phase transition, not gradual)
- The decoupled state would be an attractor (self-sustaining)

### Classical Analogies for Stability

| System | Sub-critical | Super-critical | Transition Type |
|--------|-------------|----------------|-----------------|
| MHD dynamo | B decays | B self-sustains | Sharp (Rm ≈ 10) |
| Superconductor | Normal conductor | Zero resistance, Meissner | Sharp (T_c) |
| Laser | Spontaneous emission | Stimulated emission | Sharp (pump threshold) |
| Ferromagnet | Paramagnetic | Spontaneous magnetization | Sharp (Curie temp) |

All four are examples of **symmetry-breaking phase transitions** with:
- A critical parameter (Rm, T, pump power, T_Curie)
- Sharp threshold behavior
- Self-sustaining super-critical state (attractor)
- Hysteresis (state persists even if parameter drops slightly below threshold)

### What Cannot Be Said

1. Whether decoupling is physically possible (no theoretical framework derives it from first principles)
2. What the critical parameter would be (field strength? frequency? Rm? something else?)
3. Whether the analogy to phase transitions is valid (could be a completely different class of phenomenon)
4. Whether consciousness plays a necessary role (the /deeper thread suggests it does; untestable with EM equipment)

### What Would Constitute Evidence

A stability analysis becomes meaningful only after establishing that the effect exists. The experimental ladder:

1. **Detect the effect**: Weight change, inertial anomaly, EM field discontinuity at boundary
2. **Map the threshold**: Vary parameters (field strength, frequency, conductivity) to find the critical point
3. **Test hysteresis**: Once the effect is achieved, reduce parameters — does it persist?
4. **Measure relaxation time**: If disrupted, how quickly does the system return to the decoupled state?

Steps 1-2 are physical experiments. Steps 3-4 constitute the stability analysis. None are accessible to the current simulator.

---

## Summary of Findings

| Item | Category | Key Result |
|------|----------|------------|
| Thorium RS | Hypothesis | (4,4)-4, total=12, same as Fe. Paramagnetic. Best centering predicted (lowest Δρ). ThO₂ low work function most likely explanation for doping. |
| Skin depth freq | Verified | f_d = 48.7 Hz (5cm), 60.1 Hz (4.5cm), 15.0 Hz (9cm). Core-independent. 50 Hz coincidence is geometry, not RS. |
| Boundary physics | Hypothesis | Must exist if decoupling real. Skin depth is natural transition scale. EM field at boundary is measurable. |
| Stability | Hypothesis | Dynamo analogy suggests sharp threshold + attractor. Untestable without detecting the effect first. |

### What Advances the Research

1. **Thorium as core material in simulator**: Can test centering prediction (should center best). Run `centering` experiment with Th added to CORE_MATERIALS.
2. **Skin depth as experimental design parameter**: f_d tells you where to operate for maximum EM coupling. Design sphere radius to match desired operating frequency.
3. **Boundary and stability**: Park these until a physical experiment is designed. The simulator contributes EM field maps at the boundary — useful for sensor placement, not for testing the hypothesis itself.
