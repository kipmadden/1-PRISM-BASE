---
generated_by: prism-theoretician
generated_at: 2026-04-17T00:00:00Z
spec_task_id: P1-T1
depends_on: []
source_material_available:
  - prism_research_plan_v1.0.md (spec §1, §2, §4, Appendix A, Appendix B)
  - prism_basis_research_summary_v1.docx (unextracted; used via Appendix B summary)
  - prism_hydrogen_v3.py (Phase 0 pipeline code)
source_material_missing:
  - kip_madden_prism_notes.md (declared P1-T1 input — NOT FOUND on disk)
  - prism_framework_v7.0.4_draft.md (declared P1-T1 input — NOT FOUND on disk)
flags_requiring_kip_review: [F1, F2, F3, F4, F5, F6, F7]
status: DRAFT — AWAITING CP1 HUMAN REVIEW
---

# PRISM Formal Framework Specification — P1-T1 Output

**Task:** P1-T1 — Formalize PRISM framework for computation
**Agent:** prism-theoretician
**Date:** 2026-04-17
**Status:** DRAFT. Every section marked FLAG must be resolved by Kip Madden at Checkpoint CP1 before P1-T2 dispatch.

---

## Scope of This Document

This document covers the postulate set, notation, and coordinate definitions for the PRISM 5D framework — sufficient to begin P1-T2 (wavefunction derivation). It does NOT contain any wavefunction equations; those begin in P1-T2 after CP1 approval.

The document is grounded in material extractable from the spec (§1, §4, Appendix A, Appendix B) and the implied structure of the Phase 0 pipeline. Where the primary framework notes (`kip_madden_prism_notes.md`, `prism_framework_v7.0.4_draft.md`) have not yet been supplied, this document:
1. States what CAN be inferred from available material.
2. Explicitly flags every point requiring input from Kip.

---

## Section 1. Mission Statement (Source: Spec §1)

PRISM proposes that atomic structure is a 4D Cartesian projection of a 5D logarithmic-spiral worldline, with the fine-structure constant α serving as the native rotation-scaling coupling constant of that spiral. The framework aims to derive known QED quantities (Lamb shift, Bethe logarithm, muonic proton radius) from the geometry alone, without fitting parameters to data.

---

## Section 2. Postulate Set

Each postulate is stated precisely. Any postulate requiring a choice not dictated by prior material is marked FLAG.

### Postulate P-1: Spacetime Dimensionality

The physical world is embedded in a 5-dimensional manifold M5 with signature (1, 3, 1) — one time dimension, three spatial dimensions, and one compact internal dimension. The compact dimension is denoted χ.

> **Source basis:** Spec §1 ("5D logarithmic-spiral worldline"); Appendix B ("5-fold-symmetry / φ signature").
>
> **FLAG F1:** The signature of the compact dimension is assumed spacelike (+1 in the metric). If χ is timelike or null, the wavefunction normalization and energy eigenvalue conditions change fundamentally. Kip must confirm: is χ spacelike?

### Postulate P-2: Compactification Topology

The compact dimension χ has the topology of a circle S¹ with circumference L_χ. Points identified as (x^μ, χ) = (x^μ, χ + L_χ) for all x^μ.

> **Source basis:** Standard Kaluza-Klein compactification; implied by "compactification" language in spec §4 assumption_2 and assumption_4.
>
> **FLAG F2:** The circumference L_χ may be a free parameter unless fixed by the geometry. If L_χ is set by α alone (as implied by spec §1), the explicit relation L_χ = f(α) must be stated. Kip must supply this relation from the framework notes. Without it, the derivation in P1-T2 will have an undetermined scale.

### Postulate P-3: Worldline Geometry — Logarithmic Spiral

The electron's worldline in M5 is a logarithmic spiral in the (r, χ) plane, defined by:

    r(θ) = r_0 · exp(k · θ)

where:
- r: Type = real positive scalar, Range = (0, ∞), Physical interpretation = radial distance from the nucleus in the 3+1 Cartesian projection
- θ: Type = real scalar angle, Range = [0, 2π) per orbital cycle (may extend beyond for excited states), Physical interpretation = angular parameter along the spiral worldline
- r_0: Type = real positive scalar, Range = (0, ∞), Physical interpretation = reference radius (related to Bohr radius a_0)
- k: Type = real scalar, Range = (−∞, ∞), Physical interpretation = spiral growth rate, encoding the coupling between rotation and scaling

