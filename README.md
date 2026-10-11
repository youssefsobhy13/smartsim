# SmartSim

Integrated educational simulation platform for **BAS221 - Modeling & Simulation**
(Sphinx University). One Python application covering probability, random numbers,
distributions, the (M,N) inventory system, the newspaper seller problem, statistics,
charts, a dashboard and a validation report.

```
python main.py            # interactive menu
python main.py --module 4 # run one option
python main.py --all      # run every option once
```

## Install

```
python -m pip install -r requirements.txt
python -m pytest tests/
```

Python 3.9+. Only NumPy, SciPy and Matplotlib are needed to run everything;
Plotly gives the interactive dashboard (without it a static HTML dashboard is written),
SimPy is optional (cross-checks only), pytest is only for the tests.

### Windows problems you mentioned

**Device Guard blocks `pip install`** - call pip through Python instead of the `pip.exe` launcher,
and prefer a virtual environment:

```
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

If `Activate.ps1` is blocked by the execution policy, do not activate: call
`.venv\Scripts\python.exe` directly as above. If Device Guard still blocks installing packages,
use `python -m pip install --user -r requirements.txt` or ask the university IT to allow-list Python.

**MSYS64 Python has no pip** - use the regular Windows Python, not the MSYS64 one:

```
"C:\Users\ENG _ YOUSSEF\AppData\Local\Programs\Python\Python313\python.exe" -m venv .venv
"C:\Users\ENG _ YOUSSEF\AppData\Local\Programs\Python\Python313\python.exe" -m pip install -r requirements.txt
```

(the path contains spaces, so keep the quotes). `py -3.13 -m pip ...` also works if the Python launcher is installed.
Check which Python you are running with `python -c "import sys; print(sys.executable)"`.

## Project layout

| Folder | Content | Owner |
|---|---|---|
| `config/` | constants (tables, parameters, source values), settings | all |
| `core/` | discrete-event engine: `engine`, `event`, `resource`, `queue`, `process` | P5 |
| `module1_probability/` | sample spaces, events, rules, Bayes, distributions, CDF | P1-3 |
| `module2_random/` | LCG, inverse transform, accept/reject, Box-Muller, digit tables | P4 |
| `module3_inventory/` | (M,N) system, metrics, shortage analysis, optimizer | P6-7 |
| `module4_newspaper/` | newsvendor simulation, profits, optimal Q, sensitivity | P8 |
| `module5_statistics/` | CI, tests, variance reduction, LLN/CLT, Markov chains | P9 |
| `module6_visualization/` | plots (PNG in `results/plots/`), dashboard | P10 |
| `module7_validation/` | comparison with the lecture values | P10 |
| `tests/` | pytest suite (assert-based) | all |

`core/queue.py` keeps the requested name; always import it as `core.queue` and never run scripts from inside `core/`.

## Quick examples

```python
from module1_probability import create_discrete_space, define_event, classical_probability
die = create_discrete_space([1, 2, 3, 4, 5, 6])
classical_probability(define_event(die, lambda x: x % 2 == 0), die)    # 0.5

from module3_inventory import run_full_simulation
run_full_simulation("lecture", verbose=True)

from module4_newspaper import test_order_quantities, find_optimal
find_optimal(test_order_quantities())                                  # 40
```

More in `docs/examples.md`.

## Known source discrepancies (read this)

The SmartSim plan itself flags numbers that do not agree. I could only work from the PDFs you
attached, not from the original lecture pages, so these are **not** silently "fixed". The
validation report (menu option 7, `results/reports/validation_report.md`) shows the real
difference for each.

| Item | Source says | What the code gives | Why |
|---|---|---|---|
| Inventory total ending inventory | 88 | **123** (lecture table replay) | the transcribed End column adds up to 123 (avg 4.92 instead of 3.5) |
| Inventory table vs its own rules | - | model run gives 141, 0 shortage days | RD 30 maps to demand 1 (not 2 as in the table); cycle 2 day 5 ends at 3 (table: 2); lead time 3 arrives day 4 in the table, day 3 in the model |
| Shortage days / service level | 2 / 92% | 2 / 92% (lecture replay) | match |
| Newspaper Q=40 | $6.80 | $6.80 | match |
| Newspaper Q=50 / 60 | $6.55 / $4.18 | $6.50 / $4.20 (plan's 10-day table) | arithmetic of the plan's own daily profits; exact expectation is 6.75 / 4.45 |
| Page-38 mean/variance | 0 / 1.5 / 1.22 | reproduced with PMF `0.15,0.15,0.40,0.15,0.15` on -2..2 | **reconstructed** - the PMF printed on page 38 was not in the files; the slide-10 PMF (0.1,0.2,0.4,0.2,0.1) gives variance 1.2 |
| Loaded die P(<4)=4/9 | 4/9 | weights `1,1,2,2,2,1` (/9) | **illustrative** weights chosen to reproduce 4/9 |

Because of this the project does **not** reproduce 100% of the quoted numbers; it reproduces
everything that can be derived, and reports the rest honestly. Check the flagged rows against
the original pages 94-109, 140 and 38 before you submit; if the lecture itself says 88, update
`LECTURE_TABLE` in `module3_inventory/simulation.py` and `SOURCE_VALUES` in `config/constants.py`.

Inventory lead time model: an order placed at the end of day `d` with lead time `L` arrives at the start of day `d + L`.
Cost rates for the optimizer (holding 1 per unit-day, ordering 10, shortage 5) are **assumed** because the plan gives none; change them in `config/constants.py`.

## Main menu

`[1]` Probability, `[2]` Random numbers, `[3]` Distributions, `[4]` Inventory (M,N), `[5]` Newsvendor,
`[6]` Charts, `[7]` Result verification, `[8]` Exit (the slides use `0`; both work),
plus extras `[9]` Statistics and `[10]` Simulation engine demo.

## Extending

Every module is plain Python with no I/O inside the logic, so it can sit behind a web API
(Flask/FastAPI), a desktop GUI or a mobile backend. `run_full_simulation`, `compare_with_source`
and the `*_plots` functions return plain data/paths that a front end can consume.
