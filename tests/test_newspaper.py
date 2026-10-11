"""Tests for module4_newspaper (Person 8)."""

from module4_newspaper import (
    NewspaperSeller, analytic_expected_profit, find_optimal,
    probability_sensitivity, profit_demand_gt_order, profit_demand_le_order,
    test_order_quantities)
from tests.helpers import approx

test_order_quantities.__test__ = False  # imported helper, not a test


def test_profit_formulas():
    assert approx(profit_demand_le_order(40, 50, 0.50, 0.33, 0.0), 40 * 0.50 - 50 * 0.33)
    assert approx(profit_demand_gt_order(50, 0.50, 0.33), 50 * 0.50 - 50 * 0.33)
    assert approx(profit_demand_le_order(30, 40, 0.5, 0.33, 0.1),
                  30 * 0.5 + 10 * 0.1 - 40 * 0.33)


def test_order_40_is_6_80_every_day():
    seller = NewspaperSeller(40)
    rows = seller.simulate()
    assert len(rows) == 10
    assert all(approx(r["profit"], 6.80) for r in rows)
    assert approx(seller.average_profit(), 6.80)


def test_plan_ten_day_table():
    day1 = NewspaperSeller(50).simulate()[0]
    assert (day1["rd"], day1["newsday"], day1["demand"]) == (23, "Good", 40)
    assert approx(day1["profit"], 3.50)
    assert approx(NewspaperSeller(60).simulate()[1]["profit"], 10.20)   # day 2, Poor


def test_averages_from_the_plans_own_daily_table():
    profits = test_order_quantities()
    assert approx(profits[40], 6.80, 0.005)
    assert approx(profits[50], 6.50, 0.005)    # the lecture quotes 6.55 (see README)
    assert approx(profits[60], 4.20, 0.005)    # the lecture quotes 4.18 (see README)
    assert find_optimal(profits) == 40


def test_analytic_expected_profit():
    assert approx(analytic_expected_profit(40), 6.80, 0.005)
    assert approx(analytic_expected_profit(50), 6.75, 0.005)
    assert approx(analytic_expected_profit(60), 4.45, 0.005)


def test_many_days_approach_the_analytic_values():
    sim = test_order_quantities(num_days=20000, seed=5)
    for q in (40, 50, 60):
        assert abs(sim[q] - analytic_expected_profit(q)) < 0.15, q


def test_sensitivity_moves_the_best_q():
    rows = {r["scenario"]: r["best_q"] for r in probability_sensitivity()}
    assert rows["baseline (35/45/20)"] == 40
    assert rows["more poor days (10/30/60)"] == 50