> **Source basis:** Spec §1 ("logarithmic-spiral worldline"); spec §4 assumption_4 ("5-fold-symmetry / φ signature").
>
> **FLAG F3:** The growth rate k is the central free parameter of the framework. If PRISM is to be parameter-free, k must be expressed as a function of α alone. The relation k = g(α) must be supplied from the framework notes. Without it, P1-T3 cannot produce a no-free-parameter result. Kip must supply this relation.
>
> **FLAG F4:** The logarithmic spiral is stated in 2D (r, θ). Its embedding in M5 requires specifying how θ maps onto the compact dimension χ and the 3+1 spatial directions. Kip must supply the embedding map: θ ↦ (x¹, x², x³, χ).

### Postulate P-4: α as Rotation-Scaling Coupling

The fine-structure constant α ≈ 1/137 is the native rotation-scaling coupling of the 5D logarithmic spiral. It governs the ratio of angular momentum to radial scaling per orbital cycle.

> **Source basis:** Spec §1 ("α as the native rotation-scaling coupling").
>
> **FLAG F5:** The precise mathematical statement of this postulate must be given. Two candidate forms:
> - (a) k = α (the growth rate equals the fine-structure constant directly)
> - (b) k = f(α) for some function f derived from the spiral geometry
>
> Either requires explicit justification from the framework notes. If (a) is adopted without derivation, it is a free postulate — acceptable only if flagged as such. Kip must confirm which form and supply the derivation or justification.

### Postulate P-5: 4D Cartesian Projection

The 4D Cartesian spacetime that we observe is a projection of M5 obtained by integrating over the compact dimension χ:

    Ψ_4D(x^μ) = ∫₀^{L_χ} Ψ_5D(x^μ, χ) dχ

(Integration measure to be normalized; details in P1-T2.)

> **Source basis:** Spec §1 ("4D Cartesian projection"); spec §4 assumption_2, assumption_3.
>
> This postulate is stated in conventional Kaluza-Klein language. Its application to the hydrogen wavefunction is worked out in P1-T2. The postulate as stated here is not claimed to be original — it is the standard projection prescription, applied to the PRISM spiral geometry.

### Postulate P-6: s-State Specialness

In s-states (orbital angular momentum ℓ = 0), the electron's 3+1 spatial wavefunction has non-zero density at the nucleus. The PRISM framework predicts that this contact with the origin couples to the compact dimension χ in a way that does not occur for ℓ ≥ 1 states.

> **Source basis:** Spec Appendix B ("s-states feel extra coupling, pattern scales correctly"); Phase 0 finding ("qualitative PRISM prediction confirmed").
>
> **FLAG F6:** The precise mechanism of this coupling is the content of P1-T3 (the central calculation). This postulate states only that the coupling exists and is ℓ-dependent. The mathematical form is NOT postulated here — it must be derived from Postulates P-1 through P-5. If a specific form cannot be derived (i.e., must be postulated), that is a framework incompleteness and must be flagged at P1-T3.

---

## Section 3. Notation Table

All variables used across the derivation chain P1-T1 through P1-T5 are defined here. Agents in P1-T2 onward must use this notation without alteration; any needed additions must be proposed as an amendment to this document.

| Symbol | Type | Range | Physical interpretation | Defined in |
|--------|------|-------|------------------------|------------|
| M5 | manifold | — | 5D physical manifold | P-1 |
| x^μ | 4-vector of reals | μ = 0,1,2,3 | 4D Cartesian coordinates (t, x, y, z) | P-1 |
| χ | real scalar | [0, L_χ) | compact 5th dimension coordinate | P-1, P-2 |
| L_χ | real positive scalar | (0, ∞) | circumference of compact dimension | P-2; FLAG F2 |
| r | real positive scalar | (0, ∞) | radial distance from nucleus (3D Cartesian) | P-3 |
| θ | real scalar | [0, ∞) | angular parameter along spiral worldline | P-3 |
| r_0 | real positive scalar | (0, ∞) | spiral reference radius | P-3 |
| k | real scalar | (−∞, ∞) | spiral growth rate | P-3; FLAG F3 |
| α | real positive scalar | ≈ 7.2974 × 10⁻³ | fine-structure constant (CODATA 2022) | P-4 |
| n | positive integer | {1, 2, 3, ...} | principal quantum number | standard QM |
| ℓ | non-negative integer | {0, 1, ..., n-1} | orbital angular momentum quantum number | standard QM |
| j | half-integer or integer | \|ℓ ± 1/2\| | total angular momentum quantum number | standard QM |
| a_0 | real positive scalar | ≈ 5.2918 × 10⁻¹¹ m | Bohr radius | CODATA 2022 |
| m_e | real positive scalar | ≈ 9.1094 × 10⁻³¹ kg | electron mass | CODATA 2022 |
| m_p | real positive scalar | ≈ 1.6726 × 10⁻²⁷ kg | proton mass | CODATA 2022 |
| μ_r | real positive scalar | = m_e · m_p / (m_e + m_p) | reduced mass of hydrogen system | derived |
| Ψ_5D | complex scalar field | L²(M5) | 5D wavefunction on M5 | P-5 |
| Ψ_4D | complex scalar field | L²(R^(1,3)) | 4D projected wavefunction | P-5 |
| φ | real scalar | ≈ 1.6180 | golden ratio = (1 + √5)/2 | Appendix B; FLAG F7 |

