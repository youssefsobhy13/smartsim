"""Tests for module1_probability (Persons 1, 2, 3)."""

from module1_probability import (
    addition_rule, bayes_theorem, classical_probability, complement,
    complement_rule, conditional_probability, create_continuous_space,
    create_discrete_space, cumulative_distribution, define_event, discrete_rv,
    exponential_rv, independence_check, intersection, is_subset,
    multiplication_rule, product_space, union)
from tests.helpers import approx, raises

DIE = create_discrete_space([1, 2, 3, 4, 5, 6])
COIN = create_discrete_space(["H", "T"])


# ---- Person 1: sample spaces and events -----------------------------------
def test_dice_coin_two_coins_spaces():
    assert DIE.outcomes == frozenset({1, 2, 3, 4, 5, 6})
    assert COIN.outcomes == frozenset({"H", "T"})
    assert product_space(COIN, COIN).outcomes == frozenset({"HH", "HT", "TH", "TT"})
    assert repr(product_space(COIN, COIN)) == "S = {HH, HT, TH, TT}"


def test_even_numbers_event():
    even = define_event(DIE, lambda x: x % 2 == 0)
    assert even.outcomes == frozenset({2, 4, 6})
    assert repr(even) == "E = {2, 4, 6}"


def test_continuous_flash_recycle_space():
    s = create_continuous_space((0, float("inf")))
    assert repr(s) == "S = {x | x > 0}"
    assert s.contains(3.2) and not s.contains(-1)
    assert s.get_size() == float("inf")


def test_discrete_space_validation():
    assert raises(ValueError, create_discrete_space, [])
    assert raises(ValueError, create_discrete_space, [1, 1, 2])


def test_set_operations_and_edge_cases():
    even = define_event(DIE, lambda x: x % 2 == 0)
    low = define_event(DIE, lambda x: x < 4)
    assert union(even, low).outcomes == frozenset({1, 2, 3, 4, 6})
    assert intersection(even, low).outcomes == frozenset({2})
    assert complement(complement(even)) == even          # complement of complement
    assert define_event(DIE, lambda x: False).outcomes == frozenset()   # empty event
    assert define_event(DIE, lambda x: True).outcomes == DIE.outcomes   # full space
    assert is_subset(even, DIE)
    other = define_event(COIN, lambda x: x == "H")
    assert raises(ValueError, union, even, other)


# ---- Person 2: rules, conditional, Bayes -----------------------------------
def test_classical_probabilities():
    even = define_event(DIE, lambda x: x % 2 == 0)
    prime = define_event(DIE, lambda x: x in (2, 3, 5))
    assert approx(classical_probability(even, DIE), 0.5)
    assert approx(classical_probability(prime, DIE), 0.5)
    two = product_space(COIN, COIN)
    one_head = define_event(two, lambda o: "H" in o)
    assert approx(classical_probability(one_head, two), 0.75)


def test_loaded_die_and_non_uniform_outcomes():
    # Illustrative weights (the original page-21 weights were not available):
    # chosen so that P(<4) = 4/9, the lecture result.
    weights = {1: 1 / 9, 2: 1 / 9, 3: 2 / 9, 4: 2 / 9, 5: 2 / 9, 6: 1 / 9}
    lt4 = define_event(DIE, lambda x: x < 4)
    assert approx(classical_probability(lt4, DIE, weights), 4 / 9)
    abc = create_discrete_space(["a", "b", "c"])
    ev = define_event(abc, lambda x: x in ("a", "b"))
    assert approx(classical_probability(ev, abc, {"a": 0.1, "b": 0.3, "c": 0.6}), 0.4)


def test_rules_by_hand():
    assert approx(addition_rule(0.5, 0.5, 0.25), 0.75)
    assert approx(multiplication_rule(0.5, 0.4), 0.2)
    assert approx(complement_rule(0.3), 0.7)
    assert approx(conditional_probability(0.2, 0.4), 0.5)
    assert independence_check(0.5, 0.4, 0.2)
    assert not independence_check(0.5, 0.4, 0.3)
    assert approx(bayes_theorem(0.9, 0.01, 0.108), 0.9 * 0.01 / 0.108)


def test_probability_validation():
    assert raises(ValueError, complement_rule, 1.2)
    assert raises(ValueError, addition_rule, -0.1, 0.5, 0.0)
    assert raises(ValueError, conditional_probability, 0.2, 0.0)
    assert raises(ValueError, bayes_theorem, 0.5, 0.5, 0.0)


# ---- Person 3: distributions ----------------------------------------------
def test_pmf_sum_and_two_coin_moments():
    two = discrete_rv([0, 1, 2], [0.25, 0.5, 0.25])
    assert approx(sum(two.probabilities), 1.0)
    assert approx(two.mean(), 1.0) and approx(two.variance(), 0.5)
    assert raises(ValueError, discrete_rv, [0, 1], [0.5, 0.4])


def test_page38_style_pmf_moments():
    # PMF reconstructed to reproduce the page-38 results (mean 0, var 1.5).
    p38 = discrete_rv([-2, -1, 0, 1, 2], [0.15, 0.15, 0.40, 0.15, 0.15])
    assert approx(p38.mean(), 0.0)
    assert approx(p38.variance(), 1.5)
    assert approx(p38.std(), 1.22, tol=0.005)


def test_cdf_table():
    two = discrete_rv([0, 1, 2], [0.25, 0.5, 0.25])
    assert cumulative_distribution(two) == [(0, 0.25), (1, 0.75), (2, 1.0)]
    assert two.pmf(5) == 0.0 and approx(two.cdf(1), 0.75)


def test_exponential_probabilities():
    e = exponential_rv(1.0)
    assert approx(e.cdf(1), 0.632121)
    assert approx(e.probability(1, 2.5), 0.285794)
    assert approx(1 - e.cdf(3), 0.049787)
    assert approx(e.probability(3, 3), 0.0)          # P(X=3) = 0
    assert approx(e.mean(), 1.0, tol=1e-6)


def test_numeric_integration_matches_closed_form():
    from module1_probability import continuous_rv
    import math
    numeric = continuous_rv(lambda x: math.exp(-x), (0, float("inf")))
    assert approx(numeric.cdf(1), 0.632121)
    assert approx(numeric.probability(1, 2.5), 0.285794)
