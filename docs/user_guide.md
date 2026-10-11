# SmartSim user guide

1. Install: `python -m pip install -r requirements.txt` (see README for Device Guard / MSYS64 notes).
2. Run: `python main.py`, then type a number from the menu.
3. Outputs: charts are written to `results/plots/`, the dashboard and validation report to `results/reports/`.

| Option | What it does |
|---|---|
| 1 | Sample spaces, events, classical probability, Bayes |
| 2 | LCG, inverse transform, random-digit mappings and their boundaries |
| 3 | PMF mean/variance, CDF table, exponential probabilities (0.632121, 0.285794, 0.049787) |
| 4 | 25-day (M,N) inventory table: lecture replay and model run, shortage analysis |
| 5 | Newsvendor profits for Q = 40, 50, 60 and sensitivity to the day-type probabilities |
| 6 | Generates all plots and the dashboard |
| 7 | Compares computed values with the lecture and saves a report |
| 9 | Confidence intervals, t-test, variance reduction, Markov chain |
| 10 | Car-service example on the discrete-event engine |

Non-interactive: `python main.py --module 4` or `python main.py --all`.
