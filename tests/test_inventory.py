"""Tests for module3_inventory (Persons 6, 7).

Source numbers: the lecture quotes total 88 / average 3.5, but the table as
transcribed in the plan sums to 123. Both facts are asserted explicitly so
the discrepancy cannot be hidden.
"""

from module3_inventory import (
    InventorySystemMN, analyze_shortage_patterns, average_inventory,
    calculate_shortage_rate, count_shortage_days, find_optimal_M_N,
    generate_demand, generate_lead_time, run_full_simulation,
    sensitivity_analysis, service_level, total_cost)
from module3_inventory.simulation import lecture_history
from tests.helpers import approx

HAND = [  # small hand-made history: ends 2,0,0 / one real shortage day
    {"cycle": 1, "day": 1, "abs_day": 1, "begin": 3, "demand": 1, "end": 2,
     "shortage": 0, "order_qty": None},
    {"cycle": 1, "day": 2, "abs_day": 2, "begin": 2, "demand": 2, "end": 0,
     "shortage": 0, "order_qty": None},      # ends at 0, demand fully served
    {"cycle": 1, "day": 3, "abs_day": 3, "begin": 0, "demand": 2, "end": 0,
     "shortage": 2, "order_qty": 11},
    {"cycle": 1, "day": 4, "abs_day": 4, "begin": 5, "demand": 1, "end": 4,
     "shortage": 0, "order_qty": None},
]


def test_wrappers_use_the_tables():
    assert generate_demand(24) == 1 and generate_demand(92) == 4
    assert generate_lead_time(0) == 3 and generate_lead_time(5) == 1


def test_metrics_on_hand_made_history():
    assert approx(average_inventory(HAND), 6 / 4)
    assert count_shortage_days(HAND) == 1            # end 0 with served demand is not a shortage
    assert approx(calculate_shortage_rate(HAND), 0.25)
    assert approx(service_level(HAND), 0.75)
    assert approx(total_cost(HAND, {"holding": 1, "ordering": 10, "shortage": 5}),
                  6 + 10 + 10)
    assert analyze_shortage_patterns(HAND)["days"] == [(1, 3, 2)]


def test_lecture_table_shortage_days_and_service_level():
    hist = lecture_history()
    assert len(hist) == 25
    assert count_shortage_days(hist) == 2            # cycle 3, days 2 and 3
    assert [(r["cycle"], r["day"]) for r in hist if r["shortage"]] == [(3, 2), (3, 3)]
    assert approx(calculate_shortage_rate(hist), 0.08)
    assert approx(service_level(hist), 0.92)


def test_lecture_table_as_transcribed_sums_to_123_not_88():
    hist = lecture_history()
    total = sum(r["end"] for r in hist)
    assert total == 123                              # documented discrepancy
    assert total != 88
    assert approx(average_inventory(hist), 4.92)


def test_rules_run_first_cycles_match_the_lecture_table():
    rules = run_full_simulation("rules")["history"]
    lecture = lecture_history()
    # Cycle 1, cycle 2 days 1-4, cycles 4 and 5 agree day by day.
    same = [i for i in range(25)
            if (rules[i]["demand"], rules[i]["end"]) == (lecture[i]["demand"], lecture[i]["end"])]
    for i in list(range(0, 9)) + list(range(15, 25)):
        assert i in same, i


def test_model_rules_unit_behaviour():
    s = InventorySystemMN(M=11, N=5, initial=3, pending=(8, 2))
    r1 = s.run_day(24)
    assert (r1["begin"], r1["demand"], r1["end"]) == (3, 1, 2)
    r2 = s.run_day(35)
    assert (r2["begin"], r2["end"]) == (10, 9)       # 2 + 8 arrived
    for rd in (65, 81, 54):
        s.run_day(rd)
    qty, lt = s.place_order(4)
    assert (qty, lt) == (9, 1)                        # 11 - 2
    assert s.history[-1]["order_qty"] == 9


def test_backorder_is_served_first_when_stock_arrives():
    s = InventorySystemMN(M=5, N=3, initial=0, pending=(4, 2))
    s.run_day(50)        # demand 2, no stock -> shortage 2
    assert s.history[0]["shortage"] == 2
    s.run_day(50)        # 4 arrive, 2 backorders cleared, demand 2 served
    assert s.history[1]["end"] == 0 and s.history[1]["shortage"] == 0


def test_optimizer_not_worse_than_baseline_and_reproducible():
    a = find_optimal_M_N(M_values=[9, 11, 13], N_values=[4, 5], replications=5, seed=1)
    b = find_optimal_M_N(M_values=[9, 11, 13], N_values=[4, 5], replications=5, seed=1)
    assert a["best_cost"] <= a["baseline_cost"] + 1e-12
    assert a == b


def test_sensitivity_table_shape():
    rows = sensitivity_analysis(replications=5, seed=1)
    names = [r["scenario"] for r in rows]
    assert "baseline" in names and "lead time +1" in names
    base = next(r for r in rows if r["scenario"] == "baseline")
    higher = next(r for r in rows if r["scenario"] == "demand +1")
    assert higher["avg_inventory"] < base["avg_inventory"]
