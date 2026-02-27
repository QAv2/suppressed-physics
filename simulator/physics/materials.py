"""Material properties database + Reciprocal System periodic table mapping.

Each material has:
  1. Conventional physics properties (density, conductivity, susceptibility)
  2. RS displacement values (magnetic rotation, electric displacement)
  3. RS-derived optimal coil parameters (the "dialing up" prediction)

RS Periodic Table (Larson, 1959):
  Every element is characterized by quantized displacements from the natural datum (c).
  - Magnetic rotation: two components (m1, m2) — the rotational character
  - Electric displacement: one component (e) — the linear/scalar character
  - Total displacement = m1 + m2 + e = element's scalar motion identity

RS-to-Coil Mapping Hypothesis:
  The three coil axes map to the three displacement components:
    Coil X ↔ magnetic primary (m1)
    Coil Y ↔ magnetic secondary (m2)
    Coil Z ↔ electric displacement (e)

  Optimal configuration for a given element:
    - Amplitude ratio: proportional to displacement ratio [m1, m2, e]
    - Frequency: scales with total displacement (more displacement = higher natural frequency)
    - Phase: magnetic axes in sync, electric axis in quadrature (90° offset)

  This is a TESTABLE PREDICTION: auto-tuned parameters should produce faster/tighter
  centering than equal parameters for each material.
"""

import numpy as np
from dataclasses import dataclass, field


# === RS Constants ===
# Base frequency derived from Podkletnov empirical range (50-10^6 Hz)
# and scaled by displacement. This is the reference frequency for
# an element with total displacement = 1.
RS_BASE_FREQ = 50.0  # Hz — bottom of Podkletnov's empirical range

# Displacement reference — used to normalize frequency scaling
RS_REF_DISPLACEMENT = 10.0  # Mercury's total displacement (the working fluid)


