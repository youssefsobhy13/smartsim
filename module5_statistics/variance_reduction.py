"""Variance-reduction techniques (page 65).

Each function takes a ``seed`` so results are reproducible and returns a dict
containing the plain Monte Carlo variance and the reduced one for comparison.
"""

from typing import Callable, Dict

import numpy as np

Func = Callable[[np.ndarray], np.ndarray]


def common_random_numbers(sim_a: Func, sim_b: Func, n: int = 1000,
                          seed: int = 2025) -> Dict[str, float]:
    """Compare two systems using the same random stream.

    Args:
        sim_a, sim_b: Vectorised functions mapping uniforms to an output.
        n: Number of replications.

    Returns:
        ``mean_diff`` plus the variance of the difference with independent
        streams (``var_independent``) and with common streams (``var_crn``).
    """
    rng = np.random.default_rng(seed)
    u = rng.random(n)
    v = rng.random(n)
    d_ind = sim_a(u) - sim_b(v)
    d_crn = sim_a(u) - sim_b(u)
    return {"mean_diff": float(d_crn.mean()),
            "var_independent": float(d_ind.var(ddof=1)),
            "var_crn": float(d_crn.var(ddof=1))}


def antithetic_variates(f: Func, n: int = 1000, seed: int = 2025) -> Dict[str, float]:
    """Estimate E[f(U)] pairing U with 1-U.

    Returns:
        ``estimate``, ``var_plain`` and ``var_antithetic`` (variances of the
        estimators built from ``2n`` evaluations).
    """
    rng = np.random.default_rng(seed)
    u = rng.random(n)
    anti = 0.5 * (f(u) + f(1 - u))
    plain = f(rng.random(2 * n))
    return {"estimate": float(anti.mean()),
            "var_plain": float(plain.var(ddof=1) / (2 * n)),
            "var_antithetic": float(anti.var(ddof=1) / n)}


def control_variates(f: Func, g: Func, mu_g: float, n: int = 1000,
                     seed: int = 2025) -> Dict[str, float]:
    """Estimate E[f(U)] using ``g(U)`` whose mean ``mu_g`` is known."""
    rng = np.random.default_rng(seed)
    u = rng.random(n)
    fx, gx = f(u), g(u)
    var_g = gx.var(ddof=1)
    c = float(np.cov(fx, gx, ddof=1)[0, 1] / var_g) if var_g > 0 else 0.0
    adjusted = fx - c * (gx - mu_g)
    return {"estimate": float(adjusted.mean()), "coefficient": c,
            "var_plain": float(fx.var(ddof=1) / n),
            "var_control": float(adjusted.var(ddof=1) / n)}


def stratified_sampling(f: Func, n: int = 1000, strata: int = 10,
                        seed: int = 2025) -> Dict[str, float]:
    """Estimate E[f(U)] sampling each of ``strata`` equal-width strata."""
    if strata < 1 or n < strata:
        raise ValueError("need n >= strata >= 1")
    rng = np.random.default_rng(seed)
    per = n // strata
    means, variances = [], []
    for k in range(strata):
        u = (k + rng.random(per)) / strata
        y = f(u)
        means.append(y.mean())
        variances.append(y.var(ddof=1) / per)
    estimate = float(np.mean(means))
    var_strat = float(np.sum(variances) / strata ** 2)
    plain = f(rng.random(per * strata))
    return {"estimate": estimate, "var_plain": float(plain.var(ddof=1) / plain.size),
            "var_stratified": var_strat}
