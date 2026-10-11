"""Tests for module2_random (Person 4) and the core engine (Person 5)."""

import random
from collections import Counter

from core import Resource, SimulationEngine
from core.process import run_car_example
from module2_random import (
    LinearCongruentialGenerator, accept_reject, exponential_inverse,
    generate_normal, map_to_demand, map_to_lead_time, map_to_newsday)
from module2_random.random_digits import newsday_demand
from tests.helpers import approx, raises


def test_demand_boundaries():
    expected = {1: 0, 10: 0, 11: 1, 35: 1, 36: 2, 70: 2, 71: 3, 91: 3,
                92: 4, 99: 4, 0: 4}
    for digit, demand in expected.items():
        assert map_to_demand(digit) == demand, digit


def test_lead_time_boundaries():
    for d in range(1, 7):
        assert map_to_lead_time(d) == 1
    for d in (7, 8, 9):
        assert map_to_lead_time(d) == 2
    assert map_to_lead_time(0) == 3


def test_newsday_boundaries():
    assert map_to_newsday(0) == "Good" and map_to_newsday(34) == "Good"
    assert map_to_newsday(35) == "Fair" and map_to_newsday(79) == "Fair"
    assert map_to_newsday(80) == "Poor" and map_to_newsday(99) == "Poor"
    assert [newsday_demand(n) for n in ("Good", "Fair", "Poor")] == [40, 50, 60]


def test_digit_validation():
    assert raises(ValueError, map_to_demand, 100)
    assert raises(ValueError, map_to_lead_time, 10)
    assert raises(ValueError, map_to_newsday, -1)


def test_lcg_reproducible_and_in_range():
    a = LinearCongruentialGenerator(seed=7).generate(50)
    b = LinearCongruentialGenerator(seed=7).generate(50)
    c = LinearCongruentialGenerator(seed=8).generate(50)
    assert a == b and a != c
    assert all(0 <= u < 1 for u in a)


def test_demand_frequencies_within_two_percent():
    gen = LinearCongruentialGenerator(seed=2025)
    counts = Counter(map_to_demand(gen.next_digit()) for _ in range(10000))
    table = {0: 0.10, 1: 0.25, 2: 0.35, 3: 0.21, 4: 0.09}
    for demand, prob in table.items():
        assert abs(counts[demand] / 10000 - prob) < 0.02, demand


def test_exponential_inverse_mean():
    gen = LinearCongruentialGenerator(seed=99)
    xs = [exponential_inverse(gen.next(), 2.0) for _ in range(10000)]
    assert abs(sum(xs) / len(xs) - 0.5) < 0.02


def test_accept_reject_and_box_muller():
    rng = random.Random(3)
    xs = [accept_reject(lambda x: 2 * x, 2.0, (0, 1), rng) for _ in range(4000)]
    assert abs(sum(xs) / len(xs) - 2 / 3) < 0.03          # mean of f(x)=2x is 2/3
    ns = [generate_normal(10, 2, rng) for _ in range(5000)]
    mean = sum(ns) / len(ns)
    assert abs(mean - 10) < 0.15
    var = sum((n - mean) ** 2 for n in ns) / len(ns)
    assert abs(var - 4) < 0.4


# ---- core engine -----------------------------------------------------------
def test_car_example_log_is_exact():
    expected = [
        "Car 1 arrived at 0.00", "Car 2 arrived at 2.00", "Car 3 arrived at 3.00",
        "Car 1 started service at 0.00", "Car 1 left at 5.00",
        "Car 2 started service at 5.00", "Car 2 left at 10.00",
        "Car 3 started service at 10.00", "Car 3 left at 15.00",
    ]
    assert run_car_example()["lecture"] == expected


def test_event_order_ties_and_stop():
    eng = SimulationEngine()
    out = []
    eng.schedule(2, lambda: out.append("b"))
    eng.schedule(1, lambda: out.append("a"))
    eng.schedule(2, lambda: out.append("c"))                  # tie: insertion order
    eng.schedule(2, lambda: out.append("p"), priority=-1)     # tie: priority first
    eng.run()
    assert out == ["a", "p", "b", "c"]
    eng2 = SimulationEngine()
    ran = []
    eng2.schedule(1, lambda: (ran.append(1), eng2.stop()))
    eng2.schedule(2, lambda: ran.append(2))
    eng2.run()
    assert ran == [1]


def test_resource_capacity_one_is_fifo():
    started = []
    server = Resource(1, on_start=started.append)
    assert server.request("A") is True
    assert server.request("B") is False and server.request("C") is False
    assert started == ["A"]
    server.release()
    assert started == ["A", "B"]
    server.release()
    assert started == ["A", "B", "C"]
    assert raises(ValueError, SimulationEngine().schedule, -1, lambda: None)
