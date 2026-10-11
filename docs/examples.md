# Examples

```python
# Probability
from module1_probability import *
die = create_discrete_space([1, 2, 3, 4, 5, 6])
prime = define_event(die, lambda x: x in (2, 3, 5))
classical_probability(prime, die)                     # 0.5
exponential_rv(1).probability(1, 2.5)                 # 0.285794...

# Random numbers
from module2_random import LinearCongruentialGenerator, map_to_demand
g = LinearCongruentialGenerator(seed=42)
[map_to_demand(g.next_digit()) for _ in range(5)]

# Inventory with your own random digits, reproducible
from module3_inventory import InventorySystemMN
s = InventorySystemMN(M=11, N=5, initial=3, pending=(8, 2))
s.run_cycles(5, rng=LinearCongruentialGenerator(seed=1))
s.get_metrics()

# Optimal (M,N)
from module3_inventory import find_optimal_M_N
find_optimal_M_N(replications=10)["best"]

# Newsvendor
from module4_newspaper import NewspaperSeller
seller = NewspaperSeller(40); seller.simulate(num_days=1000, seed=1)
seller.average_profit()

# Statistics
from module5_statistics import mean_ci
mean_ci([3.4, 3.6, 3.5, 3.9, 3.1])

# Engine
from core.process import run_car_example
print("\n".join(run_car_example()["lecture"]))
```
