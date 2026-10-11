"""SmartSim - main entry point.

Usage:
    python main.py              interactive menu
    python main.py --module 4   run one menu option and exit
    python main.py --all        run every option once (integration run)
"""

import argparse
import sys
from typing import Callable, Dict

MENU = """
+-----------------------------------------+
|   SmartSim - Main Menu                  |
+-----------------------------------------+
|  [1] Probability                        |
|  [2] Random numbers                     |
|  [3] Distributions                      |
|  [4] Inventory (M,N)                    |
|  [5] Newsvendor problem                 |
|  [6] Charts                             |
|  [7] Result verification                |
|  [8] Exit            (0 also exits)     |
|  [9] Statistics (extra)                 |
|  [10] Simulation engine demo (extra)    |
+-----------------------------------------+"""


def _header(title: str) -> None:
    print(f"\n=== {title} ===")


def run_module1() -> None:
    """Probability: sample spaces, events, rules, Bayes."""
    from module1_probability import (
        classical_probability, create_discrete_space, define_event,
        product_space, bayes_theorem, complement_rule)
    _header("Probability")
    die = create_discrete_space([1, 2, 3, 4, 5, 6])
    coin = create_discrete_space(["H", "T"])
    two = product_space(coin, coin)
    print("Die      ", die)
    print("Coin     ", coin)
    print("Two coins", two)
    even = define_event(die, lambda x: x % 2 == 0)
    prime = define_event(die, lambda x: x in (2, 3, 5))
    print(f"{even}  P = {classical_probability(even, die):.2f}")
    print(f"{prime}  P = {classical_probability(prime, die):.2f}")
    one_head = define_event(two, lambda o: "H" in o)
    print(f"Two coins, at least one head: P = {classical_probability(one_head, two):.2f}")
    weights = {1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 1}   # illustrative loaded die
    lt4 = define_event(die, lambda x: x < 4)
    print(f"Loaded die (illustrative weights) P(<4) = "
          f"{classical_probability(lt4, die, weights):.4f}")
    print(f"Complement of 0.3 = {complement_rule(0.3):.1f}")
    print(f"Bayes example P(A|B) = {bayes_theorem(0.9, 0.01, 0.108):.4f}")


def run_module2() -> None:
    """Random numbers: LCG, inverse transform, digit tables."""
    from module2_random import (
        LinearCongruentialGenerator, exponential_inverse, map_to_demand,
        map_to_lead_time, map_to_newsday, generate_normal)
    import random
    _header("Random numbers")
    gen = LinearCongruentialGenerator(seed=42)
    sample = gen.generate(5)
    print("LCG(seed=42):", [round(u, 4) for u in sample])
    print("Exponential inverse of those:", [round(exponential_inverse(u), 4) for u in sample])
    print("Demand map   :", {d: map_to_demand(d) for d in (1, 10, 11, 35, 36, 70, 71, 91, 92, 99, 0)})
    print("Lead-time map:", {d: map_to_lead_time(d) for d in range(10)})
    print("Newsday map  :", {d: map_to_newsday(d) for d in (0, 34, 35, 79, 80, 99)})
    rng = random.Random(1)
    print("Box-Muller N(10, 2):", [round(generate_normal(10, 2, rng), 3) for _ in range(3)])


def run_module3() -> None:
    """Distributions: PMF stats and exponential probabilities."""
    from module1_probability import discrete_rv, exponential_rv, cumulative_distribution
    _header("Distributions")
    two = discrete_rv([0, 1, 2], [0.25, 0.5, 0.25])
    print(f"Two-coin PMF: mean={two.mean():.2f} var={two.variance():.2f} std={two.std():.2f}")
    p38 = discrete_rv([-2, -1, 0, 1, 2], [0.15, 0.15, 0.40, 0.15, 0.15])
    print(f"PMF consistent with page-38 numbers (reconstructed): mean={p38.mean():.2f} "
          f"var={p38.variance():.2f} std={p38.std():.2f}")
    print("CDF table:", cumulative_distribution(two))
    e = exponential_rv(1.0)
    print(f"Exponential f(x)=e^-x: P(X<1)={e.cdf(1):.6f}  "
          f"P(1<=X<2.5)={e.probability(1, 2.5):.6f}  P(X>=3)={1 - e.cdf(3):.6f}  P(X=3)=0")


def run_module4() -> None:
    """Inventory (M,N): lecture replay, model run, analysis."""
    from module3_inventory import run_full_simulation, analyze_shortage_patterns
    _header("Inventory (M,N) - lecture table replay")
    lec = run_full_simulation("lecture", verbose=True)
    _header("Inventory (M,N) - model run with the same RDs")
    run_full_simulation("rules", verbose=True)
    print("\nShortage pattern (lecture table):", analyze_shortage_patterns(lec["history"]))
    print("NOTE: the transcribed lecture table sums to 123, not 88 - see README.")


