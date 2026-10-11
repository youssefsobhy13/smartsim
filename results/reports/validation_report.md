# SmartSim validation report

```
Metric                                Source   Computed      Diff  Match
------------------------------------------------------------------------
Total ending inventory [lecture]     88.0000   123.0000  +35.0000  DIFF
Avg inventory [lecture]               3.5000     4.9200   +1.4200  DIFF
Shortage days [lecture]               2.0000     2.0000   +0.0000  OK
Service level [lecture]               0.9200     0.9200   +0.0000  OK
Total ending inventory [rules]       88.0000   141.0000  +53.0000  DIFF
Avg inventory [rules]                 3.5000     5.6400   +2.1400  DIFF
Shortage days [rules]                 2.0000     0.0000   -2.0000  DIFF
Service level [rules]                 0.9200     1.0000   +0.0800  DIFF
Newspaper (Q=40)                      6.8000     6.8000   +0.0000  OK
Newspaper (Q=50)                      6.5500     6.5000   -0.0500  DIFF  (plan RD table gives 6.50; lecture quotes 6.55)
Newspaper (Q=60)                      4.1800     4.2000   +0.0200  DIFF  (plan RD table gives 4.20; lecture quotes 4.18)
P(X<1) Exp                            0.6321     0.6321   -0.0000  OK
P(1<=X<2.5) Exp                       0.2858     0.2858   +0.0000  OK
P(X>=3) Exp                           0.0498     0.0498   +0.0000  OK
------------------------------------------------------------------------
6/14 values match the source exactly (within tolerance).

Reference - exact expected newspaper profit: Q=40: 6.80, Q=50: 6.75, Q=60: 4.45
```

See README 'Known source discrepancies' for why DIFF rows exist.
