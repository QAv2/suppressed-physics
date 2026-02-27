"""Core dynamics — forces and motion of the solid core sample in the EM field.

AUDIT NOTE (2026-02-22): This module contains two RS-theory mechanisms that
bias results if enabled. Both are now DISABLED by default (safe-by-default):

  1. rs_resonance_boost — sigmoid that rewards RS-predicted freq/amp/phase
     with up to 2x force multiplier. Caused circular "validation" in exp 6,7,10.
     Controlled by: CoreState.disable_rs_boost (default True)

  2. rs_coupling_factor — material-dependent multiplier derived from RS
     displacement values. Biases cross-material comparisons. Had NO disable
     flag prior to this audit.
     Controlled by: CoreState.disable_rs_coupling (default True)

  To re-enable for RS hypothesis testing, set both flags to False explicitly.

The core has two states:

DORMANT: Coils off. Only buoyancy acts. Core floats (if lighter than Hg) or sinks.

COUPLED: After EM pulse forces Cooper pairing, the core becomes magnetically active.
  The mechanism: pulse → forced Cooper pairing → superconductor-like state →
  Meissner effect + flux pinning → core locks to the field geometry center.
  NOTE: Room-temperature Cooper pairing is a HYPOTHESIS, not established physics.

  This is modeled as:
  1. Flux pinning force: strong spring toward the combined field's locus point
     (proportional to B² at center — stronger field = stiffer lock)
  2. Buoyancy (still present — mercury still has density)
  3. Viscous drag from mercury
  4. The flux pinning OVERWHELMS buoyancy at sufficient field strength

  The coupling strength ramps up during the pulse and is maintained as long
  as the field stays above the decoupling threshold.

Forces in coupled state:
  F_pinning  = -k_pin * (pos - center) * |B_center|²   (toward center)
  F_buoyancy = (ρ_Hg - ρ_core) * V * g                 (Archimedes net)
  F_drag     = -6πηRv                                   (Stokes drag)
"""

import numpy as np
from physics.fields import total_field, field_gradient
from physics.materials import Material, MERCURY, core_volume, core_mass
from config import MU_0, G, SPHERE_RADIUS, CORE_RADIUS


# Coupling state
STATE_DORMANT = 0
STATE_COUPLING = 1
STATE_COUPLED = 2
STATE_DECOUPLING = 3