def run_module5() -> None:
    """Newsvendor: profits per order quantity."""
    from module4_newspaper import (
        test_order_quantities, find_optimal, analytic_expected_profit,
        probability_sensitivity)
    _header("Newsvendor problem")
    sim = test_order_quantities()
    print(f"{'Q':>4} {'10-day sim':>11} {'Exact E[profit]':>16} {'Lecture':>8}")
    lecture = {40: 6.80, 50: 6.55, 60: 4.18}
    for q in (40, 50, 60):
        print(f"{q:>4} {sim[q]:>11.2f} {analytic_expected_profit(q):>16.2f} {lecture[q]:>8.2f}")
    print(f"Best order quantity: {find_optimal(sim)}")
    for row in probability_sensitivity():
        print(f"  {row['scenario']:<28} best Q = {row['best_q']}")


def run_module6() -> None:
    """Charts: PNGs in results/plots and the dashboard."""
    from module3_inventory import run_full_simulation
    from module1_probability import discrete_rv
    from module5_statistics import law_of_large_numbers, central_limit_theorem
    from module6_visualization import (
        plot_inventory_over_time, plot_inventory_cycle, plot_shortage_analysis,
        plot_pmf_cdf, plot_histogram, plot_comparison, plot_lln, plot_clt,
        create_dashboard)
    _header("Charts")
    hist = run_full_simulation("lecture")["history"]
    paths = [
        plot_inventory_over_time(hist), plot_inventory_cycle(hist, 3),
        plot_shortage_analysis(hist),
        plot_pmf_cdf(discrete_rv([0, 1, 2], [0.25, 0.5, 0.25])),
        plot_histogram([r["demand"] for r in hist], bins=5, title="Demand histogram"),
        plot_comparison(), plot_lln(law_of_large_numbers(2000)),
        plot_clt(central_limit_theorem(n=30)),
        create_dashboard(hist),
    ]
    for p in paths:
        print("saved", p)


def run_module7() -> None:
    """Result verification against the lecture."""
    from module7_validation import compare_with_source
    _header("Result verification")
    compare_with_source()


def run_statistics() -> None:
    """Statistics: CI, tests, variance reduction, Markov chain."""
    import numpy as np
    from module2_random import LinearCongruentialGenerator
    from module3_inventory import InventorySystemMN
    from module5_statistics import (
        mean_ci, proportion_ci, t_test, antithetic_variates, steady_state)
    _header("Statistics")
    averages, shortage_days = [], 0
    for seed in range(30):
        s = InventorySystemMN(11, 5, 3, (8, 2))
        s.run_cycles(5, rng=LinearCongruentialGenerator(seed=1000 + seed))
        m = s.get_metrics()
        averages.append(m["average_inventory"])
        shortage_days += m["shortage_days"]
    lo, hi = mean_ci(averages)
    print(f"Average inventory over 30 runs: {np.mean(averages):.2f}, 95% CI [{lo:.2f}, {hi:.2f}]")
    lo, hi = proportion_ci(30 * 25 - shortage_days, 30 * 25)
    print(f"Service level 95% CI: [{lo:.3f}, {hi:.3f}]")
    print("t-test mean == 3.5: t=%.3f p=%.3f" % t_test(averages, 3.5))
    r = antithetic_variates(lambda u: np.exp(u), 2000)
    print(f"Antithetic E[e^U]: {r['estimate']:.4f} (true 1.7183); "
          f"variance {r['var_plain']:.2e} -> {r['var_antithetic']:.2e}")
    print("Markov steady state [[.9,.1],[.5,.5]]:", steady_state([[.9, .1], [.5, .5]]).round(4))


def run_engine() -> None:
    """Discrete-event engine: the car-service example (pages 157-159)."""
    from core.process import run_car_example
    _header("Simulation engine - car example")
    print("\n".join(run_car_example()["lecture"]))


def run_module8() -> None:
    """Extras: statistics and the simulation engine."""
    run_statistics()
    run_engine()


ACTIONS: Dict[str, Callable[[], None]] = {
    "1": run_module1, "2": run_module2, "3": run_module3, "4": run_module4,
    "5": run_module5, "6": run_module6, "7": run_module7,
    "9": run_statistics, "10": run_engine,
}


def show_main_menu() -> None:
    """Menu loop."""
    while True:
        print(MENU)
        try:
            choice = input("Choose an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if choice in ("0", "8"):
            print("Goodbye!")
            return
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid option, try again.")
            continue
        try:
            action()
        except ImportError as exc:   # a module is missing / dependency not installed
            print(f"Module unavailable: {exc}")


def main(argv=None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="SmartSim simulation platform")
    parser.add_argument("--module", choices=sorted(ACTIONS, key=int),
                        help="run a single menu option and exit")
    parser.add_argument("--all", action="store_true", help="run every option once")
    args = parser.parse_args(argv)
    if args.all:
        for key in sorted(ACTIONS, key=int):
            ACTIONS[key]()
        return 0
    if args.module:
        ACTIONS[args.module]()
        return 0
    show_main_menu()
    return 0


if __name__ == "__main__":
    sys.exit(main())
