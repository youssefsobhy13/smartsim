"""Project constants taken from the BAS221 lectures / SmartSim plan.

Values that the plan does not give (cost rates) are ASSUMED and marked so.
"""

from typing import List, Tuple

# --- Inventory (M,N) system (pages 84-91) ---------------------------------
M_MAX = 11
N_REVIEW = 5
INITIAL_INVENTORY = 3
PENDING_UNITS = 8
PENDING_ARRIVAL_DAY = 2
NUM_CYCLES = 5
TOTAL_DAYS = NUM_CYCLES * N_REVIEW

# Fixed demand random digits used to replay the lecture example.
FIXED_DEMAND_RDS: List[int] = [
    24, 35, 65, 81, 54, 3, 87, 27, 47, 70, 30, 30, 30,
    17, 9, 42, 87, 26, 36, 40, 3, 63, 19, 88, 94,
]

# Lead-time outcomes recorded in the lecture table for the orders placed at
# the end of cycles 1-4 (the lecture gives the outcomes, not the digits).
LECTURE_LEAD_TIMES: List[int] = [1, 3, 1, 1]
# One digit per lead time above, chosen inside the matching range.
LECTURE_LEAD_TIME_RDS: List[int] = [4, 0, 5, 3]

# Demand table (page 86): (demand, probability)
DEMAND_DISTRIBUTION: List[Tuple[int, float]] = [
    (0, 0.10), (1, 0.25), (2, 0.35), (3, 0.21), (4, 0.09),
]
# RD ranges, inclusive, with 00 treated as 100.
DEMAND_RD_RANGES: List[Tuple[int, int, int]] = [
    (1, 10, 0), (11, 35, 1), (36, 70, 2), (71, 91, 3), (92, 100, 4),
]

# Lead-time table (page 88), single digit, 0 treated as 10.
LEAD_TIME_DISTRIBUTION: List[Tuple[int, float]] = [(1, 0.60), (2, 0.30), (3, 0.10)]
LEAD_TIME_RD_RANGES: List[Tuple[int, int, int]] = [(1, 6, 1), (7, 9, 2), (10, 10, 3)]

# --- Newspaper seller (pages 132-134) --------------------------------------
PURCHASE_COST = 0.33
SELLING_PRICE = 0.50
SALVAGE_VALUE = 0.00

# (type, probability, demand, rd_low, rd_high)
NEWSDAY_TABLE = [
    ("Good", 0.35, 40, 0, 34),
    ("Fair", 0.45, 50, 35, 79),
    ("Poor", 0.20, 60, 80, 99),
]
NEWSPAPER_RDS: List[int] = [23, 88, 45, 12, 67, 91, 38, 5, 72, 29]
ORDER_QUANTITIES: List[int] = [40, 50, 60]

# --- Source (lecture) values used by the validation module -----------------
SOURCE_VALUES = {
    "total_ending_inventory": 88,
    "avg_inventory": 3.5,
    "shortage_days": 2,
    "service_level": 0.92,
    "newspaper_40": 6.80,
    "newspaper_50": 6.55,
    "newspaper_60": 4.18,
    "exp_p_lt_1": 0.632121,
    "exp_p_1_to_2_5": 0.285794,
    "exp_p_ge_3": 0.049787,
}

# --- Cost rates (ASSUMED: the plan gives none; documented in the README) ---
HOLDING_COST_PER_UNIT_DAY = 1.0
ORDERING_COST_PER_ORDER = 10.0
SHORTAGE_COST_PER_UNIT = 5.0
