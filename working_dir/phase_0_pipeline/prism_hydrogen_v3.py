"""
PRISM v3 — Real NIST Data Edition
==================================

Fetches hydrogen energy levels from NIST's Handbook of Basic Atomic
Spectroscopic Data (static HTML tables that work through the sandbox proxy).

Source: https://physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable5.htm
Reference: MK00a = Kelleher & Podobedova 2008, based on Mohr & Kotochigova 2000

Units in NIST table: cm^-1 (wavenumbers). We convert to eV.
Conversion: 1 cm^-1 = 1.2398419843320e-4 eV (CODATA)

The table gives LEVELS ABOVE GROUND STATE (not binding energies).
Binding energy of level x = ionization_limit - level_x
Ionization limit for H I = 109678.7717 cm^-1 = 13.5984 eV
"""

import re
import requests
import numpy as np
from scipy import constants
from scipy.optimize import curve_fit
from dataclasses import dataclass
import warnings


# Physical constants (CODATA 2022)
ALPHA = constants.fine_structure
CM_TO_EV = 1.2398419843320e-4  # eV per cm^-1
H_EV_S = 4.135667696e-15
M_E_C2 = 510998.95069           # eV
PI = np.pi
PHI = (1 + np.sqrt(5)) / 2


# =============================================================================
# NIST FETCH + PARSE
# =============================================================================

NIST_URL = "https://physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable5.htm"


@dataclass
class Level:
    n: int
    l: int              # 0=s, 1=p, 2=d, 3=f, 4=g
    j: float            # total angular momentum
    energy_cm: float    # energy above ground state, cm^-1
    label: str

    @property
    def energy_ev(self) -> float:
        return self.energy_cm * CM_TO_EV

    def binding_ev(self, ionization_cm: float) -> float:
        return (ionization_cm - self.energy_cm) * CM_TO_EV

    def dirac_binding_ev(self) -> float:
        """Dirac fine-structure prediction for the binding energy."""
        j_half = self.j + 0.5
        under_root = j_half**2 - ALPHA**2
        if under_root <= 0:
            return float("nan")
        delta = j_half - np.sqrt(under_root)
        n_eff = self.n - delta
        gamma = (1 + (ALPHA / n_eff)**2) ** (-0.5)
        return M_E_C2 * (1 - gamma)


L_SYMBOL_TO_INT = {"s": 0, "p": 1, "d": 2, "f": 3, "g": 4, "h": 5, "i": 6}


def fetch_nist_h1_levels() -> tuple[list[Level], float]:
    """
    Fetch NIST H I energy level table, parse into Level objects.
    Returns (levels, ionization_limit_cm).
    """
    r = requests.get(NIST_URL, timeout=30)
    r.raise_for_status()
    html = r.text

    # Convert HTML to semi-structured text for easier parsing.
    # Strategy: extract the table cells, rebuild rows.
    # NIST's table has columns: Configuration | Term | J | Level (cm^-1) | Ref
    # Example row: "2 p 2 P° 1/2 82258.9191 MK00a"

    # Strip tags, normalize whitespace
    text = re.sub(r'<[^>]+>', '|', html)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&#176;', '°', text)
    text = re.sub(r'\|+', '|', text)
    text = re.sub(r' +', ' ', text)

    # Find the table data section
    # Rows look like "| 2 | p | 2 | P° | 1/2 | 82258.9191 | MK00a |"
    # But also rows with just "| 3/2 | 82259.2850 | MK00a |" when config carries over

    lines = [line.strip(' |') for line in text.split('|') if line.strip(' |')]

    levels = []
    current_n = None
    current_l = None
    ionization_cm = None

    # Find ionization limit first (text has pipe separators)
    m = re.search(r'H[|\s]+Limit[|\s]+([0-9]+\.[0-9]+)', text)
    if m:
        ionization_cm = float(m.group(1))

    # Parse energy levels from text, row by row.
    # Pattern: [n] [l_letter] [2S+1] [Term] J  energy  Ref
    # Or continuation: J  energy  Ref  (uses last-seen n, l)

    # Reassemble into row strings by splitting on the Ref code (MK00a etc.)
    # Every data row ends with MK00a (or similar)
    joined = ' '.join(lines)
    # Break into chunks that end with a ref code like MK00a
    # Ref codes are capital-letter sequences followed by digits and optional lowercase
    row_pattern = re.compile(
        r'(?:(\d+)\s+([spdfghi])\s+\d+\s+[A-Z]°?\s+)?'   # optional [n l 2S+1 Term]
        r'(\d+)/(\d+)\s+'                                   # J as fraction
        r'(\d+(?:\.\d+)?)\s+'                              # energy cm^-1
        r'([A-Z]+\d+[a-z]?)'                               # ref code
    )

    for m in row_pattern.finditer(joined):
        n_str, l_str, j_num, j_den, energy_str, _ref = m.groups()
        if n_str:
            current_n = int(n_str)
            current_l = L_SYMBOL_TO_INT.get(l_str)
        if current_n is None or current_l is None:
            continue
        j_val = float(j_num) / float(j_den)
        energy = float(energy_str)
        label = f"{current_n}{'spdfghi'[current_l]}_{j_num}/{j_den}"
        levels.append(Level(current_n, current_l, j_val, energy, label))

    return levels, ionization_cm