> **FLAG F7 (φ):** The golden ratio φ appears in spec Appendix B ("5-fold-symmetry / φ signature" with 2.7σ marginal detection). Its role in the framework is not yet postulated — it is an observed candidate signature, not a derived quantity. If φ appears in the derivation, it must emerge from the geometry (e.g., from the Fibonacci spiral / logarithmic spiral relationship) rather than being introduced as a postulate. Kip must clarify: is φ expected to appear explicitly in any postulate, or only as an emergent consequence?

---

## Section 4. Coordinate Transformation: 5D Native to 4D Cartesian

The transformation from the 5D spiral-native coordinates to 4D Cartesian is the central geometric object of the framework. The following is the candidate form, to be confirmed by Kip at CP1.

### 4.1 5D Spiral Coordinates

The native coordinates of a point on the electron's worldline in M5 are:

    (θ, φ_az, φ_pol, χ, t)

where:
- θ: spiral angular parameter (as defined in P-3)
- φ_az: azimuthal angle in 3D space, Range [0, 2π), Type real
- φ_pol: polar angle in 3D space, Range [0, π], Type real
- χ: compact dimension coordinate, Range [0, L_χ), Type real
- t: time coordinate, Range (−∞, ∞), Type real

### 4.2 Forward Map: 5D Spiral → 4D Cartesian

Given the spiral relation r(θ) = r_0 · exp(k · θ), the map to 4D Cartesian coordinates (t, x, y, z) is:

    t       = t                                    (time is unchanged)
    x       = r(θ) · sin(φ_pol) · cos(φ_az)
    y       = r(θ) · sin(φ_pol) · sin(φ_az)
    z       = r(θ) · cos(φ_pol)

with r(θ) = r_0 · exp(k · θ).

The compact coordinate χ does not appear in the 4D Cartesian map — it is integrated over per Postulate P-5. The specific coupling of χ to the spiral parameter θ is:

    [[CHOICE: χ-θ coupling form]]
    Candidate A: χ = θ mod L_χ  (linear identification)
    Candidate B: χ = (2π/n) · θ mod L_χ  (n-dependent compactification)
    Candidate C: χ is an independent degree of freedom, not coupled to θ

> **FLAG F3 (continued):** The coupling between χ and θ is the key to deriving the s-state correction. Candidate A (linear) is the simplest but may not produce the correct n-dependence of the Bethe log analog. Candidates B and C are more flexible but introduce additional structure. **Kip must select and justify one coupling form from the framework notes before P1-T2 can proceed.**

### 4.3 Inverse Map: 4D Cartesian → 5D Spiral

From the 4D Cartesian coordinates, the spiral parameter θ is recovered as:

    r = √(x² + y² + z²)
    θ = (1/k) · ln(r / r_0)      [defined up to 2π/k ambiguity per spiral period]
    φ_az = atan2(y, x)
    φ_pol = arccos(z / r)

The compact coordinate χ is not recoverable from 4D Cartesian data alone — this is consistent with χ being a hidden dimension (Postulate P-1).

### 4.4 Jacobian

The Jacobian of the forward map (∂(x,y,z) / ∂(θ, φ_az, φ_pol)) is:

    J = r(θ)² · k · r(θ) · sin(φ_pol)
      = k · r_0³ · exp(3kθ) · sin(φ_pol)

This Jacobian is required for computing volume elements and wavefunction normalization in P1-T2.

> Note: the factor of k in the Jacobian means that if k → 0 (no spiral growth), the map becomes singular and the 5D description degenerates. This is consistent with k being required to be non-zero.

---

## Section 5. Physical Constants (Fixed — CODATA 2022)

The following constants are fixed by external measurement and are not free parameters of PRISM. Any derivation that requires adjusting these constants to match data is disqualified.

