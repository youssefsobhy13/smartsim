"""Tests for module5_statistics, module6_visualization, module7_validation."""

import os
import tempfile

import numpy as np

from module3_inventory import run_full_simulation
from module5_statistics import (
    antithetic_variates, central_limit_theorem, chi_square_test,
    common_random_numbers, control_variates, law_of_large_numbers, mean_ci,
    proportion_ci, steady_state, t_test, transition_matrix)
from module5_statistics.variance_reduction import stratified_sampling
from module6_visualization import (
    create_dashboard, plot_inventory_over_time, plot_pmf_cdf)
from module7_validation import compare_with_source
from module7_validation.validate import validate_distribution_results
from tests.helpers import approx, raises


def test_lln_running_mean_approaches_true_mean():
    rm = law_of_large_numbers(20000, seed=1)
    assert abs(rm[-1] - 1.0) < 0.05
    assert abs(rm[-1] - 1.0) < abs(rm[9] - 1.0) + 0.5


def test_clt_sums_look_normal():
    z = central_limit_theorem(n=100, replications=5000,
                              sampler=lambda rng, size: rng.random(size),
                              mean=0.5, std=np.sqrt(1 / 12), seed=2)
    skew = float(np.mean(((z - z.mean()) / z.std()) ** 3))
    assert abs(skew) < 0.15
    assert abs(z.mean()) < 0.05 and abs(z.std() - 1) < 0.05


def test_ci_covers_true_mean_about_95_percent():
    rng = np.random.default_rng(7)
    hits = 0
    for _ in range(1000):
        lo, hi = mean_ci(rng.normal(10, 2, 30))
        hits += lo <= 10 <= hi
    assert 0.92 < hits / 1000 < 0.98


def test_ci_narrows_with_n():
    rng = np.random.default_rng(3)
    small = mean_ci(rng.normal(0, 1, 20))
    large = mean_ci(rng.normal(0, 1, 2000))
    assert (large[1] - large[0]) < (small[1] - small[0])


def test_proportion_ci_and_tests():
    lo, hi = proportion_ci(23, 25)
    assert lo < 0.92 < hi
    t, p = t_test([3.4, 3.6, 3.5, 3.55, 3.45], 3.5)
    assert abs(t) < 1e-9 and p > 0.99
    chi, p = chi_square_test([25, 25, 25, 25], [0.25, 0.25, 0.25, 0.25])
    assert approx(chi, 0.0) and p > 0.99
    assert raises(ValueError, mean_ci, [1.0])


def test_variance_reduction_reduces_variance():
    f = lambda u: np.exp(u)
    anti = antithetic_variates(f, 2000, seed=1)
    assert anti["var_antithetic"] < anti["var_plain"]
    ctrl = control_variates(f, lambda u: u, 0.5, 2000, seed=1)
    assert ctrl["var_control"] < ctrl["var_plain"]
    strat = stratified_sampling(f, 2000, 10, seed=1)
    assert strat["var_stratified"] < strat["var_plain"]
    crn = common_random_numbers(lambda u: np.exp(u), lambda u: 1.1 * np.exp(u), 2000, seed=1)
    assert crn["var_crn"] < crn["var_independent"]
    assert abs(anti["estimate"] - (np.e - 1)) < 0.01


def test_markov_steady_state():
    p = transition_matrix([[0.9, 0.1], [0.5, 0.5]])
    pi = steady_state(p)
    assert np.allclose(pi @ p, pi) and approx(float(pi.sum()), 1.0)
    assert raises(ValueError, transition_matrix, [[0.5, 0.4], [0.5, 0.5]])


def test_plots_are_saved_as_png():
    hist = run_full_simulation("lecture")["history"]
    with tempfile.TemporaryDirectory() as tmp:
        p1 = plot_inventory_over_time(hist, save_path=os.path.join(tmp, "inv.png"))
        from module1_probability import discrete_rv
        p2 = plot_pmf_cdf(discrete_rv([0, 1, 2], [0.25, 0.5, 0.25]),
                          save_path=os.path.join(tmp, "pmf.png"))
        p3 = create_dashboard(hist, save_path=os.path.join(tmp, "d.html"),
                              force_static=True)
        for path in (p1, p2, p3):
            assert os.path.getsize(path) > 1000


def test_validation_is_honest():
    out = compare_with_source(save=False, verbose=False)
    rows = {r["metric"]: r for r in out["rows"]}
    assert rows["Newspaper (Q=40)"]["match"]
    assert rows["Shortage days [lecture]"]["match"]
    assert rows["Service level [lecture]"]["match"]
    # known source discrepancies must be reported, not hidden
    assert not rows["Total ending inventory [lecture]"]["match"]
    assert approx(rows["Total ending inventory [lecture]"]["diff"], 35)
    assert all(r["match"] for r in validate_distribution_results())
