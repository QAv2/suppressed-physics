# Pencil Math: 9cm Sphere + Pancake Coil — Is Cyclotron Resonance Reachable?

**Date**: 2026-02-21
**Purpose**: Determine whether a realistic pancake coil can produce B-fields strong enough for magnetized Hg⁺ orbits inside a 9cm sphere.
**Method**: Textbook Biot-Savart + cyclotron physics. No RS, no simulator. Independently verifiable.

---

## 1. Coil Geometry (from Joseph's Gemini session, recalled)

- **Type**: Flat pancake air coil
- **Turns**: 4–6
- **Approximate diameter**: ~45 cm (17.7") — comparable to standard 45 lb weight plate
- **Coil radius**: R_coil ≈ 0.225 m
- **Wire**: Heavy gauge copper (assume 4 AWG ~ 5.2mm diameter for heavy current)
- **Three coils**: orthogonal (gimbal), each producing field along one axis

## 2. B-Field at Center of a Flat Coil (Biot-Savart)

For a single circular loop of radius R carrying current I, the on-axis field at center (z=0):

> **B = μ₀NI / (2R)**

Where:
- μ₀ = 4π × 10⁻⁷ T·m/A = 1.2566 × 10⁻⁶ T·m/A
- N = number of turns
- I = current (amperes)
- R = coil radius (meters)

This is exact for a thin coil at its center. For a pancake (turns spread radially), it's an approximation — the inner turns contribute more, outer turns less. For 4-6 turns of 5mm wire, the radial spread is ~2-3 cm on a 22.5 cm radius, so the thin-coil approximation is good to ~10%.

### Calculation Table

| N (turns) | I (A) | R (m)  | B = μ₀NI/(2R) (mT) |
|-----------|-------|--------|---------------------|
| 4         | 10    | 0.225  | 0.0112              |
| 4         | 20    | 0.225  | 0.0223              |
| 4         | 50    | 0.225  | 0.0559              |
| 4         | 100   | 0.225  | 0.112               |
| 6         | 10    | 0.225  | 0.0168              |
| 6         | 20    | 0.225  | 0.0335              |
| 6         | 50    | 0.225  | 0.0838              |
| 6         | 100   | 0.225  | 0.168               |

**Verification**: For N=1, I=1A, R=0.225m: B = (1.257e-6 × 1)/(2 × 0.225) = 2.79 μT. ✓ (standard result)

### Reality check on current
- 4 AWG copper: rated ~60-85A continuous in free air (NEC), higher with active cooling
- 100A through 4 AWG is achievable but requires cooling (water jacket or pulsed operation)
- At 50A continuous: comfortable for heavy gauge, no special cooling needed

**Result**: These coils produce B ≈ 0.01–0.17 mT at the sphere center.

### ⚠️ PROBLEM IMMEDIATELY VISIBLE

Previous experiments used B_dc = 0.65 mT. These realistic coils top out at **0.17 mT at 100A** with 6 turns.

The sphere center is where B is strongest (on-axis). The sphere wall (4.5 cm off-center for 9cm sphere) sees somewhat less.

## 3. Hg⁺ Ion Cyclotron Physics

### Larmor (cyclotron) radius

> **r_c = m v_⊥ / (|q| B)**

Where:
- m_Hg = 200.59 u = 200.59 × 1.6605 × 10⁻²⁷ kg = **3.331 × 10⁻²⁵ kg**
- q = e = 1.602 × 10⁻¹⁹ C (singly ionized)
- v_⊥ = thermal velocity perpendicular to B

### Thermal velocity at plasma temperature

> **v_thermal = √(k_B T / m)**

| T (K)    | v_thermal (m/s) | Context                    |
|----------|-----------------|----------------------------|
| 300      | 2.88            | Room temp (not plasma)     |
| 1,000    | 5.26            | Warm gas                   |
| 5,000    | 11.8            | Low-temp plasma            |
| 10,000   | 16.6            | Typical Hg arc plasma      |
| 50,000   | 37.2            | Hot plasma                 |

**Verification**: v = √(1.381e-23 × 10000 / 3.331e-25) = √(4.145e-4 / 3.331e-25) = √(1.244e21) ...

Wait, let me redo this carefully:
- k_B T = 1.381e-23 × 10000 = 1.381e-19 J
- k_B T / m = 1.381e-19 / 3.331e-25 = 4.145e5 m²/s²
- v = √(4.145e5) = **644 m/s**

I made an error above. Let me recalculate all:

| T (K)    | k_BT/m (m²/s²) | v_thermal (m/s) | Context                    |
|----------|-----------------|-----------------|----------------------------|
| 300      | 1.244e4         | 112             | Room temp (not plasma)     |
| 1,000    | 4.145e4         | 204             | Warm gas                   |
| 5,000    | 2.072e5         | 455             | Low-temp plasma            |
| 10,000   | 4.145e5         | 644             | Typical Hg arc plasma      |
| 50,000   | 2.072e6         | 1,439           | Hot plasma                 |

**Verification check**: Mercury atomic mass = 200.59 u. At 10,000 K:
- k_B T = 1.381e-23 × 1e4 = 1.381e-19 J = 0.863 eV ✓ (thermal energy ~ 1 eV at 10kK)
- v = √(2 × 0.863 eV / 200.59 u) ... using eV and u: v = √(2 × 0.863 × 1.602e-19 / (200.59 × 1.661e-27))
- = √(2.766e-19 / 3.331e-25) = √(8.303e5) = 911 m/s

Hmm, discrepancy — ah, the √(k_BT/m) is the 1D thermal speed. The mean speed is √(8k_BT/πm) and RMS perpendicular is √(2k_BT/m). For Larmor radius, we want v_⊥ which has 2 degrees of freedom:

> **v_⊥,rms = √(2 k_B T / m)**

| T (K)    | v_⊥,rms (m/s)  | Context                    |
|----------|-----------------|----------------------------|
| 300      | 158             | Room temp                  |
| 1,000    | 288             | Warm gas                   |
| 5,000    | 644             | Low-temp plasma            |
| 10,000   | 911             | Typical Hg arc plasma      |
| 50,000   | 2,036           | Hot plasma                 |

### Larmor radius: r_c = m × v_⊥ / (q × B)

For Hg⁺ at T = 10,000 K (v_⊥ = 911 m/s):

| B (mT)  | r_c (m)  | r_c / R_sphere (4.5cm) | Magnetized? |
|---------|----------|------------------------|-------------|
| 0.01    | 189.9    | 4,220×                 | NO          |
| 0.05    | 37.98    | 844×                   | NO          |
| 0.10    | 18.99    | 422×                   | NO          |
| 0.17    | 11.17    | 248×                   | NO          |
| 0.65    | 2.92     | 64.9×                  | NO          |
| 5.0     | 0.380    | 8.4×                   | NO          |
| 20.0    | 0.095    | 2.1×                   | NO          |
| 50.0    | 0.038    | 0.84×                  | YES (barely)|
| 100.0   | 0.019    | 0.42×                  | YES         |
| 200.0   | 0.0095   | 0.21×                  | YES (good)  |

**Verification**: r_c = (3.331e-25 × 911) / (1.602e-19 × 0.050) = 3.035e-22 / 8.01e-21 = 0.0379 m ✓

### Cyclotron frequency

> **f_c = qB / (2π m)**

| B (mT) | f_c (Hz)  |
|---------|-----------|
| 0.17    | 13.0      |
| 0.65    | 49.7      |
| 5.0     | 382       |
| 50.0    | 3,823     |
| 100.0   | 7,647     |
| 200.0   | 15,293    |

**Note**: f_c = 49.7 Hz at B = 0.65 mT — this is the RS prediction for Hg (total displacement = 10). Previously noted in memory. But as we see above, at that B the orbits are NOT magnetized (r_c = 2.92 m >> 4.5 cm).

## 4. Assessment

### The core problem

For a 9cm sphere with Hg⁺ plasma at ~10,000 K:
- **Realistic pancake coils (45cm, 4-6 turns, ≤100A) produce B ≈ 0.01–0.17 mT**
- **Magnetized orbits require B ≥ ~50 mT** (r_c ≤ R_sphere)
- **Gap: ~300× to 5000×**

This is not close. The coils would need to produce ~300× more field to get magnetized orbits.

### Ways to close the gap

| Approach                          | Factor gained | Practical?        |
|-----------------------------------|---------------|-------------------|
| More turns (6→60)                 | 10×           | Bigger coil, more resistance |
| Higher current (100A→1000A)       | 10×           | Needs serious power supply + cooling |
| Smaller coil radius (bring coils closer to sphere) | ~2-3× | Reduces uniformity |
| Lower plasma temperature          | √T factor     | Defeats ionization purpose |
| Helmholtz pair (two coils/axis)   | ~1.3×         | Marginal gain     |
| Iron core / flux concentrator     | 10-100×       | Destroys air-coil concept |
| Pulsed operation (capacitor bank) | 10-100×       | Changes the physics |
| Superconducting coils             | Any needed    | $$$, cryo complexity |

### The honest conclusion

**A 45cm diameter, 4-6 turn pancake air coil cannot produce magnetized Hg⁺ orbits in a 9cm sphere at plasma temperatures.** The gap is ~300×. You'd need either:

1. A fundamentally different coil (many more turns, much closer to sphere, or iron-cored), OR
2. Much lower ion temperatures (but then it's not really a plasma), OR
3. The mechanism doesn't rely on classical cyclotron resonance at all

Option 3 is worth taking seriously. ~~The RS frequency formula works in the MHD simulator (5/5 elements confirmed)~~ **CORRECTION (audit 2026-02-22)**: The "5/5 confirmed" result was CIRCULAR — the simulator hardcoded a boost favoring RS-predicted frequencies. When the boost was disabled (experiment 19), frequency sweeps were flat. The RS frequency formula is an untested hypothesis.

That said, the mechanism question remains open:
- Faraday induction (E ∝ ω) is the dominant energy transfer mechanism (PIC experiment 17: monotonic ∝ f^0.87)
- Textbook eddy-current coupling peaks at f_d = 1/(2πμ₀σR²) — verified analytically (exp 20)
- There may be collective/MHD effects that don't require individual ion magnetization

### What this does NOT disprove
- It does not disprove that the device works — only that classical single-particle cyclotron resonance is unlikely to be the mechanism at these parameters
- The MHD/collective behavior may operate differently from single-particle physics
- There may be mechanisms in RS theory that don't map to standard plasma physics

## 5. Assumptions to flag

1. **Thin coil approximation**: Good to ~10% for this geometry. Conservative (real B slightly lower).
2. **On-axis field only**: Field at sphere center. Off-center is lower. Optimistic estimate.
3. **Singly ionized Hg**: If multiply ionized, q increases, r_c decreases by 1/Z. Hg²⁺ helps 2×, still not enough.
4. **Thermal equilibrium**: Assumed Maxwellian distribution. Real plasma might have non-thermal populations.
5. **Uniform B assumption**: Real pancake coil field is non-uniform across 9cm sphere. Doesn't help — average B is lower than center B.
6. **No collective effects**: This is single-particle physics. Plasma collective effects (waves, instabilities) may change the picture.
