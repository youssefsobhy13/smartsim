# API reference

All public functions have Google-style docstrings; `help(function)` shows details.

## core
- `SimulationEngine`: `schedule(delay, callback, priority=0)`, `run(until=None)`, `stop()`, `now`
- `Event(time, priority, seq, callback)`; `Resource(capacity, on_start)`: `request(entity)`, `release()`; `Queue`: `enqueue`, `dequeue`, `len()`
- `core.process.run_car_example(arrivals, service_time)`

## module1_probability
- `create_discrete_space(outcomes)`, `create_continuous_space((lo, hi))`, `product_space(*spaces)`, `SampleSpace.get_size()/contains()`
- `define_event(space, condition)`, `is_subset`, `union`, `intersection`, `complement`
- `classical_probability(event, space, weights=None)`, `addition_rule`, `multiplication_rule`, `complement_rule`
- `conditional_probability(P_A_and_B, P_A)`, `independence_check`, `bayes_theorem(P_B_given_A, P_A, P_B)`
- `discrete_rv(values, probs)` -> `pmf, cdf, mean, variance, std`; `continuous_rv(pdf, support)` / `exponential_rv(lam)` -> `pdf, cdf, probability(a, b), mean`
- `cumulative_distribution(dist)`

## module2_random
- `LinearCongruentialGenerator(seed, a, c, m)`: `next()`, `generate(n)`, `next_digit()`
- `exponential_inverse(u, lam)`, `uniform_inverse(u, a, b)`, `generic_inverse(u, inv_cdf)`
- `accept_reject(pdf, max_pdf, support, rng)`, `generate_normal(mean, std, rng)`
- `generate_digit()`, `map_to_demand(digit)`, `map_to_lead_time(digit)`, `map_to_newsday(digit)`, `newsday_demand(type)`

## module3_inventory
- `InventorySystemMN(M, N, initial, pending)`: `run_day(rd)`, `place_order(lt_rd)`, `run_cycles(n, demand_rds, lead_time_rds, rng)`, `get_metrics()`
- History format: list of dicts with `cycle, day, abs_day, begin, rd_demand, demand, end, shortage, order_qty, lead_time, note` (+ `arrival`, `backorder`)
- `run_full_simulation(mode="rules"|"lecture", verbose)`
- `average_inventory`, `service_level`, `total_cost(history, costs)`, `count_shortage_days`, `calculate_shortage_rate`, `analyze_shortage_patterns`
- `find_optimal_M_N(...)`, `cost_function(M, N)`, `sensitivity_analysis()`

## module4_newspaper
- `NewspaperSeller(order_qty, cost, price, salvage)`: `get_newsday`, `calculate_profit`, `simulate_day`, `simulate`, `average_profit`
- `profit_demand_le_order(demand, Q, p, c, s)`, `profit_demand_gt_order(Q, p, c)`
- `test_order_quantities(quantities)`, `find_optimal()`, `analytic_expected_profit(Q)`, `probability_sensitivity()`

## module5_statistics
- `mean_ci`, `proportion_ci`, `t_test`, `chi_square_test`
- `common_random_numbers`, `antithetic_variates`, `control_variates`, `stratified_sampling`
- `law_of_large_numbers`, `central_limit_theorem`, `transition_matrix`, `steady_state`

## module6_visualization / module7_validation
- `plot_inventory_over_time`, `plot_inventory_cycle`, `plot_shortage_analysis`, `plot_pmf_cdf`, `plot_histogram`, `plot_comparison`, `plot_lln`, `plot_clt` (each returns the PNG path)
- `create_dashboard(history)` (Plotly, static HTML fallback)
- `validate_inventory_results`, `validate_newspaper_results`, `compare_with_source`