@dataclass
class Material:
    name: str
    symbol: str
    density: float              # kg/m³
    conductivity: float         # S/m (electrical conductivity)
    susceptibility: float       # Dimensionless magnetic susceptibility (χ)
    viscosity: float            # Pa·s (dynamic viscosity, for fluids)
    color: tuple                # RGB for rendering

    # Reciprocal System displacement values
    # From Larson's "Nothing But Motion" and "The Structure of the Physical Universe"
    rs_magnetic: tuple = (0, 0)     # (primary, secondary) magnetic rotation
    rs_electric: int = 0            # Electric displacement

    @property
    def rs_total_displacement(self):
        """Total scalar motion displacement — RS 'identity' of the element."""
        return self.rs_magnetic[0] + self.rs_magnetic[1] + self.rs_electric

    @property
    def rs_displacement_vector(self) -> np.ndarray:
        """Displacement as 3-vector [m1, m2, e] for coil mapping."""
        return np.array([
            float(self.rs_magnetic[0]),
            float(self.rs_magnetic[1]),
            float(self.rs_electric),
        ])

    @property
    def rs_amplitude_ratio(self) -> np.ndarray:
        """
        Optimal coil amplitude ratio derived from RS displacement.
        WARNING: This is an RS HYPOTHESIS, not validated physics.
        Experiment 21 found NO special status for these ratios.

        Normalized so the maximum component = 1.0.
        Maps displacement components directly to coil axes:
          X-coil amplitude ∝ m1 (magnetic primary)
          Y-coil amplitude ∝ m2 (magnetic secondary)
          Z-coil amplitude ∝ e  (electric)
        """
        v = self.rs_displacement_vector
        mx = np.max(v)
        if mx < 0.01:
            return np.ones(3)
        return v / mx

    @property
    def rs_optimal_frequency(self) -> float:
        """
        Optimal coil frequency derived from RS displacement.
        WARNING: This is an RS HYPOTHESIS. Simulator "validation" (exp 7, 10)
        was CIRCULAR — the frequency preference was hardcoded via rs_resonance_boost.
        When the boost was disabled (exp 19), frequency sweeps were FLAT.
        This formula remains UNTESTED.

        f = 50 * (total_displacement / 10)^2 Hz
        """
        td = self.rs_total_displacement
        if td < 1:
            return RS_BASE_FREQ
        return RS_BASE_FREQ * (td / RS_REF_DISPLACEMENT) ** 2

    @property
    def rs_phase_offsets(self) -> np.ndarray:
        """
        Optimal phase offsets between coil axes (radians).
        WARNING: RS HYPOTHESIS. No physical derivation for why "electric
        displacement" should correspond to a 90-degree phase offset.
        Feeds into rs_resonance_mismatch with 25% weight.

        RS predicts:
          - Two magnetic axes share rotational character → in phase (0° offset)
          - Electric axis has linear character → in quadrature (90° offset)
          - The electric/magnetic ratio determines exact quadrature angle

        For symmetric magnetic displacement (m1 == m2):
          phases = [0, 0, π/2]

        For asymmetric magnetic displacement (m1 ≠ m2):
          phases = [0, π·(m2-m1)/(m1+m2), π/2]
          (slight offset between magnetic axes proportional to asymmetry)
        """
        m1, m2 = self.rs_magnetic
        e = self.rs_electric

        # Magnetic axes: in phase if symmetric, slight offset if asymmetric
        if m1 + m2 > 0:
            mag_offset = np.pi * abs(m2 - m1) / (m1 + m2) * 0.5
        else:
            mag_offset = 0.0

        # Electric axis: quadrature offset scaled by e/(m1+m2) ratio
        if m1 + m2 > 0:
            elec_offset = np.pi / 2.0 * min(e / (m1 + m2), 1.0)
        else:
            elec_offset = 0.0

        return np.array([0.0, mag_offset, elec_offset])

    @property
    def rs_coupling_factor(self) -> float:
        """
        RS-derived coupling efficiency factor.
        WARNING: This is PURE RS THEORY with no physical derivation. None of
        these relationships (symmetry→coupling, magnetic fraction→strength,
        displacement→coupling) are derived from any physical equation.
        DISABLED by default in CoreState (disable_rs_coupling=True) since
        audit 2026-02-22. Biases all cross-material comparisons if enabled.

        How well this material couples to a field tuned to its displacement.
        Based on the match between the material's displacement structure
        and the field's structure.
        """
        m1, m2 = self.rs_magnetic
        e = self.rs_electric
        td = self.rs_total_displacement
        if td < 1:
            return 0.1

        # Symmetry bonus: m1==m2 means balanced rotation
        if m1 + m2 > 0:
            symmetry = 1.0 - abs(m1 - m2) / (m1 + m2)
        else:
            symmetry = 0.5
        symmetry_factor = 0.7 + 0.3 * symmetry

        # Magnetic dominance: higher magnetic/total ratio → stronger rotational coupling
        mag_fraction = (m1 + m2) / td
        mag_factor = 0.5 + 0.5 * mag_fraction

        # Displacement strength: higher total → stronger identity → stronger coupling
        disp_factor = td / RS_REF_DISPLACEMENT

        return symmetry_factor * mag_factor * disp_factor

    def rs_resonance_mismatch(self, amplitudes: np.ndarray, frequency: float,
                               phases: np.ndarray) -> float:
        """
        Compute how far the current coil parameters are from this material's
        RS-optimal configuration. Returns 0.0 for perfect match, higher for worse.

        This is the key metric: lower mismatch → better coupling.
        """
        # Amplitude ratio mismatch
        optimal_ratio = self.rs_amplitude_ratio
        if np.max(amplitudes) > 0.01:
            actual_ratio = np.abs(amplitudes) / np.max(np.abs(amplitudes))
        else:
            actual_ratio = np.zeros(3)
        amp_mismatch = np.linalg.norm(actual_ratio - optimal_ratio) / np.sqrt(3)

        # Frequency mismatch (log scale — octave distance)
        opt_freq = self.rs_optimal_frequency
        if frequency > 0.01 and opt_freq > 0.01:
            freq_mismatch = abs(np.log2(frequency / opt_freq))
        else:
            freq_mismatch = 5.0  # Large mismatch

        # Phase mismatch
        opt_phase = self.rs_phase_offsets
        phase_diff = np.abs(phases - opt_phase)
        # Wrap to [-π, π]
        phase_diff = np.minimum(phase_diff, 2*np.pi - phase_diff)
        phase_mismatch = np.linalg.norm(phase_diff) / np.pi

        # Weighted combination
        return 0.4 * amp_mismatch + 0.35 * freq_mismatch + 0.25 * phase_mismatch


# === Material Database ===
# RS displacement values from Larson's periodic table
# Format: rs_magnetic=(m1, m2), rs_electric=e
# Reference: "Nothing But Motion" (1979), "The Structure of the Physical Universe" (1959)

LEAD = Material(
    name="Lead", symbol="Pb",
    density=11340.0,
    conductivity=4.81e6,
    susceptibility=-1.8e-5,
    viscosity=0.0,
    color=(120, 125, 140),
    rs_magnetic=(4, 4), rs_electric=1,  # Period 6, Group 14 (IVA)
)

