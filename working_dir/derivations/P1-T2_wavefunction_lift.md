---
generated_by: prism-theoretician
generated_at: 2026-04-17T00:01:00Z
spec_task_id: P1-T2
revision: 1
depends_on:
  - working_dir/derivations/prism_formal_spec.md
  - working_dir/kip_madden_prism_notes.md
  - working_dir/knowledge_base/literature_values.yaml
derivation_metadata:
  starting_postulates: [P-1, P-2, P-3, P-4, P-5, P-6]
  introduced_postulates: []
  one_step_per_turn: true
  current_step: 1
  steps_completed: [Step-1A, Step-1B, Step-1C, Step-1D]
  steps_remaining: [Step-2-evaluate-projection-integral, Step-3-verify-normalization-and-4D-limit]
  choice_points:
    - id: CP-1
      description: >
        m=0 restriction: the full wavefunction sum includes m=-ell..+ell, but
        because the log-spiral embedding (P-2) lies in the (x,y) plane and the
        χ-θ coupling (P-4) is azimuthally symmetric in the embedding, integrating
        out χ over [0, L_χ] commutes with the azimuthal rotation. As a result,
        matrix elements of the χ-derivative Hamiltonian term (the one driving
        ΔE_nS) are identical for all m at fixed (n, ell). It is therefore
        sufficient to compute at m=0 and note the (2ell+1) degeneracy factor
        separately. This is a symmetry argument, not an ansatz.
      structural: false
      decision: work at m=0; note degeneracy multiplicity separately when needed
      reasoning: P-2 (planar spiral) implies azimuthal symmetry of the χ-integral; does not affect functional form of Delta_E_nS
    - id: CP-2
      description: >
        Delta-function localization for f(chi, theta): the P-4 postulate states
        chi(theta) = theta mod L_chi, which is a deterministic map — for a given
        spiral parameter theta, chi is exactly theta mod L_chi, with no spread.
        The natural measure on the 5D worldline density is therefore a delta
        function localizing Psi_5D onto the worldline. The alternative — a smooth
        distribution in chi at fixed theta (e.g., a Gaussian of width sigma_chi) —
        would require specifying sigma_chi as an additional parameter beyond
        P-1..P-6, which is prohibited. Delta-function localization is the unique
        choice consistent with the postulate set without introducing a free parameter.
        This choice does not introduce a free parameter; it is the minimal
        interpretation of P-4.
      structural: false
      decision: use delta(chi - theta(r) mod L_chi) as the chi-coupling factor
      reasoning: >
        Dimensional check: integrating delta(chi - theta mod L_chi) over chi in
        [0, L_chi] gives 1 (dimensionless), so the lifted Psi_5D has the same
        dimensions as psi_4D times a length^{-1/2} normalization from the
        chi-space measure. N_lift absorbs this. Does not affect functional form
        of Delta_E_nS because the delta function will be used to perform the
        chi-integral analytically in Step 2, leaving behind a function of
        theta(r) only. The resulting integrand for Delta_E_nS is determined by
        the chi-derivative of the phase factor exp(i*n_w*chi) at chi=theta(r),
        which is the same regardless of sigma_chi -> 0 regularization path.
  flags: []
  t_theta_assumption: >
    t proportional to theta (non-relativistic Schrodinger limit). For
    non-relativistic hydrogen, proper-time parameterization t(theta) is taken
    as linear in theta. This recovers the Schrodinger equation as the effective
    4D dynamics in the projected theory. This is a documented assumed limit
    (noted as a known open item in kip_madden_prism_notes.md §6 and
    prism_formal_spec.md §10.3 item 1); it is not derived from P-1..P-6. It
    will be checked in P1-T3 when the lifted Hamiltonian is written down. If
    linearity fails to recover the Schrodinger equation, that step will HALT.
review_status: PENDING
verdict: STEP_COMPLETE_PENDING_REVIEW
---

# P1-T2 — Wavefunction Lift: Derivation Document (Step 1 of 3)

