# P1-T3 Derivation Log

Append-only step-by-step audit of the PRISM s-state correction derivation.
Format: `<step> | <UTC timestamp> | <decision> | <one-line summary>`

1 | 2026-04-17T00:00:00Z | ACCEPT (Kip Madden, "named and justified") | 5D Hamiltonian decomposition: H_5D = H_0 + H_chi; Delta_E_nl = <Psi_nl|H_chi|Psi_nl>; Delta_E_nS = Delta_E_{n,0}. Postulates P-1, P-6. No new postulates. No CHOICE flags.
2 | 2026-04-17T00:00:00Z | ACCEPT (Kip Madden) | Fourier regularization (Path-B): δ→k=n mode (P1-T2 §3.3 topology-to-QN identification); Jacobian dθ/dr=1/(αr) derived from F4 embedding; R_χ=a₀/α; r₀≡a₀ by parameter-parsimony. ΔE_nℓ=ℏ²n²α²/(2m_e a₀²). 2 CHOICE flags resolved inline. No new postulates.

ADVANCE WARNING FOR STEP 3 (Kip Madden, 2026-04-17): ΔE_nℓ = n²·α²·Ry is ~10³× too large and has wrong n-scaling vs Bethe-log target. Step 3 P-6 Jacobian weighting must simultaneously (i) introduce ℓ-selectivity, (ii) reduce magnitude by ~α, (iii) reshape n² → roughly flat. If it does not, cp2 may fire before Step 3 completes.