# =============================================================================
# ANALYSIS
# =============================================================================

def lamb_shift_from_levels(levels):
    """Find 2s_1/2 and 2p_1/2 and compute their splitting."""
    s2 = next((lv for lv in levels if lv.n == 2 and lv.l == 0 and lv.j == 0.5), None)
    p2 = next((lv for lv in levels if lv.n == 2 and lv.l == 1 and lv.j == 0.5), None)
    if s2 is None or p2 is None:
        return None
    splitting_cm = s2.energy_cm - p2.energy_cm
    splitting_ev = splitting_cm * CM_TO_EV
    splitting_mhz = splitting_ev / H_EV_S / 1e6
    return {
        "s_level_cm": s2.energy_cm,
        "p_level_cm": p2.energy_cm,
        "splitting_cm": splitting_cm,
        "splitting_ev": splitting_ev,
        "splitting_mhz": splitting_mhz,
        "literature_mhz": 1057.845,
    }


def compute_residuals_vs_dirac(levels, ionization_cm):
    """
    For each level, compute (measured binding E) - (Dirac prediction).
    Return array of residuals in eV.
    """
    rows = []
    for lv in levels:
        bind_meas = lv.binding_ev(ionization_cm)
        bind_dirac = lv.dirac_binding_ev()
        resid = bind_meas - bind_dirac
        rows.append({
            "label": lv.label, "n": lv.n, "l": lv.l, "j": lv.j,
            "binding_meas_ev": bind_meas,
            "binding_dirac_ev": bind_dirac,
            "residual_ev": resid,
        })
    return rows


# ---------- Candidate winding-ratio models ----------
# Each returns predicted BINDING energy in eV for level (n, l, j).

def m_rydberg_reduced(n, l, j, R):
    return R / n**2


def m_dirac(n, l, j, R):
    # R here is dummy scale; we use the analytic Dirac expression.
    j_half = j + 0.5
    delta = j_half - np.sqrt(j_half**2 - ALPHA**2)
    n_eff = n - delta
    gamma = (1 + (ALPHA/n_eff)**2) ** (-0.5)
    return M_E_C2 * (1 - gamma)


def m_prism_log(n, l, j, R, k_log):
    base = m_dirac(n, l, j, R)
    correction = R * k_log * ALPHA**2 * np.log(n) / n**3
    return base + correction


def m_prism_log_s(n, l, j, R, k_log, k_s):
    """Log spiral + s-state bonus (only l=0 feels it)."""
    base = m_dirac(n, l, j, R)
    s_bonus = k_s * ALPHA**3 * np.where(np.asarray(l) == 0, 1.0, 0.0) / n**3
    log_term = k_log * ALPHA**2 * np.log(n) / n**3
    return base + R * (log_term + s_bonus)


def m_prism_full(n, l, j, R, k_log, k_s, k_phi):
    """Log spiral + s-state bonus + phi modulation."""
    base = m_dirac(n, l, j, R)
    s_bonus = k_s * ALPHA**3 * np.where(np.asarray(l) == 0, 1.0, 0.0) / n**3
    log_term = k_log * ALPHA**2 * np.log(n) / n**3
    phi_term = k_phi * ALPHA**2 * np.sin(2*PI*np.log(n)/np.log(PHI)) / n**3
    return base + R * (log_term + s_bonus + phi_term)


