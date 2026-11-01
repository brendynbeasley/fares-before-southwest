# Technical notes

This is the technical companion to the [README](README.md). It covers the data, the rules, the full set of test
statistics and how to reproduce everything. Every table is in [results/FINDINGS.md](results/FINDINGS.md).

## The original study

Paul Milgrom and John Roberts, "Limit Pricing and Entry under Incomplete Information: An Equilibrium Analysis,"
*Econometrica* 50(2), March 1982, pp. 443–459. With complete information, pre-entry prices cannot affect a rational
entrant, so there is no limit pricing. When the incumbent's cost is private, its price can signal that cost and
limit pricing arises in equilibrium, but entry can be lower than, equal to or higher than under full information.
In the paper's two-type example (P = 10 − Q, K = 7, incumbent cost 0.5 or 2, entrant cost 1.5 or 2) the low-cost
incumbent produces 7.2 instead of its monopoly 4.75 in a separating equilibrium, the high-cost incumbent produces its
monopoly 4.0, and entry occurs with the prior probability q that the incumbent is high-cost, exactly as with full
information. A pooling equilibrium at 4.75 exists when q lies in (0.273, 0.954) and the chance of a high-cost entrant
exceeds 0.063; entry then occurs with probability 1 − p. `src/paper_example.py` recomputes every number in that
example from the paper's formulas, and they match (`results/paper_example.csv`).

## Headline results

| Test (potential entrant Southwest unless noted) | Estimate | SE | N |
|---|---|---|---|
| Incumbent log fare, threat year (average of quarters 0 to 3) | −0.0505 | 0.0062 | 159,116 route-quarters, 706 threatened routes |
| Same, quarters −4 to −2 (pre-trend) | −0.0078 | 0.0063 | |
| Same, SE clustered by newly served airport | −0.0505 | 0.0177 | 21 airports (control routes are their own clusters) |
| Same, threats starting 2015–2019 | −0.0359 | 0.0077 | 249 threatened routes |
| Same, threats starting 2021–2023 (all began in 2021) | −0.0669 | 0.0099 | 447 threatened routes |
| Same, network incumbents only (no low-fare airlines) | −0.0512 | 0.0060 | 705 threatened routes |
| Further change, first year after Southwest competes | 0.0069 | 0.0086 | |
| Incumbent log passengers, threat year | 0.0266 | 0.0156 | |
| Threat-year fare, routes later entered | −0.0532 | 0.0080 | 362 routes |
| Threat-year fare, routes never entered | −0.0483 | 0.0096 | 344 routes |
| Difference (entered minus never) | −0.0049 | 0.0124 | p = 0.69 |
| Entry within 12 quarters on threat-year fare change, β | 0.0086 | 0.2232 | 701 routes, p = 0.97 |
| Spirit as entrant, threat-year fare | −0.0106 | 0.0032 | 1,188 threatened routes |
| Frontier as entrant, threat-year fare | 0.0049 | 0.0021 | 2,772 threatened routes |

Of the 706 Southwest-threatened routes, 48.3% had Southwest competing within three years, 5.8% saw it fly nonstop,
and the median wait was three quarters.

## Data

- **Tickets:** Bureau of Transportation Statistics, Airline Origin and Destination Survey, DB1B Market, 2014 Q1 to
  2024 Q4 (`Origin_and_Destination_Survey_DB1BMarket_{year}_{quarter}.zip` from
  `transtats.bts.gov/PREZIP/`, about 100 MB each, not committed). `src/build_panel.py` collapses them into
  `data/derived/route_quarter_2014_2019.csv.gz`, `data/derived/route_quarter_2020_2024.csv.gz` (airport pair ×
  quarter, passengers and fare revenue in total, for Southwest, Spirit, Frontier, Allegiant and JetBlue, and for the
  three largest ticketing airlines) and `data/derived/airport_quarter.csv.gz` (airport × airline × quarter,
  passengers the airline itself flew through the airport). These are committed.
- **Prices:** FRED series CPIAUCSL, `data/raw/CPIAUCSL.csv`, downloaded November 1, 2026. Fares are in 2024
  dollars.

## Method

Rules were set before estimation, with two exceptions noted below.

- **Ticket filters:** fares from $25 to $2,500 one way, no bulk fares, one ticketing airline, at most three coupons
  in a direction. Routes are non-directional airport pairs.
- **Routes:** at least 100 miles; present (at least 50 sampled passengers) in at least 32 of the 41 usable quarters;
  at least 100 sampled incumbent passengers a quarter on average. Quarters 2020 Q2 to Q4 are dropped.
- **Presence:** an airline serves an airport once it flies at least 300 sampled passengers to or from it in a quarter,
  two quarters running (the airline must operate the flights itself).
- **Threat and entry:** the threat quarter $`T_r`$ is the first quarter the entrant serves both endpoints. It
  competes from the first of two consecutive quarters in which it sells at least 5% of the route's tickets or carries
  at least 100 sampled nonstop passengers. Threatened routes have $`T_r`$ from 2015 Q1 to 2023 Q4 (not in 2020 Q2 to
  Q4) and no competition by $`T_r`$. Control routes are never served at both ends and never entered. Routes served
  or threatened in 2014 are dropped.