class CoreState:
    """State of the solid core sample."""

    def __init__(self, material: Material):
        self.material = material
        self.radius = CORE_RADIUS
        self.volume = core_volume(self.radius)
        self.mass = core_mass(material, self.radius)

        # Start at top of sphere (Pb floats in Hg) or bottom (denser than Hg)
        buoyant = material.density < MERCURY.density
        y_start = (SPHERE_RADIUS - self.radius - 0.002) * (1.0 if buoyant else -1.0)
        self.pos = np.array([0.0, y_start, 0.0])
        self.vel = np.zeros(3)

        # Coupling state machine
        self.state = STATE_DORMANT
        self.coupling_strength = 0.0   # 0 = no coupling, 1 = fully coupled
        self.coupling_rate = 3.0       # Base rate — modified by RS resonance match
        self.decoupling_rate = 0.5     # How fast coupling decays without field

        # Flux pinning spring constant (N/m per T²)
        self.k_pin_base = 500.0

        # RS resonance state
        self.rs_mismatch = 1.0         # How far from RS-optimal (0=perfect, higher=worse)
        self.rs_resonance_boost = 1.0  # Multiplier from RS tuning (1.0 = no effect)
        self.disable_rs_boost = True   # DEFAULT ON: neutralizes rs_resonance_boost to 1.0
        self.disable_rs_coupling = True  # DEFAULT ON: neutralizes rs_coupling_factor to 1.0

        # Force tracking (for UI display)
        self.f_magnetic = np.zeros(3)
        self.f_buoyancy = np.zeros(3)
        self.f_drag = np.zeros(3)
        self.f_total = np.zeros(3)
        self.B_at_core = np.zeros(3)
        self.state_name = "DORMANT"

    def set_material(self, material: Material):
        """Switch core material, reset position."""
        self.material = material
        self.mass = core_mass(material, self.radius)
        buoyant = material.density < MERCURY.density
        y_start = (SPHERE_RADIUS - self.radius - 0.002) * (1.0 if buoyant else -1.0)
        self.pos = np.array([0.0, y_start, 0.0])
        self.vel = np.zeros(3)
        self.state = STATE_DORMANT
        self.coupling_strength = 0.0

    def begin_coupling(self):
        """Trigger the pulse — start transitioning to coupled state."""
        if self.state == STATE_DORMANT or self.state == STATE_DECOUPLING:
            self.state = STATE_COUPLING

    def compute_forces(self, amplitudes: np.ndarray, dt: float,
                       frequency: float = 60.0,
                       phases: np.ndarray = None) -> np.ndarray:
        """Compute all forces on the core. Returns total force vector.

        Now includes RS resonance: when coil parameters match the material's
        RS-predicted optimal configuration, coupling is faster and stronger.
        """
        mat = self.material
        if phases is None:
            phases = np.zeros(3)

        # B field at core position and at center
        self.B_at_core = total_field(self.pos, amplitudes)
        B_center = total_field(np.zeros(3), amplitudes)
        B_center_mag2 = np.dot(B_center, B_center)

        # === RS resonance computation ===
        self.rs_mismatch = mat.rs_resonance_mismatch(amplitudes, frequency, phases)
        if self.disable_rs_boost:
            self.rs_resonance_boost = 1.0  # Neutral — no frequency preference
        else:
            # Resonance boost: perfect match → 2x, bad match → 0.5x
            # Uses sigmoid-like curve centered on mismatch=0.5
            self.rs_resonance_boost = 0.5 + 1.5 / (1.0 + np.exp(3.0 * (self.rs_mismatch - 0.3)))

        # === Update coupling state ===
        has_field = B_center_mag2 > 1e-6

        # Coupling rate is modified by RS resonance and material coupling factor
        # NOTE: Both RS mechanisms are disabled by default (safe-by-default).
        # rs_coupling_factor is derived entirely from RS displacement values —
        # it biases cross-material comparisons if enabled. See audit 2026-02-22.
        rs_cf = 1.0 if self.disable_rs_coupling else mat.rs_coupling_factor
        effective_coupling_rate = (self.coupling_rate
                                   * self.rs_resonance_boost
                                   * rs_cf)

        if self.state == STATE_COUPLING:
            self.coupling_strength = min(1.0, self.coupling_strength + effective_coupling_rate * dt)
            if self.coupling_strength >= 1.0:
                self.state = STATE_COUPLED
        elif self.state == STATE_COUPLED:
            if not has_field:
                self.state = STATE_DECOUPLING
        elif self.state == STATE_DECOUPLING:
            self.coupling_strength = max(0.0, self.coupling_strength - self.decoupling_rate * dt)
            if self.coupling_strength <= 0.0:
                self.state = STATE_DORMANT
            elif has_field:
                self.state = STATE_COUPLING

        state_names = {STATE_DORMANT: "DORMANT", STATE_COUPLING: "COUPLING",
                       STATE_COUPLED: "COUPLED", STATE_DECOUPLING: "DECOUPLING"}
        self.state_name = state_names[self.state]

        # === 1. Flux pinning / magnetic centering force ===
        if self.coupling_strength > 0 and B_center_mag2 > 1e-8:
            # Pinning force: spring toward center, proportional to B² and coupling
            k_eff = self.k_pin_base * self.coupling_strength * B_center_mag2

            # Material factor: conductivity baseline
            sigma_norm = np.log10(max(mat.conductivity, 1.0)) / 7.0
            material_factor = 0.5 + 0.5 * sigma_norm

            # RS resonance boost: tuned coils → stronger pinning
            # This is the key RS prediction: the right configuration
            # produces qualitatively better coupling
            material_factor *= self.rs_resonance_boost

            self.f_magnetic = -k_eff * material_factor * self.pos
        else:
            # Dormant: only weak diamagnetic/paramagnetic force
            grad_B2 = field_gradient(self.pos, amplitudes)
            self.f_magnetic = (mat.susceptibility * self.volume / MU_0) * grad_B2
            # Cap ferromagnetic
            if abs(mat.susceptibility) > 1000:
                mag = np.linalg.norm(self.f_magnetic)
                if mag > 10.0:
                    self.f_magnetic = self.f_magnetic * 10.0 / mag

        # === 2. Buoyancy (Archimedes net force) ===
        # This IS the net of buoyancy - gravity: (ρ_fluid - ρ_core) * V * g
        delta_rho = MERCURY.density - mat.density
        self.f_buoyancy = np.array([0.0, delta_rho * self.volume * G, 0.0])

        # === 3. Viscous drag (Stokes) ===
        eta = MERCURY.viscosity
        self.f_drag = -6.0 * np.pi * eta * self.radius * self.vel

        # Add effective mass drag (mercury must move out of the way)
        # Added mass for sphere in fluid = 0.5 * ρ_fluid * V
        added_mass_coeff = 0.5 * MERCURY.density * self.volume
        # This acts as extra drag at higher velocities
        speed = np.linalg.norm(self.vel)
        if speed > 1e-6:
            f_added = -added_mass_coeff * 20.0 * self.vel  # Effective damping
            self.f_drag += f_added

        self.f_total = self.f_magnetic + self.f_buoyancy + self.f_drag
        return self.f_total

    def step(self, amplitudes: np.ndarray, dt: float,
             frequency: float = 60.0, phases: np.ndarray = None):
        """Advance core state by one timestep using symplectic Euler."""
        self.compute_forces(amplitudes, dt, frequency, phases)
        a = self.f_total / self.mass
        self.vel += a * dt
        self.pos += self.vel * dt
        self._enforce_boundary()

    def _enforce_boundary(self):
        """Keep core inside the ceramic sphere."""
        max_r = SPHERE_RADIUS - self.radius - 0.001
        r = np.linalg.norm(self.pos)
        if r > max_r:
            self.pos = self.pos * (max_r / r)
            radial = self.pos / r
            radial_vel = np.dot(self.vel, radial)
            if radial_vel > 0:
                self.vel -= radial_vel * radial
                self.vel *= 0.3  # Energy loss on wall collision
