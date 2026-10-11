"""Module 2 - random number generation (Person 4)."""

from module2_random.lcg import LinearCongruentialGenerator
from module2_random.inverse_transform import (
    exponential_inverse, uniform_inverse, generic_inverse)
from module2_random.acceptance_rejection import accept_reject
from module2_random.box_muller import generate_normal
from module2_random.random_digits import (
    generate_digit, map_to_demand, map_to_lead_time, map_to_newsday,
    newsday_demand)