ALUMINUM = Material(
    name="Aluminum", symbol="Al",
    density=2700.0,
    conductivity=3.77e7,
    susceptibility=2.2e-5,
    viscosity=0.0,
    color=(200, 210, 220),
    rs_magnetic=(2, 2), rs_electric=3,  # Period 3, Group 13 (IIIA)
)

COPPER = Material(
    name="Copper", symbol="Cu",
    density=8960.0,
    conductivity=5.96e7,
    susceptibility=-9.6e-6,
    viscosity=0.0,
    color=(200, 130, 80),
    rs_magnetic=(3, 3), rs_electric=1,  # Period 4, Group 11 (IB)
)

IRON = Material(
    name="Iron", symbol="Fe",
    density=7874.0,
    conductivity=1.0e7,
    susceptibility=200000.0,
    viscosity=0.0,
    color=(160, 160, 165),
    rs_magnetic=(3, 3), rs_electric=6,  # Period 4, Group 8 (VIII)
)

BISMUTH = Material(
    name="Bismuth", symbol="Bi",
    density=9780.0,
    conductivity=7.7e5,
    susceptibility=-1.66e-4,
    viscosity=0.0,
    color=(180, 170, 190),
    rs_magnetic=(4, 4), rs_electric=3,  # Period 6, Group 15 (VA)
)

MERCURY = Material(
    name="Mercury", symbol="Hg",
    density=13534.0,
    conductivity=1.04e6,
    susceptibility=-2.9e-5,
    viscosity=1.526e-3,
    color=(180, 195, 210),
    rs_magnetic=(4, 4), rs_electric=2,  # Period 6, Group 12 (IIB)
)

# === Additional elements for broader periodic table coverage ===

GOLD = Material(
    name="Gold", symbol="Au",
    density=19300.0,
    conductivity=4.1e7,
    susceptibility=-3.4e-5,
    viscosity=0.0,
    color=(218, 185, 82),
    rs_magnetic=(4, 4), rs_electric=1,  # Period 6, Group 11 (IB) — same displacement as Pb!
)

SILVER = Material(
    name="Silver", symbol="Ag",
    density=10490.0,
    conductivity=6.3e7,
    susceptibility=-2.4e-5,
    viscosity=0.0,
    color=(192, 192, 200),
    rs_magnetic=(3, 3), rs_electric=1,  # Period 5, Group 11 (IB) — same as Cu pattern
)

TIN = Material(
    name="Tin", symbol="Sn",
    density=7265.0,
    conductivity=9.17e6,
    susceptibility=-2.4e-5,
    viscosity=0.0,
    color=(170, 175, 180),
    rs_magnetic=(3, 3), rs_electric=4,  # Period 5, Group 14 (IVA)
)

ZINC = Material(
    name="Zinc", symbol="Zn",
    density=7134.0,
    conductivity=1.69e7,
    susceptibility=-1.6e-5,
    viscosity=0.0,
    color=(160, 170, 185),
    rs_magnetic=(3, 3), rs_electric=2,  # Period 4, Group 12 (IIB)
)

TUNGSTEN = Material(
    name="Tungsten", symbol="W",
    density=19250.0,
    conductivity=1.79e7,
    susceptibility=6.8e-5,
    viscosity=0.0,
    color=(140, 145, 155),
    rs_magnetic=(4, 4), rs_electric=6,  # Period 6, Group 6 (VIB)
)

TITANIUM = Material(
    name="Titanium", symbol="Ti",
    density=4507.0,
    conductivity=2.38e6,
    susceptibility=1.8e-4,
    viscosity=0.0,
    color=(160, 170, 175),
    rs_magnetic=(3, 3), rs_electric=4,  # Period 4, Group 4 (IVB)
)

THORIUM = Material(
    name="Thorium", symbol="Th",
    density=11724.0,
    conductivity=6.67e6,
    susceptibility=8.4e-5,
    viscosity=0.0,
    color=(160, 155, 140),
    rs_magnetic=(4, 4), rs_electric=4,  # Period 7 actinide, total displacement 12
)

YBCO = Material(
    name="YBCO", symbol="YBCO",
    density=6300.0,
    conductivity=1e12,
    susceptibility=-1.0,
    viscosity=0.0,
    color=(40, 40, 50),
    rs_magnetic=(0, 0), rs_electric=0,  # Compound — RS TBD
)