def fit_model(func, levels, ionization_cm, p0):
    ns = np.array([lv.n for lv in levels], dtype=float)
    ls = np.array([lv.l for lv in levels], dtype=float)
    js = np.array([lv.j for lv in levels], dtype=float)
    Es = np.array([lv.binding_ev(ionization_cm) for lv in levels])

    def packed(X, *params):
        n_, l_, j_ = X
        return func(n_, l_, j_, *params)

    X = (ns, ls, js)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        popt, _ = curve_fit(packed, X, Es, p0=p0, maxfev=30000)

    predicted = packed(X, *popt)
    residuals = Es - predicted
    n_data = len(Es)
    n_params = len(popt)
    rss = np.sum(residuals**2)
    bic = n_data * np.log(rss/n_data + 1e-30) + n_params * np.log(n_data)
    return {
        "params": popt, "residuals": residuals,
        "rms": float(np.sqrt(np.mean(residuals**2))),
        "max_abs": float(np.max(np.abs(residuals))),
        "bic": float(bic), "n_params": n_params,
    }


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 76)
    print("PRISM v3 - REAL NIST DATA")
    print("=" * 76)

    print("\nFetching NIST H I energy levels ...")
    levels, ionization_cm = fetch_nist_h1_levels()
    print(f"  Parsed {len(levels)} levels")
    print(f"  Ionization limit: {ionization_cm} cm^-1 = {ionization_cm*CM_TO_EV:.9f} eV")

    print("\n" + "-" * 76)
    print("PARSED LEVELS (above ground state)")
    print("-" * 76)
    print(f"{'Label':<12} {'n':<3} {'l':<3} {'j':<5} {'E (cm^-1)':<16} {'E (eV)':<12}")
    for lv in levels:
        print(f"{lv.label:<12} {lv.n:<3} {lv.l:<3} {lv.j:<5} "
              f"{lv.energy_cm:<16.4f} {lv.energy_ev:<12.9f}")

    print("\n" + "-" * 76)
    print("LAMB SHIFT (2s_1/2 - 2p_1/2)")
    print("-" * 76)
    ls = lamb_shift_from_levels(levels)
    if ls:
        print(f"  2s_1/2 level:        {ls['s_level_cm']:.4f} cm^-1")
        print(f"  2p_1/2 level:        {ls['p_level_cm']:.4f} cm^-1")
        print(f"  Splitting (cm^-1):   {ls['splitting_cm']:+.4f}")
        print(f"  Splitting (eV):      {ls['splitting_ev']:+.6e}")
        print(f"  Splitting (MHz):     {ls['splitting_mhz']:+.3f}")
        print(f"  Literature (MHz):    {ls['literature_mhz']:.3f}")
        agreement = abs(ls['splitting_mhz'] - ls['literature_mhz']) / ls['literature_mhz']
        print(f"  Agreement:           {(1-agreement)*100:.3f}%")
        print("\n  ** This is the Lamb shift. In Dirac's relativistic QM, 2s_1/2")
        print("     and 2p_1/2 are EXACTLY degenerate. The splitting is pure QED.")
        print("     PRISM's claim: this splitting is geometric, arising from the")
        print("     different 5D scaling-radius exposure of l=0 vs l=1 orbitals. **")

    print("\n" + "-" * 76)
    print("RESIDUALS FROM DIRAC PREDICTION (= QED signal + recoil + nuclear size)")
    print("-" * 76)
    rows = compute_residuals_vs_dirac(levels, ionization_cm)
    print(f"{'Label':<12} {'E_meas (eV)':<16} {'E_Dirac (eV)':<16} {'Residual (eV)':<16}")
    for r in rows:
        print(f"{r['label']:<12} {r['binding_meas_ev']:<16.9f} "
              f"{r['binding_dirac_ev']:<16.9f} {r['residual_ev']:<+16.3e}")

    print("\n" + "-" * 76)
    print("MODEL COMPARISON (lower BIC = better, after penalizing free parameters)")
    print("-" * 76)
    models = {
        "rydberg":      (m_rydberg_reduced, [13.6]),
        "dirac":        (m_dirac,           [13.6]),
        "prism_log":    (m_prism_log,       [13.6, 0.0]),
        "prism_log_s":  (m_prism_log_s,     [13.6, 0.0, 0.0]),
        "prism_full":   (m_prism_full,      [13.6, 0.0, 0.0, 0.0]),
    }
    results = {}
    for name, (func, p0) in models.items():
        try:
            results[name] = fit_model(func, levels, ionization_cm, p0)
        except Exception as e:
            results[name] = {"error": str(e)}

    print(f"{'Model':<16} {'#p':<4} {'RMS (eV)':<16} {'Max (eV)':<16} {'BIC':<12}")
    sorted_res = sorted(
        [(n, r) for n, r in results.items() if "error" not in r],
        key=lambda x: x[1]["bic"],
    )
    for name, r in sorted_res:
        print(f"{name:<16} {r['n_params']:<4} "
              f"{r['rms']:<16.3e} {r['max_abs']:<16.3e} {r['bic']:<12.2f}")

    if sorted_res:
        best_name, best = sorted_res[0]
        print(f"\n  BEST: {best_name}")
        print(f"  Parameters: {best['params']}")

    print("\n" + "=" * 76)
    print("INTERPRETATION")
    print("=" * 76)
    print("""
The data now comes from NIST's critically-evaluated hydrogen reference table
with no tuning or rounding by me. The Lamb shift numerical value that the
pipeline extracts IS the real QED signature that Dirac cannot explain in 4D.

If prism_log or prism_log_s has BIC substantially below dirac, that's
positive signal that a logarithmic-spiral correction earns its keep in
describing the fine-structure pattern.

If prism_full's phi-modulation coefficient comes out statistically
consistent with zero, that RULES OUT the 5-fold-symmetry claim at this
precision - PRISM would need to find its phi signature elsewhere (maybe
in the running of alpha, maybe in the proton radius puzzle, maybe in
the muonic hydrogen data).

This pipeline is now doing real physics: running candidate geometric
models against real measured data and letting the data decide.
""")


if __name__ == "__main__":
    main()