| Constant | Symbol | Value | Source |
|----------|--------|-------|--------|
| Fine-structure constant | α | 7.2973525643 × 10⁻³ | CODATA 2022 |
| Bohr radius | a_0 | 5.29177210544 × 10⁻¹¹ m | CODATA 2022 |
| Electron mass | m_e | 9.1093837139 × 10⁻³¹ kg | CODATA 2022 |
| Proton mass | m_p | 1.67262192595 × 10⁻²⁷ kg | CODATA 2022 |
| Speed of light | c | 2.99792458 × 10⁸ m/s | CODATA 2022 (exact) |
| Planck constant | ℏ | 1.054571817 × 10⁻³⁴ J·s | CODATA 2022 |
| Golden ratio | φ | (1 + √5)/2 ≈ 1.6180339887 | mathematical constant |

---

## Section 6. Target Quantities (From Spec Appendix A — For Reference Only)

These values are the comparison targets for P1-T5. They must NOT be used to adjust any derivation step in P1-T2 or P1-T3.

| n | Bethe log (Drake & Swainson 1990) |
|---|-----------------------------------|
| 1 | 2.984128556 |
| 2 | 2.811769893 |
| 3 | 2.767663612 |
| 4 | 2.749811840 |
| 5 | 2.740823727 |

These are listed here solely so that the theoretician can confirm the derivation is addressing the correct quantity. The derived PRISM analog will be evaluated by prism-computer (P1-T4) and compared by prism-validator (P1-T5).

---

## Section 7. What This Document Does Not Cover

The following are explicitly out of scope for P1-T1 and are reserved for later tasks:

- Wavefunction ψ_5D(n, ℓ, j, χ, r) — derived in P1-T2
- 4D projection and reduction to standard hydrogen wavefunction — derived in P1-T2
- Angular momentum quantization from compactification topology — derived in P1-T2
- s-state correction integral expression — derived in P1-T3
- Numerical evaluation — P1-T4
- Comparison to Bethe log — P1-T5

---

## Section 8. Flags Summary — Required Kip Input Before CP1 Approval

| Flag ID | Section | Question for Kip | Blocking which task? |
|---------|---------|-----------------|---------------------|
| F1 | P-1 | Is the compact dimension χ spacelike? | P1-T2 |
| F2 | P-2 | What is the explicit relation L_χ = f(α)? | P1-T2, P1-T3 |
| F3 | P-3, §4.2 | What is the spiral growth rate k in terms of α? What is the χ-θ coupling form? | P1-T2, P1-T3 |
| F4 | P-3 | What is the explicit embedding map θ ↦ (x¹, x², x³, χ)? | P1-T2 |
| F5 | P-4 | Is k = α directly, or k = f(α) for some other f? Supply justification. | P1-T3 |
| F6 | P-6 | Confirm: the s-state coupling mechanism must emerge from derivation, not be postulated. Is that the intent? | P1-T3 |
| F7 | §3 (φ) | Is φ expected to appear explicitly in any postulate, or only as emergent? | P1-T2, P1-T3 |

**CP1 human review must resolve all 7 flags before P1-T2 is dispatched.** Kip's answers should be supplied as an amendment section appended to this document.

---

## Section 9. Source Material Gap Notice

The two declared input files for P1-T1 per spec §8 were not found on disk:

- `kip_madden_prism_notes.md` — NOT FOUND
- `prism_framework_v7.0.4_draft.md` — NOT FOUND

This document was prepared from:
- `prism_research_plan_v1.0.md` (spec §1, §4, Appendix A, Appendix B)
- The implied structure of the Phase 0 v3 pipeline

The transcript file `4D PRISM BASIS Transcript 041526.docx` is present but was not extractable in this agent session. **Kip should supply the primary framework notes either as plain-text files or by pasting the relevant framework definitions into the CP1 review response.** The flags in Section 8 are likely fully or partially resolved in those notes.

---

## Section 10. Consistency Check

The postulates as stated are not internally inconsistent based on available material. The main unresolved structural question (Flags F3, F4, F5) concerns the relationship between k, α, and χ — if k is not expressible as a pure function of α, PRISM will require at least one additional parameter and the "no free parameters beyond α" claim (spec §2 success criterion) will fail. This would not necessarily terminate the program (see spec §14), but it would require explicit documentation.

No framework inconsistency has been detected. The flag list above represents open questions, not contradictions.

---

*End of prism_formal_spec.md — P1-T1 draft output. Awaiting CP1 human review.*