# Core materials for the simulator (cycleable with M key)
CORE_MATERIALS = [LEAD, ALUMINUM, COPPER, IRON, BISMUTH, GOLD, SILVER, TIN, THORIUM]
FLUID_MATERIAL = MERCURY

# Full database for RS analysis
ALL_MATERIALS = [
    LEAD, ALUMINUM, COPPER, IRON, BISMUTH, MERCURY,
    GOLD, SILVER, TIN, ZINC, TUNGSTEN, TITANIUM, THORIUM,
]


class HgIon:
    """Mercury ion (Hg⁺) properties for PIC plasma simulation."""
    mass = 200.59 * 1.6605e-27      # kg (200.59 amu)
    charge = 1.602e-19               # C (singly ionized)
    qm = charge / mass               # charge-to-mass ratio ≈ 4.81e5 rad/s/T

    @staticmethod
    def cyclotron_freq(B_mag):
        """Cyclotron frequency f_c = qB / (2π m) in Hz."""
        return HgIon.qm * B_mag / (2.0 * np.pi)

    @staticmethod
    def cyclotron_radius(v_perp, B_mag):
        """Larmor radius r_c = m v_perp / (q B) in meters."""
        if B_mag < 1e-20:
            return np.inf
        return HgIon.mass * v_perp / (HgIon.charge * B_mag)


def get_buoyancy_force(core: Material, fluid: Material, core_volume: float) -> np.ndarray:
    """Compute buoyancy force on core in fluid. Returns force vector (upward = +y)."""
    delta_rho = fluid.density - core.density
    force_magnitude = delta_rho * core_volume * 9.81
    return np.array([0.0, force_magnitude, 0.0])


def core_volume(radius: float) -> float:
    """Volume of spherical core."""
    return (4.0 / 3.0) * np.pi * radius**3


def core_mass(material: Material, radius: float) -> float:
    """Mass of spherical core."""
    return material.density * core_volume(radius)


def print_rs_table():
    """Print the RS displacement table for all materials."""
    print(f"{'Element':10s} {'Sym':4s} {'m1':>3s} {'m2':>3s} {'e':>3s} {'tot':>4s} "
          f"{'amp_ratio':>14s} {'freq_Hz':>8s} {'phase_deg':>16s} {'coupling':>8s}")
    print("-" * 90)
    for mat in ALL_MATERIALS:
        r = mat.rs_amplitude_ratio
        p = np.degrees(mat.rs_phase_offsets)
        print(f"{mat.name:10s} {mat.symbol:4s} {mat.rs_magnetic[0]:3d} {mat.rs_magnetic[1]:3d} "
              f"{mat.rs_electric:3d} {mat.rs_total_displacement:4d} "
              f"[{r[0]:.2f},{r[1]:.2f},{r[2]:.2f}] "
              f"{mat.rs_optimal_frequency:8.1f} "
              f"[{p[0]:5.1f},{p[1]:5.1f},{p[2]:5.1f}] "
              f"{mat.rs_coupling_factor:8.3f}")


if __name__ == "__main__":
    print("=" * 90)
    print("  RS Periodic Table — Displacement-to-Coil Mapping")
    print("=" * 90)
    print()
    print_rs_table()
    print()

    print("Mapping: Coil X ↔ m1 (mag primary), Coil Y ↔ m2 (mag secondary), Coil Z ↔ e (electric)")
    print(f"Base frequency: {RS_BASE_FREQ} Hz, Reference displacement: {RS_REF_DISPLACEMENT} (Hg)")
    print()

    # Show predictions
    print("RS Predictions for optimal configurations:")
    print("-" * 70)
    for mat in CORE_MATERIALS:
        r = mat.rs_amplitude_ratio
        f = mat.rs_optimal_frequency
        p = np.degrees(mat.rs_phase_offsets)
        print(f"  {mat.symbol:4s}: amps=[{r[0]:.2f}, {r[1]:.2f}, {r[2]:.2f}]  "
              f"freq={f:.1f}Hz  phase=[{p[0]:.0f}, {p[1]:.0f}, {p[2]:.0f}]deg  "
              f"coupling={mat.rs_coupling_factor:.3f}")

    # Show resonance mismatch example
    print()
    print("Mismatch when using EQUAL amplitudes [1,1,1] at 60Hz:")
    equal_amps = np.array([1.0, 1.0, 1.0])
    equal_phases = np.array([0.0, 0.0, 0.0])
    for mat in CORE_MATERIALS:
        mm = mat.rs_resonance_mismatch(equal_amps, 60.0, equal_phases)
        print(f"  {mat.symbol:4s}: mismatch = {mm:.3f}")
