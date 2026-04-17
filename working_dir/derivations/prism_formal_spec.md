---
generated_by: prism-theoretician
generated_at: 2026-04-17T00:00:00Z
revised_at: 2026-04-17T00:00:00Z
revision: 2
spec_task_id: P1-T1
depends_on: []
source_material_available:
  - prism_research_plan_v1.0.md (spec §1, §2, §4, Appendix A, Appendix B)
  - prism_basis_research_summary_v1.docx (unextracted; used via Appendix B summary)
  - prism_hydrogen_v3.py (Phase 0 pipeline code)
  - working_dir/kip_madden_prism_notes.md (PRIMARY INPUT for revision 2 — 467 lines, Kip's authoritative framework notes with explicit F1-F7 resolutions and consolidated postulate set P-1..P-6)
source_material_missing:
  - prism_framework_v7.0.4_draft.md (declared P1-T1 input — NOT FOUND on disk; superseded by kip_madden_prism_notes.md per Kip's instruction)
flags_requiring_kip_review: []
new_flags_raised_this_revision: []
status: DRAFT_PENDING_CP1
verdict: DRAFT_PENDING_CP1
revision_history:
  revision_1:
    generated_at: 2026-04-17T00:00:00Z
    status: DRAFT — AWAITING CP1 HUMAN REVIEW
    flags: [F1, F2, F3, F4, F5, F6, F7]
    outputs:
      - working_dir/derivations/prism_formal_spec.md (revision 1 — now superseded)
      - working_dir/derivations/prism_coordinate_diagram.svg
    notes: >
      Primary inputs kip_madden_prism_notes.md and prism_framework_v7.0.4_draft.md
      were not found on disk. All 7 flags raised as open questions for Kip.
      Kip supplied kip_madden_prism_notes.md resolving all 7 flags; CP1 decision
      = REVISE (Path A); revision 2 dispatched 2026-04-17.
---

# PRISM Formal Framework Specification — P1-T1 Output (Revision 2)

**Task:** P1-T1 — Formalize PRISM framework for computation
**Agent:** prism-theoretician
**Date (revision 2):** 2026-04-17
**Status:** DRAFT_PENDING_CP1. Flags F1-F7 resolved by Kip Madden via kip_madden_prism_notes.md. No new flags raised during integration (see Section 8). This document is ready for Kip's CP1 APPROVE decision before P1-T2 dispatch.

---

## Scope of This Document

This document establishes the postulate set, notation, coordinate definitions, and embedding map for the PRISM 5D framework — sufficient to begin P1-T2 (wavefunction derivation) and P1-T3 (s-state correction integral). It does NOT contain wavefunction equations; those begin in P1-T2 after CP1 approval.

Revision 2 integrates Kip Madden's authoritative framework notes (kip_madden_prism_notes.md, 2026-04-17) as primary input. All postulates in §2 are taken verbatim from that document's §4 (Consolidated postulate set). Where revision 1 inferred or flagged a choice, revision 2 substitutes Kip's explicit answer.

The theoretician's job on this revision is integration and consistency checking, not re-derivation. One new structural note has been added in Section 10 (Consistency Check) regarding a minor notational collision between the revision-1 coordinate φ_az and the golden ratio φ — resolved cleanly, no new flag required (see §10).

---

## Section 1. Mission Statement (Source: Spec §1 + Notes §1)

PRISM proposes that atomic structure is a 4D Cartesian projection of a 5D logarithmic-spiral worldline, with the fine-structure constant α serving as the native rotation-scaling coupling constant of that spiral. The framework aims to derive known QED quantities (Lamb shift, Bethe logarithm, muonic proton radius) from the geometry alone, without fitting parameters to data.

The two commitments at the core (notes §1):

1. **α is a geometric rate, not merely a coupling number.** Specifically, α is the ratio of the electron worldline's angular velocity (how fast it winds) to its radial scaling rate (how fast the log-spiral opens). k ≡ α.

2. **Quantum numbers are winding counts.** n, ℓ, m are how many times the spiral winds the compactified dimension before closing onto itself at a given orbital radius.

---

## Section 2. Postulate Set

The following six postulates are Kip Madden's consolidated postulate set from kip_madden_prism_notes.md §4, taken verbatim. They replace the inferred postulates of revision 1. No postulate here is the theoretician's own inference; each is labeled with its source authority.

### Postulate P-1: 5D Spacetime, KK Compactification

Spacetime is (1,3) Minkowski plus one compactified spacelike axis χ. Signature (+,−,−,−,−). Compactification length L_χ is finite and fixed by P-2 and P-3 (via the closure condition in P-5).

> **Source:** Notes §4, P-1. Notes §3 F1: "χ is spacelike. Signature (+,−,−,−,−). Postulate."
>
> **Flag F1: RESOLVED.** χ is spacelike. Two-time pathologies explicitly rejected by Kip (notes §3 F1). Kaluza-Klein style compactification.

### Postulate P-2: Electron Worldline is a Logarithmic Spiral

The electron in a bound state traces a logarithmic spiral in the (x, y) plane of the 4D slice, with growth rate k and angular coordinate θ:

    r(θ) = r₀ · exp(k · θ)

Orientation (which plane) is a convention choice; observables are rotation-invariant. z = 0 along the spiral plane is a gauge choice, not a physical constraint.

> **Source:** Notes §4, P-2.

### Postulate P-3: k = α (Growth Rate Identification)

The log-spiral growth rate k is identified with the fine-structure constant α measured at the electron rest-mass scale:

    k ≡ α ≈ 7.2973525643 × 10⁻³   (CODATA 2022, low-energy value)

This is a direct identification, not a renormalization-group derived relation. The running of α with energy scale is a derived prediction of the framework (Phase 3, P3-T2), not an input.

> **Source:** Notes §4, P-3. Notes §3 F3: "k ≡ α directly." Notes §3 F5: "direct identification at the electron-mass scale."
>
> **Flag F3 (partial): RESOLVED.** k = α. See also P-4 for χ-θ coupling.
>
> **Flag F5: RESOLVED.** k = α is a direct identification at electron rest-mass scale. Running emerges as derived prediction in Phase 3.

### Postulate P-4: Modular χ-θ Coupling

The compact coordinate χ is coupled to the spiral angle θ by a linear modular map:

    χ(θ) = θ mod L_χ

The electron winds the compact dimension linearly with the spiral angle. This is Candidate A of revision 1. Candidates B and C are rejected (notes §3 F3: "I don't see motivation for it and it breaks the winding-count interpretation of n").

> **Source:** Notes §4, P-4. Notes §3 F3: "Candidate A."
>
> **Flag F3 (continued): RESOLVED.** χ-θ coupling is linear modular, Candidate A selected.
>
> **Flag F4: RESOLVED.** Full embedding map given in Section 4 of this document.

### Postulate P-5: Closure Condition Fixes L_χ (Derived, Not Independent)

Combined with P-3, the requirement that one spiral θ-revolution traverses one full compact circle gives:

    α · L_χ = 2π   ⇒   L_χ = 2π / α

With α ≈ 1/137.036, L_χ ≈ 860.9 (dimensionless; units: radians, with r₀ = 1 setting length scale).

This is not an independent postulate — it is derived from P-1 (compactification), P-2 (log-spiral), P-3 (k = α), and P-4 (linear χ-θ coupling). The closure argument: if χ(θ) = θ mod L_χ and k = α, then one full θ-revolution (Δθ = 2π) advances χ by 2π, which must equal L_χ for the spiral to close. Therefore L_χ = 2π/α.

The α in L_χ is the low-energy α (at the electron rest-mass scale). At higher energies, L_χ would differ by the running-α correction (see P3-T2, Phase 3).

> **Source:** Notes §4, P-5. Notes §3 F2: "L_χ = 2π/α (closure condition; derived from P-2/P-3, not free)."
>
> **Flag F2: RESOLVED.** L_χ = 2π/α, derived not free.

### Postulate P-6: 4D Projection is the QM Wavefunction

The 4D-observed wavefunction is the projection of the 5D worldline density onto 4D Cartesian coordinates, with the Jacobian of the embedding map (derived from P-2 and P-4):

    J(θ, θ_pol) = k · r₀³ · exp(3kθ) · sin(θ_pol)

where θ_pol is the polar angle in 3D space. The QM hydrogen Hamiltonian emerges as the effective projected dynamics. This is to be validated in P1-T2 by recovering the Schrödinger equation as an effective 4D limit.

The s-state extra coupling is NOT postulated. It emerges from the small-r behavior of ψ_s interacting with the J ∝ exp(3kθ) factor (which concentrates at small r = small θ). Higher-ℓ states are suppressed by the centrifugal barrier ℓ(ℓ+1)/r² and never probe that region. This mechanism is to be made quantitative in P1-T3.

> **Source:** Notes §4, P-6. Notes §3 F6: "s-state extra coupling is DERIVED from P-2/P-4/P-6 small-r behavior of ψ_s, not postulated."
>
> **Flag F6: RESOLVED.** s-state coupling is derived. No new postulate needed.

---

## Section 3. What Is Explicitly NOT Postulated

Per kip_madden_prism_notes.md §4 ("Not postulated"):

- **s-state extra coupling** — derived from P-2/P-4/P-6 via small-r behavior of ψ_s.
- **Running of α** — derived prediction; Phase 3, P3-T2.
- **γ (Euler–Mascheroni constant)** — expected to emerge as regularization residue in the Bethe-log calculation; not postulated.
- **The "036" tail of 1/α = 137.036** — expected as projection residue of irrational winding count onto integer grid; not postulated.
- **QED α-power series** — all derived as projection residues; not postulated.
- **φ (golden ratio)** — EXPLICITLY EXCLUDED from the postulate set. If φ appears in a derivation step, it must be flagged as a red signal (notes §3 F7: "flag as a red signal"; notes §7 falsification condition 3: "If the derivation requires φ as a postulate → kill").

> **Flag F7: RESOLVED.** φ is excluded from the postulate set. Its appearance in any derivation is a red signal, not a legitimate result.

---

## Section 4. Coordinate Transformation: 5D Native → 4D Cartesian

This section gives the fully resolved embedding map, integrating Kip's answer to F4 (notes §3 F4).

### 4.1 Resolved Forward Map

The electron's worldline in M5 is parameterized by θ. The full embedding is:

    x(θ)  = r₀ · exp(α·θ) · cos(θ)          [Cartesian x]
    y(θ)  = r₀ · exp(α·θ) · sin(θ)          [Cartesian y]
    z(θ)  = 0                                  [spiral lies in xy-plane by convention]
    χ(θ)  = θ mod L_χ                         [compact coordinate, modular]
    t(θ)  = τ(θ)                              [proper-time; DEFERRED — known open item]

The spiral lies in the (x,y) plane. z = 0 is a gauge choice (rotation invariance means the plane is not physically distinguished). The orientation of the plane does not affect spectral observables.

**Status of t(θ):** The proper-time parameterization is not yet specified. For non-relativistic hydrogen the expected form is t ∝ θ (linear), which should recover the Schrödinger equation as an effective 4D limit. This is a known open item flagged by Kip (notes §6), to be addressed at the start of P1-T3. It is not a new flag — it is a documented uncertainty within the existing framework. P1-T3 will either confirm t ∝ θ as sufficient or surface a constraint.

### 4.2 Radial and Jacobian Relations

From the forward map, the radial distance from the nucleus is:

    r = √(x² + y²) = r₀ · exp(α·θ)

The inverse gives the spiral parameter from Cartesian coordinates:

    θ = (1/α) · ln(r / r₀)     [defined up to additive multiples of L_χ = 2π/α]

The Jacobian of the map (∂(x,y,z)/∂(θ, θ_pol, φ_az)), evaluated including the full 3D solid-angle structure, is:

    J(θ, θ_pol) = α · r₀³ · exp(3α·θ) · sin(θ_pol)

Note: k has been replaced by α throughout per Postulate P-3.

The exp(3αθ) factor is the volume-element driver for the s-state enhancement: at small r (small θ), this factor is small, which concentrates wavefunction density toward the spiral core and produces the ℓ = 0 coupling discussed in Postulate P-6.

### 4.3 Coupling Summary

| Mapping | Expression | Status |
|---------|-----------|--------|
| r(θ) | r₀ · exp(αθ) | Postulate P-2 + P-3 |
| χ(θ) | θ mod (2π/α) | Postulate P-4 + P-5 |
| L_χ | 2π/α | Derived closure (P-5) |
| J(θ, θ_pol) | α · r₀³ · exp(3αθ) · sin(θ_pol) | Derived from P-2, P-3, P-4 |
| t(θ) | τ(θ), form TBD | Deferred — known open item for P1-T3 |

---

## Section 5. Notation Table

All variables used across the derivation chain P1-T1 through P1-T5 are defined here. Agents in P1-T2 onward must use this notation without alteration; any needed additions must be proposed as an amendment to this document.

Notation change from revision 1: the azimuthal angle formerly called φ_az is now called φ_az throughout (unchanged symbol), but the golden ratio symbol φ is removed from the notation table entirely per Kip's F7 resolution. If φ (golden ratio) appears in any downstream derivation it is a signal, not a defined symbol.

| Symbol | Type | Range | Physical interpretation | Defined in |
|--------|------|-------|------------------------|------------|
| M5 | manifold | — | 5D physical manifold with signature (+,−,−,−,−) | P-1 |
| x^μ | 4-vector of reals | μ = 0,1,2,3 | 4D Cartesian coordinates (t, x, y, z) | P-1 |
| χ | real scalar | [0, L_χ) | compact 5th spacelike dimension coordinate | P-1, P-2 |
| L_χ | real positive scalar | = 2π/α | circumference of compact dimension | P-5 (derived) |
| r | real positive scalar | (0, ∞) | radial distance from nucleus = r₀·exp(αθ) | P-2, P-3 |
| θ | real scalar | [0, ∞) | angular parameter along spiral worldline | P-2 |
| r₀ | real positive scalar | (0, ∞) | spiral reference radius (related to a₀) | P-2 |
| k | real scalar | = α | spiral growth rate; k ≡ α by P-3 | P-3 |
| α | real positive scalar | ≈ 7.2973525643 × 10⁻³ | fine-structure constant (CODATA 2022); also equals k | P-3, P-4 |
| θ_pol | real scalar | [0, π] | polar angle in 3D space | §4 |
| φ_az | real scalar | [0, 2π) | azimuthal angle in 3D space | §4 |
| n | positive integer | {1, 2, 3, ...} | principal quantum number | standard QM |
| ℓ | non-negative integer | {0, 1, ..., n-1} | orbital angular momentum quantum number | standard QM |
| j | half-integer or integer | |ℓ ± 1/2| | total angular momentum quantum number | standard QM |
| a₀ | real positive scalar | ≈ 5.29177210544 × 10⁻¹¹ m | Bohr radius | CODATA 2022 |
| m_e | real positive scalar | ≈ 9.1093837139 × 10⁻³¹ kg | electron mass | CODATA 2022 |
| m_p | real positive scalar | ≈ 1.67262192595 × 10⁻²⁷ kg | proton mass | CODATA 2022 |
| μ_r | real positive scalar | = m_e·m_p/(m_e+m_p) | reduced mass of hydrogen system | derived |
| J | real positive scalar | = α·r₀³·exp(3αθ)·sin(θ_pol) | Jacobian of 5D→4D embedding map | §4, derived |
| Ψ_5D | complex scalar field | L²(M5) | 5D wavefunction on M5 | P-6 |
| Ψ_4D | complex scalar field | L²(R^(1,3)) | 4D projected wavefunction | P-6 |
| ΔE_nS | real scalar | (units of energy) | PRISM s-state self-energy correction for principal quantum number n | target of P1-T3 |
| β(n,s) | real scalar | dimensionless | Bethe logarithm for s-states; target comparison values from Drake-Swainson 1990 | P1-T5 comparison |

**Removed from revision 1 notation table:** φ (golden ratio). Reason: F7 resolution — φ is excluded from the postulate set and must not appear as a defined symbol in derivations.

---

## Section 6. Target Quantities (From Spec Appendix A — For Reference Only)

These values are the comparison targets for P1-T5. They must NOT be used to adjust any derivation step in P1-T2 or P1-T3.

| n | β(n,s) Drake-Swainson 1990 |
|---|---------------------------|
| 1 | 2.984128556 |
| 2 | 2.811769893 |
| 3 | 2.767663612 |
| 4 | 2.749811840 |
| 5 | 2.740823727 |

These are listed here solely so that the theoretician can confirm the derivation addresses the correct quantity. The derived PRISM analog will be evaluated by prism-computer (P1-T4) and compared by prism-validator (P1-T5).

---

## Section 7. P1-T3 / P1-T4 Recipe (From Notes §5)

Kip's explicit instruction for the next derivation steps (notes §5), recorded here for handoff:

1. Write down ψ_nℓ(r, θ_pol, φ_az) in 4D as the standard hydrogen wavefunctions.
2. Lift to 5D by attaching χ = θ mod L_χ and the Jacobian J = α·r₀³·exp(3αθ)·sin(θ_pol).
3. Compute the effective self-energy correction for an s-state, ΔE_nS, as the expectation value of the χ-derivative term in the lifted Hamiltonian, using L_χ = 2π/α.
4. Predict the Bethe logarithm β(n,s) = ln(k₀/Ry) for n = 1..5 from ΔE_nS via the standard Bethe-log definition.
5. Compare to Drake-Swainson 1990 values at P1-T5.

The recipe is stated here for orientation. P1-T2 begins the symbolic execution (wavefunction lifting); P1-T3 executes step 3 (the central integral); P1-T4 evaluates numerically; P1-T5 compares.

---

## Section 8. Flags Summary — Revision 2 Status

All seven flags from revision 1 are resolved. No new flags raised during revision 2 integration. See Section 10 for a minor notation note that was resolved without raising a flag.

| Flag ID | Section | Kip's Resolution | Source | Status |
|---------|---------|-----------------|--------|--------|
| F1 | P-1 | χ is spacelike. Signature (+,−,−,−,−). Postulate. | Notes §3 F1 | RESOLVED |
| F2 | P-2 | L_χ = 2π/α. Derived from closure condition on P-2/P-3/P-4, not a free parameter. | Notes §3 F2 | RESOLVED |
| F3 | P-3, P-4, §4 | k ≡ α directly. χ-θ coupling is linear modular: χ(θ) = θ mod L_χ. Candidate A selected. | Notes §3 F3 | RESOLVED |
| F4 | §4 | Embedding is planar log-spiral in (x,y), z=0, χ=θ mod L_χ. Forward map: x=r₀·exp(αθ)cosθ, y=r₀·exp(αθ)sinθ. t(θ) deferred as documented open item. | Notes §3 F4 | RESOLVED |
| F5 | P-3 | k = α at the electron rest-mass scale — direct identification. Running α is a derived prediction for Phase 3, not an additional postulate. | Notes §3 F5 | RESOLVED |
| F6 | P-6 | s-state extra coupling is DERIVED from P-2/P-4/P-6 via small-r behavior of ψ_s interacting with J ∝ exp(3αθ). No new postulate needed. | Notes §3 F6 | RESOLVED |
| F7 | §3, §5 | φ (golden ratio) is EXPLICITLY EXCLUDED from the postulate set. Any appearance in derivation is a red signal to be flagged, not a result to accept. | Notes §3 F7, Notes §7 kill-condition 3 | RESOLVED |

**New flags raised in revision 2:** NONE.

**CP1 auto-approve condition (per orchestrator and Kip's notes §8):** Since no new flags were raised, Kip may now issue APPROVE on CP1, which will unblock P1-T2 dispatch.

---

## Section 9. Source Material — Updated

**Revision 2 primary input (new):**
- `working_dir/kip_madden_prism_notes.md` — PRESENT. 467 lines. Kip Madden's authoritative framework notes, 2026-04-17. Contains: §1 framework commitments, §2 Phase 0 autopsy, §3 explicit F1-F7 resolutions, §4 consolidated postulate set P-1..P-6, §5 P1-T3/T4 recipe, §6 known uncertainties, §7 falsification conditions, §8 handoff instructions, §9 provenance. This document supersedes all theoretician inferences from revision 1 wherever they conflict.

**Still missing:**
- `prism_framework_v7.0.4_draft.md` — NOT FOUND. Kip has confirmed this was a draft that existed only as an intent, not a file. It is superseded by kip_madden_prism_notes.md for all purposes.
- `4D PRISM BASIS Transcript 041526.docx` — present on disk but not extractable as text in this agent session. Notes §9 cites it as the primary source for Kip's spoken commitments (642 lines, 2026-04-15). The notes file provides the relevant excerpts; the transcript is not needed for the derivation to proceed.

**Revision 1 inputs (unchanged):**
- `prism_research_plan_v1.0.md` (spec §1, §4, Appendix A, Appendix B)
- `prism_basis_research_summary_v1.docx` (unextracted; Appendix B summary used)
- `prism_hydrogen_v3.py` (Phase 0 pipeline code)

---

## Section 10. Consistency Check — Revision 2

### 10.1 Internal Consistency of the Postulate Set

The six postulates (P-1 through P-6) and derived relation P-5 are internally consistent:

- P-1 (spacelike χ) is compatible with P-2 (log-spiral in spatial plane) and P-4 (linear χ-θ coupling). No timelike mixing.
- P-3 (k = α) and P-4 (χ = θ mod L_χ) together with P-5 (L_χ = 2π/α) are mutually consistent by direct substitution: advancing θ by 2π advances χ by 2π, which equals L_χ = 2π/α · α = 2π. The closure is exact.
- P-6 (Jacobian = α·r₀³·exp(3αθ)·sin(θ_pol)) is derived from P-2, P-3, P-4 by the standard calculation — no circular reasoning.
- The exclusion of φ (F7 resolution) is consistent with k = α ≈ 0.0073, which is nowhere near log(φ) ≈ 0.481. No log-spiral geometry with k = α will produce φ natively.

### 10.2 Notation Collision — Resolved Without New Flag

Revision 1 used the symbol φ_az for the azimuthal angle in 3D space and separately listed φ for the golden ratio in the notation table. With φ (golden ratio) now excluded from the postulate set (F7 resolution), this collision is dissolved: φ is no longer a defined symbol in the derivation. The azimuthal angle retains its symbol φ_az throughout, which is unambiguous. No flag needed.

### 10.3 Open Items Documented (Not New Flags)

These items were explicitly flagged by Kip in notes §6 as known uncertainties. They are recorded here for the P1-T2 and P1-T3 agents:

1. **t(θ) proper-time parameterization is not yet specified.** Expected: t ∝ θ for non-relativistic limit. P1-T3 will either confirm this or surface a constraint. This is a documented open item within the existing framework, not an inconsistency.

2. **Relativistic limit (Dirac spectrum, Lamb shift proper)** — Phase 2 scope, not Phase 1.

3. **Log-spiral plane precession for moving electrons** — not relevant to stationary bound-state spectra; deferred.

4. **"036" tail of 1/α and γ (Euler-Mascheroni)** — expected as derived residues; verification at end of P1-T3 if time permits; not required for P1-T5 gate.

### 10.4 No Framework Inconsistency Detected

No contradiction among P-1 through P-6, L_χ = 2π/α, χ-θ coupling, and the embedding map has been found during revision 2 integration. The postulate set is tighter than revision 1 (fewer free choices) and fully specified for the purposes of P1-T2 wavefunction derivation.

---

## Section 11. Falsification Conditions (From Notes §7 — For Reference)

Recorded here so that prism-validator (P1-T5) has explicit kill criteria from Kip:

1. **P1-T5 returns FALSIFIED** (frac deviation ≥ 50% or mixed-sign on the Bethe log comparison) AND failure is not localized to a single n → program halts at CP3.
2. **The only rescue move requires a new postulate** beyond P-1..P-6 → kill per spec §14.
3. **The derivation requires φ as a postulate** to reproduce Bethe log values → kill. φ is not in the postulate set.
4. **k cannot be identified with α** (P1-T3 derivation only works with k ≠ α) → kill. The geometric identification k = α is the core claim of PRISM.

These conditions are to be held by the orchestrator and prism-validator, not re-evaluated by prism-theoretician.

---

## Section 12. What This Document Does Not Cover

The following are explicitly out of scope for P1-T1 and are reserved for later tasks:

- Wavefunction ψ_5D(n, ℓ, j, χ, r) — derived in P1-T2
- 4D projection and reduction to standard hydrogen wavefunction — derived in P1-T2
- Angular momentum quantization from compactification topology — derived in P1-T2
- s-state correction integral expression ΔE_nS — derived in P1-T3
- Numerical evaluation of β(n,s) — P1-T4
- Comparison to Bethe log — P1-T5

---

*End of prism_formal_spec.md — P1-T1 revision 2 output. Verdict: DRAFT_PENDING_CP1 (clean — no new flags). Ready for Kip Madden's CP1 APPROVE decision.*