- **Exception:** I first defined entry as nonstop service only. Inspection showed the entrant already selling a
  material share of tickets by connection on routes that definition called merely threatened, which would have
  counted actual competition as a threat. I changed the definition before running the split and entry tests.
- **Network-incumbent fare (robustness, added after the main results were in):** the same fare computed without Southwest,
  Spirit, Frontier, Allegiant and JetBlue, used only in route-quarters with at least 20 such tickets, so that a
  second low-fare airline arriving on a route cannot lower the average by changing the mix.
- **Event study:** with route-by-season effects $`\alpha_{r,s}`$ and quarter effects $`\phi_t`$, swept out by
  alternating projections,

```math
\begin{aligned}
\ln F_{rt} &= \sum_{k \ne -1} \tau_k\, \mathbf{1}[t - T_r = k] + \sum_{j=1}^{3} \lambda_j\, \mathbf{1}[t - E_r \in J_j] \\
&\quad + \alpha_{r,s(t)} + \phi_t + u_{rt}
\end{aligned}
```

  with $`k`$ binned at −8 and +12, $`J_j`$ = quarters 0–3, 4–7 and 8+ after entry, and SEs clustered by route.
  Summary statistics are averages of $`\tau_0`$ to $`\tau_3`$ and of $`\tau_{-4}`$ to $`\tau_{-2}`$.
- **Separating test:** the $`\tau_k`$ are interacted with whether the route was ever entered by 2024 Q4, for threats
  starting by 2021 Q4 (at least 12 later quarters observed).
- **Route-level cut:** $`\Delta_r`$ is the mean log fare in up to four pre-entry quarters from $`T_r`$ minus the
  mean of the four last usable quarters before $`T_r`$, net of the same change in the control routes' season-adjusted
  mean log fare.
- **Entry regression:**

```math
\text{Enter}_r = \beta\,\Delta_r + \gamma' X_r + \delta_{y(r)} + e_r
```

  where Enter is competition within 12 quarters, $`X_r`$ is log distance, log pre-threat incumbent passengers and log
  entrant passengers at the newly served airport, and $`\delta`$ are threat-year effects. Linear probability model,
  SEs clustered by the newly served airport.

## Full entry-regression results (Southwest)

| Specification | Coefficient | SE | p | Routes | Entry rate |
|---|---|---|---|---|---|
| Cut only | 0.0086 | 0.2232 | 0.97 | 701 | 0.479 |
| Cut with route controls | −0.2242 | 0.2092 | 0.28 | 701 | 0.479 |
| Cut, also holding the pre-threat fare | −0.6063 | 0.1946 | 0.002 | 701 | 0.479 |
| Cut, routes not entered in year 1 (entry in quarters 4–15) | −0.0866 | 0.1790 | 0.63 | 521 | 0.319 |
| Cut only, threats starting 2015–2019 | −0.7458 | 0.6249 | 0.23 | 248 | 0.544 |
| Log fare level during the threat | −0.7505 | 0.1480 | < 0.001 | 701 | 0.479 |

The third row conditions on the pre-threat fare, which enters the cut with a negative sign, so a temporarily high
pre-threat fare mechanically produces a large cut; I do not read it as evidence of anything. The 2015–2019 row has
only six clusters.

## Reproducing the results

1. Install the packages (Python 3.12 or later):

   ```bash
   pip install -r requirements.txt
   ```

2. Optional, to rebuild the derived tables from the raw ticket files (about 4 GB of downloads):

   ```bash
   python src/build_panel.py --workers 4
   ```

3. Run the analysis (about three minutes):

   ```bash
   python src/paper_example.py
   python src/limit_pricing.py
   python src/figures.py
   ```

## Repository layout

| Path | What it is |
|---|---|
| [src/build_panel.py](src/build_panel.py) | DB1B quarterly zips to route and airport tables |
| [src/limit_pricing.py](src/limit_pricing.py) | Threat and entry dates, event studies, split test, entry regressions, tables |
| [src/figures.py](src/figures.py) | The two event-study charts, drawn from `results/event_study.csv` |
| [src/paper_example.py](src/paper_example.py) | The paper's Section 2 example, recomputed |
| `results/*.csv`, `results/*.png` | Every number and figure in the README |

## References

- Stanford Graduate School of Business. John Roberts faculty page, and "John Roberts, an Economist Who Transformed
  the Study of Organizations, Dies at 80," school news, March 27, 2026.
- Bain, J. S. (1949). A note on pricing in monopoly and oligopoly. *American Economic Review* 39.
- Friedman, J. (1979). On entry preventing behavior. In *Applied Game Theory*, ed. S. J. Brams, A. Schotter and
  G. Schwödiauer. Physica-Verlag.
- Goolsbee, A. & Syverson, C. (2008). How do incumbents respond to the threat of entry? Evidence from the major
  airlines. *Quarterly Journal of Economics* 123(4).
- Milgrom, P. & Roberts, J. (1982). Limit pricing and entry under incomplete information: An equilibrium analysis.
  *Econometrica* 50(2).
- Milgrom, P. & Roberts, J. (1982). Predation, reputation, and entry deterrence. *Journal of Economic Theory* 27(2).