**Task:** P1-T2 — Derive orbital wavefunction in 5D spiral basis
**Agent:** prism-theoretician
**Date:** 2026-04-17
**Revision:** 1 (first step; subsequent steps will increment)
**Status:** STEP_COMPLETE_PENDING_REVIEW — Kip Madden must review Step 1 before Step 2 is dispatched (per spec §11 theoretician human-in-the-loop requirement; CP2 gate fires formally after P1-T3, but each step is reviewed before the next is dispatched).

---

## 0. Scope of this document

This document records Step 1 of the 5D wavefunction lift. Step 1 has four
sub-parts (1A through 1D). Steps 2 and 3 will be written in subsequent
/prism-next dispatches.

**Step 1** (this document): Write canonical psi_nlm, re-express in spiral
coordinates, attach chi, define the projection operator (un-evaluated).

**Step 2** (next dispatch): Evaluate the projection integral to confirm that
integrating out chi recovers psi_nlm in the 4D limit (the "4D reduction" check).

**Step 3** (next dispatch or the one after): Verify angular momentum quantization
emerges from compactification topology (P1-T2 success criterion per spec §8).

Binding constraints from the orchestrator (reproduced for this agent's record):
- Use only P-1 through P-6. Any new postulate triggers HALT.
- phi (golden ratio ~1.618) must NOT appear. phi_az (azimuthal angle) is a
  different symbol; no confusion risk if notation is careful.
- Structural CHOICE points trigger HALT for CP2 review.
- t ∝ theta assumed for NR limit; documented, not derived.
- One step per turn; stop after Step 1D.

---

## Step 1A — Canonical hydrogen wavefunction psi_nlm(r, theta_pol, phi_az)

**Source:** Griffiths, D.J., *Introduction to Quantum Mechanics*, 3rd ed.,
Cambridge University Press (2018), eq. 4.73 (radial) and eq. 4.32 (full
product form). Also: Bethe & Salpeter, *Quantum Mechanics of One- and
Two-Electron Atoms*, Springer (1977), §2 — used for the normalized Laguerre
form cited below. No re-derivation from the Schrodinger equation is performed
here; the eigenfunctions are taken as established results.

The hydrogen atom Hamiltonian in 4D (3+1 Minkowski, non-relativistic limit) is:

    H_4D = -hbar^2/(2 m_e) * nabla^2 - e^2/(4 pi eps_0 r)

with eigenfunctions (Griffiths eq. 4.73):

    psi_nlm(r, theta_pol, phi_az) = R_nl(r) * Y_l^m(theta_pol, phi_az)

where:

### Radial eigenfunction R_nl(r)

The normalized radial wavefunction is (Griffiths eq. 4.73):

    R_nl(r) = sqrt( (2/(n a_0))^3 * (n-l-1)! / (2n [(n+l)!]^3) )
              * exp(-r / (n a_0))
              * (2r / (n a_0))^l
              * L_{n-l-1}^{2l+1}(2r / (n a_0))

where:
- a_0 = 4 pi eps_0 hbar^2 / (m_e e^2) is the Bohr radius
  (CODATA 2022: a_0 ≈ 5.29177210544 × 10^{-11} m)
- L_p^q(x) is the associated Laguerre polynomial of degree p = n-l-1 and
  order q = 2l+1
- n ∈ {1, 2, 3, ...}, l ∈ {0, 1, ..., n-1}

Normalization convention:

    ∫_0^∞ [R_nl(r)]^2 r^2 dr = 1

### Spherical harmonics Y_l^m(theta_pol, phi_az)

The spherical harmonics are the standard ones (Griffiths eq. 4.32):

    Y_l^m(theta_pol, phi_az) = eps * sqrt( (2l+1)/(4 pi) * (l-|m|)!/(l+|m|)! )
                                * P_l^|m|(cos theta_pol) * exp(i m phi_az)

where:
- eps = (-1)^m for m >= 0, eps = 1 for m < 0 (Condon-Shortley phase)
- P_l^|m| are the associated Legendre polynomials
- Normalization: ∫ [Y_l^m]* Y_l^m sin(theta_pol) d(theta_pol) d(phi_az) = 1

The full product normalization satisfies:

    ∫_0^∞ ∫_0^pi ∫_0^{2pi} |psi_nlm|^2 r^2 sin(theta_pol) dr d(theta_pol) d(phi_az) = 1

**[[CHOICE]] CP-1 — m = 0 restriction:**
For the purpose of this derivation, we work at m = 0. The azimuthal integral
over phi_az of the Jacobian factor (from P-6, which does not depend on phi_az
because the log-spiral lies in the (x,y) plane by P-2) factorizes. The
chi-derivative term in the lifted Hamiltonian is azimuthally symmetric by the
same argument. Therefore all m modes contribute the same matrix element, and
the degeneracy factor (2l+1) appears separately as a multiplicative prefactor
that does not affect the functional form of Delta_E_nS. This is a symmetry
consequence of P-2 (planar spiral), not an ansatz.

Decision (CP-1, non-structural): proceed at m = 0. Denote psi_nl ≡ psi_{nl,m=0}.

---

## Step 1B — Radial wavefunction in spiral coordinate theta

From postulates P-2 and P-3, the radial distance from the nucleus is:

    r = r_0 * exp(alpha * theta)           [Embedding map, prism_formal_spec.md §4.1]

Inverting:

    theta(r) = (1/alpha) * ln(r / r_0)    [prism_formal_spec.md §4.2, eq. for inverse]

This is defined for r > r_0 (the spiral starts at the reference radius r_0). For
r < r_0, theta < 0, which is physically the inner winding of the spiral — still
geometrically valid since the log-spiral extends to r → 0 as theta → -∞.

**Notation:** We write theta for the spiral parameter. For clarity in the lifted
wavefunction, we will write theta(r) when r is the independent variable (4D
perspective) and simply theta when the spiral parameter is primary (5D perspective).

Substituting r → r_0 * exp(alpha * theta) in R_nl(r):

    R_nl^(spiral)(theta) := R_nl(r_0 * exp(alpha * theta))

Concretely, the substitution maps:

    r          →   r_0 * exp(alpha * theta)
    r^l        →   r_0^l * exp(alpha * l * theta)
    exp(-r/(n a_0))  →   exp(-r_0 * exp(alpha * theta) / (n a_0))
    2r/(n a_0) →   2 r_0 * exp(alpha * theta) / (n a_0)
    L_{n-l-1}^{2l+1}(2r/(n a_0))  →  L_{n-l-1}^{2l+1}(2 r_0 exp(alpha theta) / (n a_0))

So the full spiral-coordinate radial function is:

    R_nl^(spiral)(theta) = C_nl
                           * exp(alpha * l * theta)
                           * exp(-r_0 * exp(alpha * theta) / (n a_0))
                           * L_{n-l-1}^{2l+1}(2 r_0 * exp(alpha * theta) / (n a_0))

where C_nl collects the normalization prefactor from Step 1A:

    C_nl = sqrt( (2/(n a_0))^3 * (n-l-1)! / (2n [(n+l)!]^3) ) * r_0^l * (2 r_0 / (n a_0))^l

This can be simplified to:

    C_nl = sqrt( (2/(n a_0))^3 * (n-l-1)! / (2n [(n+l)!]^3) ) * (2 r_0^{l+1} / (n a_0))^l

Note: r_0 is the spiral reference radius. Its relationship to the Bohr radius
a_0 has not yet been fixed by P-1..P-6. Setting r_0 = a_0/2 (or some fixed
multiple of a_0) is a candidate normalization choice, but fixing it is not
required for the functional form of the lift — r_0 enters as a scale factor.
This is a deferred but non-structural choice (it scales the wavefunction
normalization, not the n-dependence of Delta_E_nS). Record as a note, not a
formal CHOICE point: r_0 will be fixed when computing absolute values in P1-T4.

**Angular parts:** The spherical harmonics Y_l^m(theta_pol, phi_az) depend only
on solid-angle coordinates (theta_pol, phi_az), not on r. They are unchanged by
the r → theta(r) reparameterization:

    Y_l^m(theta_pol, phi_az)  [unchanged; theta_pol and phi_az are independent]

The 4D wavefunction in spiral coordinates (at m = 0) is therefore:

    psi_nl(theta, theta_pol) = R_nl^(spiral)(theta) * Y_l^0(theta_pol)

where theta = theta(r) = (1/alpha) * ln(r/r_0).

---

## Step 1C — Attach chi to produce the 5D wavefunction Psi_nlm^(5D)

### Physical motivation from P-6

Postulate P-6 states: "The 4D-observed wavefunction is the projection of the 5D
worldline density onto 4D Cartesian coordinates." This means the physical object
is Psi_5D defined on M5, and psi_4D is its shadow in 4D.

Postulate P-4 states: chi(theta) = theta mod L_chi. For a given spiral parameter
theta, the compact coordinate chi is exactly theta mod L_chi — there is no
probability distribution in chi at fixed theta; chi is determined by theta. The
5D worldline is a 1-dimensional object (parameterized by theta), and its density
on M5 is localized to that worldline.

### Form of the chi-coupling factor f(chi, theta)

**[[CHOICE]] CP-2 — Delta-function localization (non-structural):**

The chi-coupling factor must satisfy: given theta, chi = theta mod L_chi exactly.
The unique probability density on chi at fixed theta that implements a deterministic
map without introducing a free parameter is:

    f(chi, theta) = delta(chi - (theta mod L_chi))

Alternatives:
- Smooth distribution: f(chi, theta) = (1/sigma_chi) * G((chi - theta mod L_chi)/sigma_chi)
  for some width sigma_chi. This requires sigma_chi as a free parameter beyond P-1..P-6.
  REJECTED: violates the no-new-parameter rule.
- Flat distribution: f(chi, theta) = 1/L_chi (constant in chi for all theta).
  This would mean the electron simultaneously occupies all chi values at each
  theta — incompatible with the deterministic coupling chi = theta mod L_chi
  stated in P-4. REJECTED.

The delta-function is the unique choice. Decision (CP-2, non-structural): proceed
with delta(chi - theta(r) mod L_chi).

**Structural assessment:** This choice does not affect the functional form of
Delta_E_nS. When the projection integral is evaluated in Step 2, the delta
function performs the chi-integral analytically, setting chi = theta(r) in any
integrand. The resulting expression for the chi-derivative Hamiltonian term
(Step 3 / P1-T3) depends on d/dchi of the wavefunction evaluated at chi = theta(r),
which is the same regardless of the width of the chi-distribution in the limit
where that width goes to zero. This is not a load-bearing structural choice.

### The 5D wavefunction

Assembling Steps 1A, 1B, and the above:

    Psi_nl(r, theta_pol, phi_az, chi) =
        N_lift
        * R_nl^(spiral)(theta(r))
        * Y_l^0(theta_pol)
        * delta(chi - theta(r) mod L_chi)

where:
- theta(r) = (1/alpha) * ln(r/r_0) [from P-2, P-3]
- R_nl^(spiral)(theta) is defined in Step 1B above
- Y_l^0(theta_pol) is the standard spherical harmonic at m = 0
- delta(chi - theta(r) mod L_chi) is the P-4 localization factor
- N_lift is a normalization constant, to be determined in Step 2 by requiring
  that the projection integral recovers the correctly normalized psi_nl

**Note on phi_az:** At m = 0, Y_l^0 does not depend on phi_az. The lifted
wavefunction Psi_nl also does not depend on phi_az at m = 0. For m ≠ 0, the
phi_az dependence enters through Y_l^m as usual, unchanged by the lift.

**Note on postulates used:**
- P-2: r = r_0 exp(alpha theta) — used in the r → theta substitution
- P-3: k = alpha — used to identify the growth rate with alpha
- P-4: chi(theta) = theta mod L_chi — used to choose f(chi, theta)
- P-5: L_chi = 2 pi / alpha — defines the chi integration domain [0, L_chi)
- P-6: 4D wavefunction = projection of 5D density — motivates the structure
- P-1: 5D spacetime with compact chi — provides the domain for chi

**NEW_POSTULATE_REQUIRED check:** No new postulate was required for this step.
introduced_postulates remains empty.

**GOLDEN_RATIO_ALERT check:** The symbols appearing in this step are alpha, r_0,
a_0, n, l, m, theta, theta_pol, phi_az, chi, L_chi, R_nl, Y_l^m, C_nl, N_lift,
L_{n-l-1}^{2l+1} (Laguerre polynomial label), P_l^|m| (Legendre polynomial
label). None of these is the golden ratio (~1.618). No alert raised.

---

## Step 1D — Projection operator definition (un-evaluated)

The projection operator P: L^2(M5) → L^2(R^3) must recover psi_nl from Psi_5D.
Per P-6, the 4D wavefunction is the projection of the 5D density with the
Jacobian weight J.

The measure on M5 for the spiral coordinate system is:

    d(vol_M5) = J(theta, theta_pol) * d(theta) * d(theta_pol) * d(phi_az) * d(chi)

where J(theta, theta_pol) = alpha * r_0^3 * exp(3 alpha theta) * sin(theta_pol)
is the Jacobian from prism_formal_spec.md §4.2 (derived from P-2, P-3, P-4; see
also Appendix of that document for the calculation).

To project out chi (integrate over the compact dimension), the projection is:

    psi_nl(r, theta_pol) = (P * Psi_nl)(r, theta_pol)
                         = ∫_0^{L_chi} Psi_nl(r, theta_pol, phi_az=0, chi)
                           * J(theta(r), theta_pol)^{-1}
                           d(chi)   [at fixed r, theta_pol; phi_az=0 for m=0]

Substituting the form of Psi_nl from Step 1C:

    = ∫_0^{L_chi}
        N_lift
        * R_nl^(spiral)(theta(r))
        * Y_l^0(theta_pol)
        * delta(chi - theta(r) mod L_chi)
        * J(theta(r), theta_pol)^{-1}
        d(chi)

The integral over chi of delta(chi - theta(r) mod L_chi) over [0, L_chi) equals 1
(the delta function's argument hits exactly once in the interval [0, L_chi)
because theta mod L_chi is by definition in [0, L_chi)). Therefore:

    = N_lift
      * R_nl^(spiral)(theta(r))
      * Y_l^0(theta_pol)
      * J(theta(r), theta_pol)^{-1}
      * 1

This should equal psi_nl(r, theta_pol) = R_nl(r) * Y_l^0(theta_pol).

**Dimensional consistency check:**
- Psi_nl has dimensions [length]^{-3/2} * [chi]^{-1} = [length]^{-3/2} * [length]^{-1}
  if chi has dimensions of length. But chi is dimensionless (it is an angle in
  radians, same as theta which parameterizes the log-spiral by angle). So the
  delta function delta(chi - theta mod L_chi) has units [dimensionless]^{-1} =
  dimensionless (the argument is dimensionless; the delta function of a
  dimensionless variable has dimensions [1/(units of variable)] = 1).
  Therefore: Psi_nl has dimensions [length]^{-3/2} if N_lift is dimensionless.
- J(theta, theta_pol)^{-1} has dimensions 1/[alpha * r_0^3 * exp(3 alpha theta) * sin(theta_pol)]
  = [length]^{-3} * [dimensionless]^{-1} → has dimensions [length]^{-3} (since
  alpha is dimensionless and the exponential factor is dimensionless).
- The product Psi_nl * J^{-1} has dimensions [length]^{-3/2} * [length]^{-3}
  = [length]^{-9/2}. But we need psi_nl ~ [length]^{-3/2} after integrating out chi.
  The chi integration is dimensionless (chi is dimensionless, dchi is dimensionless).

**Dimensional resolution:** The Jacobian J enters the volume measure d(vol_M5);
the inverse J^{-1} in the projection operator serves to undo the volume weighting
and extract the scalar density. The correct projection formula uses J not as a
division factor applied to the wavefunction value, but as the ratio of 5D volume
element to 4D volume element. The formal projection is:

    psi_nl(r, theta_pol) = integral over chi of Psi_nl d(chi)
                           evaluated with the chi-marginal of the M5 measure

Since d(vol_M5) = J * d(theta) * d(theta_pol) * d(phi_az) * d(chi) and we want
the 4D wavefunction in (r, theta_pol, phi_az) coordinates with the standard 4D
measure d(vol_4D) = r^2 dr * sin(theta_pol) d(theta_pol) * d(phi_az), the
projection that recovers the correct normalization is:

    psi_nl(r, theta_pol) = N_lift^{-1} ∫_0^{L_chi} Psi_nl(r, theta_pol, chi) d(chi)

where the d(chi) integral extracts the chi-independent part, and N_lift is
chosen so that ∫ |psi_nl|^2 r^2 sin(theta_pol) dr d(theta_pol) d(phi_az) = 1.

This formula will be evaluated in Step 2. The conclusion of the dimensional check
is: the form is consistent — N_lift is a dimensionless normalization constant
to be fixed in Step 2.

**Formal projection operator statement:**

    P: L^2(M5) → L^2(R^3)

    (P * Psi)(r, theta_pol, phi_az) = ∫_0^{L_chi} Psi(r, theta_pol, phi_az, chi) d(chi)

This definition uses the 4D volume element in the output space and integrates
out the compact chi. The Jacobian of the embedding enters when converting
between the 5D native coordinates (theta, theta_pol, phi_az, chi) and the 4D
Cartesian (r, theta_pol, phi_az) — this conversion is what fixes N_lift.

Step 2 will explicitly evaluate P * Psi_nl and show it equals psi_nl, fixing N_lift.

---

## Summary of Step 1

Four sub-parts completed:

| Sub-step | Content | Status |
|----------|---------|--------|
| 1A | Canonical psi_nlm from Griffiths; m=0 restriction noted (CP-1, non-structural) | COMPLETE |
| 1B | R_nl expressed in spiral coordinate theta via r = r_0 exp(alpha theta) | COMPLETE |
| 1C | 5D wavefunction Psi_nl = N_lift * R_nl^(spiral)(theta) * Y_l^0 * delta(chi - theta mod L_chi) | COMPLETE |
| 1D | Projection operator P defined; dimensional check performed; N_lift deferred to Step 2 | COMPLETE |

**Postulates invoked:** P-1, P-2, P-3, P-4, P-5, P-6 (all six; none missing, none new).

**New postulates introduced:** NONE.

**Golden-ratio alert:** NOT triggered. The symbol phi_az (azimuthal angle) appears
but is distinct from the golden ratio. The value ~1.618 does not appear.

**Structural CHOICE points:** NONE (CP-1 and CP-2 are both non-structural; assessed
above).

**Non-structural CHOICE points recorded:** CP-1 (m=0 restriction), CP-2 (delta-function
localization). Both are in derivation_metadata.choice_points above.

---

## Next step (to be dispatched in next /prism-next call)

**Step 2 — Evaluate the projection integral to verify 4D reduction.**

Specifically: perform the chi-integral of Psi_nl over [0, L_chi], apply the
r → r_0 exp(alpha theta) inverse to convert back to the 4D wavefunction in (r,
theta_pol) coordinates, and confirm the result equals R_nl(r) * Y_l^0(theta_pol)
up to N_lift. Fix N_lift.

**Step 3 — Angular momentum quantization from compactification topology.**

Show that the winding-count condition on the compact dimension (P-5: L_chi = 2 pi/alpha;
P-4: chi winds by 2 pi per theta-revolution) implies that n, l must be integers —
i.e., angular momentum quantization emerges from geometry.

---

## What the next /prism-next should hand off to P1-T3

Once Steps 2 and 3 are complete and reviewed, the P1-T3 agent (s-state correction)
needs from this document:
1. The explicit form of Psi_nl (Step 1C) — in particular its behavior at small r (theta → -∞).
2. The projection operator P (Step 1D, fixed in Step 2) — in particular J^{-1} and N_lift.
3. The angular quantization condition (Step 3).
4. The spiral-coordinate substitution r = r_0 exp(alpha theta).

All of the above will be in the final version of this document after Steps 2 and 3
are completed.

---

*End of Step 1. Verdict: STEP_COMPLETE_PENDING_REVIEW.*
*Awaiting human-in-the-loop review (per spec §11: theoretician tasks require human review at each step) before Step 2 is dispatched.*
