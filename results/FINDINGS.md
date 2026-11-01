# Milgrom and Roberts (1982) on airline routes: findings

## In plain English

In 1982 Paul Milgrom and John Roberts showed that a dominant firm can rationally cut its price before a rival
arrives, to signal that its costs are low, but that a rational rival sees through the signal, so the cut need not
keep it out. I tested both halves on US airline routes from 2014 to 2024, treating Southwest's arrival at both ends
of a route as the threat.

- **Incumbents cut fares when Southwest surrounds a route.** On routes led by American, United and Delta, fares
  fell by 5 to 7% in the year after Southwest began serving both airports, before it sold a meaningful share of tickets on the
  route. Out of Cincinnati in 2017 the average cut was 15% (14% for the network airlines alone, since Frontier
  grew there at the same time).
- **The cut did not sort routes the way a signal would.** Routes Southwest later entered had seen the same fare cut
  as routes it never entered (5.2% against 4.7%), so the cut did not reveal which incumbents were vulnerable.
- **Bigger cuts did not keep Southwest out.** Southwest competed within three years on 47% of the quarter of routes
  with the largest cuts and on 45% of the quarter with the smallest cuts or outright rises.
- **Spirit and Frontier draw almost no response.** Incumbents cut fares by about 1% when Spirit surrounded a route
  and not at all for Frontier.

A friendlier tour is in the [README](../README.md). The rest of this page is the technical detail.

**Key to the labels below.** *Threat quarter* (k = 0) = the first quarter the entrant has regular service at both
endpoint airports without competing on the route. *Competing* or *entry* = the entrant sells at least 5% of the
route's tickets or flies it nonstop, two quarters running. *Threat-year fare* = the average of the event-study
coefficients for quarters 0 to 3, in log points, relative to quarter −1. *Change, net of controls* ($`\Delta_r`$) =
the route's change in mean log incumbent fare from the four quarters before the threat to up to four pre-entry
quarters after, minus the same change on routes the entrant never reached. *Incumbents* = every airline except the
entrant. *Network incumbents* = every airline except Southwest, Spirit, Frontier, Allegiant and JetBlue. Fares are 2024 dollars. Passenger counts in the route table are sample counts times ten.

## Main estimates (results/threat_summary.csv)

|  | Southwest | Spirit | Frontier |
|---|---|---|---|
| Threatened routes | 706 | 1,188 | 2,772 |
| Control routes | 3,249 | 5,811 | 2,931 |
| Route-quarters | 159,116 | 283,032 | 230,378 |
| Fare, threat year (log points) | -0.0505 | -0.0106 | 0.0049 |
|   SE | 0.0062 | 0.0032 | 0.0021 |
| Fare, quarters -4 to -2 | -0.0078 | -0.0125 | 0.0111 |
|   SE | 0.0063 | 0.0035 | 0.0020 |
| Fare, first year after entry | 0.0069 | 0.0304 | 0.0170 |
|   SE | 0.0086 | 0.0082 | 0.0061 |
| Passengers, threat year | 0.0266 | -0.0020 | -0.0135 |
|   SE | 0.0156 | 0.0062 | 0.0048 |
| Passengers, quarters -4 to -2 | -0.0364 | 0.0141 | -0.0175 |
|   SE | 0.0168 | 0.0079 | 0.0045 |
| Passengers, first year after entry | -0.0131 | -0.0370 | -0.0772 |
|   SE | 0.0269 | 0.0197 | 0.0163 |
| Threatened routes, threats by 2021 Q4 | 706 | 723 | 2,686 |
| Share competing within 3 years | 0.483 | 0.241 | 0.115 |
| Share flying nonstop within 3 years | 0.058 | 0.095 | 0.048 |
| Share ever competing by 2024 Q4 | 0.513 | 0.335 | 0.166 |
| Median quarters to entry | 3 | 6 | 7 |
| Fare, threat year, later entered | -0.0532 | -0.0151 | 0.0183 |
|   SE | 0.0080 | 0.0083 | 0.0044 |
| Fare, threat year, never entered | -0.0483 | -0.0171 | 0.0052 |
|   SE | 0.0096 | 0.0052 | 0.0023 |
| Difference | -0.0049 | 0.0020 | 0.0132 |
|   SE | 0.0124 | 0.0098 | 0.0050 |
|   p | 0.694 | 0.836 | 0.008 |
| Routes later entered | 362 | 242 | 446 |
| Routes never entered | 344 | 481 | 2,240 |
| Threats 2015-19: fare, later entered | -0.0461 | -0.0089 | 0.0152 |
|   SE | 0.0086 | 0.0093 | 0.0041 |
| Threats 2015-19: fare, never entered | -0.0196 | 0.0080 | 0.0009 |
|   SE | 0.0137 | 0.0058 | 0.0022 |
| Threats 2015-19: routes entered / never | 152 / 97 | 186 / 320 | 410 / 2022 |

## Event-study coefficients, incumbent log fare (results/event_study.csv)

Quarter −1 is the reference. End points pool earlier (≤ −8) and later (≥ 12) quarters. Standard errors are in the
CSV.

| Quarter k | Southwest, all | Southwest, later entered | Southwest, never entered | Spirit, all | Frontier, all |
|---|---|---|---|---|---|
| -8 | 0.0432 | 0.0489 | 0.0367 | 0.0009 | 0.0219 |
| -7 | 0.0174 | 0.0063 | 0.0281 | -0.0003 | 0.0213 |
| -6 | 0.0215 | 0.0103 | 0.033 | 0.0012 | 0.0242 |
| -5 | 0.0198 | 0.0135 | 0.0257 | 0.0011 | 0.0189 |
| -4 | 0.0093 | -0.0033 | 0.023 | -0.0063 | 0.0149 |
| -3 | -0.033 | -0.0365 | -0.0282 | -0.0175 | 0.0102 |
| -2 | 0.0002 | -0.0075 | 0.0113 | -0.0137 | 0.0082 |
| -1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 0 | -0.046 | -0.0459 | -0.0468 | -0.0025 | 0.0083 |
| 1 | -0.0656 | -0.077 | -0.0543 | -0.0187 | 0.0055 |
| 2 | -0.0482 | -0.0516 | -0.0454 | -0.0152 | 0.0003 |
| 3 | -0.042 | -0.0381 | -0.0467 | -0.006 | 0.0054 |
| 4 | -0.0499 | -0.0403 | -0.0602 | 0.0028 | 0.0034 |
| 5 | -0.0681 | -0.0475 | -0.0873 | -0.0055 | 0.0019 |
| 6 | -0.0708 | -0.0514 | -0.0886 | -0.0005 | 0.0048 |
| 7 | -0.0498 | -0.0305 | -0.0687 | 0.0011 | 0.0025 |
| 8 | -0.0506 | -0.0326 | -0.0674 | -0.0021 | 0.0124 |
| 9 | -0.0605 | -0.0607 | -0.0618 | -0.0053 | 0.0165 |
| 10 | -0.0561 | -0.0637 | -0.0502 | -0.0111 | 0.0128 |
| 11 | -0.0494 | -0.058 | -0.0426 | -0.0152 | -0.0011 |
| 12 | -0.0912 | -0.0941 | -0.0919 | -0.0309 | -0.0066 |

## Robustness (results/robustness.csv)

| Entrant | Sample | Threat-year fare | SE | Pre-trend (k = -4 to -2) | SE | Threatened routes |
|---|---|---|---|---|---|---|
| Southwest | all threats, SE by route | -0.0505 | 0.0062 | -0.0078 | 0.0063 | 706 |
| Southwest | all threats, SE by newly served airport | -0.0505 | 0.0177 | -0.0078 | 0.0152 | 706 |
| Southwest | threats starting 2015-2019 only | -0.0359 | 0.0077 | -0.007 | 0.0058 | 249 |
| Southwest | threats starting 2021-2023 only | -0.0669 | 0.0099 | 0.0225 | 0.0143 | 447 |
| Southwest | network incumbents only (no low-fare airlines) | -0.0512 | 0.006 | -0.0049 | 0.0061 | 705 |
| Spirit | all threats, SE by route | -0.0106 | 0.0032 | -0.0125 | 0.0035 | 1188 |
| Spirit | all threats, SE by newly served airport | -0.0106 | 0.0081 | -0.0125 | 0.0097 | 1188 |
| Spirit | threats starting 2015-2019 only | 0.0012 | 0.005 | 0.0023 | 0.0044 | 506 |
| Spirit | threats starting 2021-2023 only | -0.0181 | 0.0042 | -0.0243 | 0.0052 | 682 |
| Spirit | network incumbents only (no low-fare airlines) | -0.0168 | 0.0033 | -0.0133 | 0.0035 | 1184 |
| Frontier | all threats, SE by route | 0.0049 | 0.0021 | 0.0111 | 0.002 | 2772 |
| Frontier | all threats, SE by newly served airport | 0.0049 | 0.0053 | 0.0111 | 0.0054 | 2772 |
| Frontier | threats starting 2015-2019 only | 0.0024 | 0.002 | 0.0091 | 0.0019 | 2432 |
| Frontier | threats starting 2021-2023 only | 0.0342 | 0.0107 | 0.0232 | 0.0139 | 340 |
| Frontier | network incumbents only (no low-fare airlines) | 0.0133 | 0.002 | 0.0117 | 0.002 | 2742 |

## Does a bigger cut keep the entrant out? (results/entry_regression.csv)

Linear probability of competing within 12 quarters of the threat; threats starting by 2021 Q4; SEs clustered by
the newly served airport. A positive coefficient on the cut means larger cuts (more negative) went with less entry,
the separating-equilibrium prediction. The row holding the pre-threat fare is mechanical, because that fare enters
the cut with a negative sign.

| Entrant | Specification | Regressor | Coefficient | SE | p | Routes | Clusters | Entry rate |
|---|---|---|---|---|---|---|---|---|
| Southwest | cut only | cut | 0.0086 | 0.2232 | 0.9693 | 701 | 21 | 0.4793 |
| Southwest | cut with route controls | cut | -0.2242 | 0.2092 | 0.2839 | 701 | 21 | 0.4793 |
| Southwest | cut, also holding the pre-threat fare | cut | -0.6063 | 0.1946 | 0.0018 | 701 | 21 | 0.4793 |
| Southwest | cut, routes not entered in year 1 | cut | -0.0866 | 0.179 | 0.6285 | 521 | 21 | 0.3186 |
| Southwest | cut only, threats starting 2015-2019 | cut | -0.7458 | 0.6249 | 0.2327 | 248 | 6 | 0.5444 |
| Southwest | fare level during threat | ln_post_fare | -0.7505 | 0.148 | 0.0 | 701 | 21 | 0.4793 |
| Spirit | cut only | cut | 0.3476 | 0.1316 | 0.0082 | 723 | 25 | 0.2407 |
| Spirit | cut with route controls | cut | 0.0732 | 0.1448 | 0.6132 | 723 | 25 | 0.2407 |
| Spirit | cut, also holding the pre-threat fare | cut | 0.0579 | 0.1506 | 0.7004 | 723 | 25 | 0.2407 |
| Spirit | cut, routes not entered in year 1 | cut | -0.2684 | 0.1398 | 0.055 | 625 | 24 | 0.1584 |
| Spirit | cut only, threats starting 2015-2019 | cut | 0.3812 | 0.2076 | 0.0662 | 506 | 19 | 0.2352 |
| Spirit | fare level during threat | ln_post_fare | -0.0625 | 0.1058 | 0.5551 | 723 | 25 | 0.2407 |
| Frontier | cut only | cut | -0.0397 | 0.089 | 0.6555 | 2684 | 51 | 0.1155 |
| Frontier | cut with route controls | cut | -0.1834 | 0.0856 | 0.0322 | 2684 | 51 | 0.1155 |
| Frontier | cut, also holding the pre-threat fare | cut | -0.1742 | 0.0855 | 0.0417 | 2684 | 51 | 0.1155 |
| Frontier | cut, routes not entered in year 1 | cut | 0.0234 | 0.0746 | 0.7543 | 2534 | 51 | 0.0762 |
| Frontier | cut only, threats starting 2015-2019 | cut | 0.0362 | 0.0768 | 0.6368 | 2430 | 46 | 0.1128 |
| Frontier | fare level during threat | ln_post_fare | -0.0068 | 0.0495 | 0.891 | 2684 | 51 | 0.1155 |

## Entry by size of the cut (results/entry_by_cut_quartile.csv)

| Entrant | Threat-year fare change | Routes | Mean change (log points) | Entry within 3 years | Mean change (%) |
|---|---|---|---|---|---|
| Southwest | largest cuts | 176 | -0.229 | 0.466 | -20.495 |
| Southwest | second | 175 | -0.076 | 0.474 | -7.36 |
| Southwest | third | 175 | -0.0 | 0.531 | -0.047 |
| Southwest | smallest cuts or rises | 175 | 0.098 | 0.446 | 10.31 |
| Spirit | largest cuts | 181 | -0.128 | 0.243 | -12.025 |
| Spirit | second | 181 | -0.024 | 0.188 | -2.39 |
| Spirit | third | 180 | 0.031 | 0.211 | 3.151 |
| Spirit | smallest cuts or rises | 181 | 0.121 | 0.32 | 12.862 |
| Frontier | largest cuts | 671 | -0.114 | 0.116 | -10.779 |
| Frontier | second | 671 | -0.019 | 0.112 | -1.858 |
| Frontier | third | 671 | 0.027 | 0.113 | 2.703 |
| Frontier | smallest cuts or rises | 671 | 0.097 | 0.121 | 10.142 |

## Southwest threats by largest incumbent (results/southwest_by_incumbent.csv)

Airlines with at least 10 threatened routes.

| Largest incumbent | Routes | Mean change (log points) | Median pre-threat fare ($) | Entry within 3 years | Mean change (%) |
|---|---|---|---|---|---|
| American | 240 | -0.059 | 362.872 | 0.504 | -5.769 |
| United | 208 | -0.054 | 353.288 | 0.336 | -5.229 |
| Delta | 118 | -0.069 | 356.433 | 0.5 | -6.702 |
| Alaska | 45 | 0.023 | 339.268 | 0.622 | 2.358 |
| Allegiant | 28 | -0.047 | 188.057 | 0.607 | -4.622 |
| Hawaiian | 27 | -0.023 | 429.322 | 0.778 | -2.287 |
| JetBlue | 12 | 0.0 | 219.592 | 0.667 | 0.007 |

## Southwest threats by newly served airport (results/southwest_by_new_airport.csv)

| Newly served airport | Routes | Threat began | Mean change (log points) | Entry within 3 years | Mean change (%) | Network incumbents, mean change (log points) | Network incumbents, mean change (%) |
|---|---|---|---|---|---|---|---|
| ORD | 80 | 2021 Q1 | -0.092 | 0.225 | -8.768 | -0.106 | -10.086 |
| HNL | 70 | 2019 Q1 | -0.009 | 0.443 | -0.875 | -0.01 | -1.006 |
| IAH | 70 | 2021 Q2 | -0.068 | 0.271 | -6.586 | -0.077 | -7.425 |
| CVG | 50 | 2017 Q2 | -0.168 | 0.56 | -15.448 | -0.147 | -13.678 |
| SAV | 45 | 2021 Q1 | -0.061 | 0.4 | -5.878 | -0.08 | -7.693 |
| OGG | 44 | 2019 Q2 | -0.018 | 0.523 | -1.748 | -0.021 | -2.058 |
| SYR | 43 | 2021 Q4 | -0.107 | 0.419 | -10.188 | -0.109 | -10.327 |
| KOA | 39 | 2019 Q2 | 0.042 | 0.59 | 4.277 | 0.039 | 3.951 |
| VPS | 37 | 2021 Q2 | -0.065 | 0.486 | -6.304 | -0.042 | -4.096 |
| LIH | 33 | 2019 Q4 | 0.049 | 0.667 | 5.024 | 0.046 | 4.671 |
| EUG | 31 | 2021 Q3 | 0.052 | 0.677 | 5.305 | 0.046 | 4.677 |
| BZN | 30 | 2021 Q2 | -0.092 | 0.8 | -8.82 | -0.102 | -9.664 |
| MYR | 27 | 2021 Q2 | -0.125 | 0.444 | -11.731 | -0.082 | -7.851 |
| FAT | 24 | 2021 Q2 | -0.019 | 0.5 | -1.862 | -0.025 | -2.468 |
| SRQ | 22 | 2021 Q1 | -0.077 | 0.5 | -7.436 | -0.099 | -9.384 |
| COS | 13 | 2021 Q1 | -0.097 | 0.769 | -9.226 | -0.095 | -9.065 |
| LGB | 12 | 2016 Q2 | 0.024 | 0.667 | 2.378 | 0.05 | 5.073 |
| SBA | 11 | 2021 Q2 | 0.055 | 0.636 | 5.694 | 0.052 | 5.336 |
| ITO | 10 | 2020 Q1 | -0.001 | 0.7 | -0.099 | -0.004 | -0.347 |
| MTJ | 5 | 2021 Q1 | -0.163 | 0.8 | -15.064 | -0.142 | -13.273 |
| BLI | 5 | 2021 Q4 | -0.075 | 0.4 | -7.227 | -0.097 | -9.261 |

## The largest Southwest-threatened routes (from results/threatened_routes.csv)

The full list, for all three entrants, is in the CSV. Fares are geometric means over the windows.

| Route | Largest incumbent | Miles | Passengers a quarter before (est.) | Fare before ($) | Fare during threat ($) | Change, net of controls | Threat began | Southwest competing from |
|---|---|---|---|---|---|---|---|---|
| LGA-ORD | American | 733 | 546160 | 218 | 198 | 0.0794 | 2021 Q1 |  |
| LAX-ORD | American | 1744 | 417220 | 252 | 196 | -0.0776 | 2021 Q1 |  |
| BOS-ORD | American | 867 | 308848 | 203 | 179 | 0.0463 | 2021 Q1 |  |
| HNL-LAX | Hawaiian | 2556 | 276148 | 399 | 361 | -0.0464 | 2019 Q1 | 2021 Q2 |
| ORD-SFO | United | 1846 | 273990 | 353 | 279 | -0.0606 | 2021 Q1 |  |
| MCO-ORD | United | 1005 | 253525 | 190 | 124 | -0.1955 | 2021 Q1 | 2021 Q2 |
| LAS-ORD | United | 1514 | 247008 | 210 | 129 | -0.2562 | 2021 Q1 | 2021 Q2 |
| ATL-ORD | Delta | 606 | 236792 | 202 | 144 | -0.162 | 2021 Q1 |  |
| EWR-ORD | United | 719 | 219432 | 292 | 210 | -0.1523 | 2021 Q1 |  |
| ORD-SEA | Alaska | 1721 | 191468 | 248 | 197 | -0.055 | 2021 Q1 |  |
| MSP-ORD | Delta | 334 | 191252 | 194 | 151 | -0.0734 | 2021 Q1 |  |
| MIA-ORD | American | 1197 | 180235 | 239 | 153 | -0.2657 | 2021 Q1 |  |
| DCA-ORD | American | 612 | 173120 | 299 | 196 | -0.2478 | 2021 Q1 |  |
| IAH-LAX | United | 1379 | 171090 | 200 | 184 | 0.0005 | 2021 Q2 |  |
| ORD-PHL | American | 678 | 169372 | 294 | 202 | -0.1987 | 2021 Q1 |  |

## Sample groups (results/sample_groups.csv)

| Entrant | Route group | Routes |
|---|---|---|
| Southwest | control | 3249 |
| Southwest | served or threatened in 2014 | 2626 |
| Southwest | threatened | 706 |
| Southwest | entered at once | 349 |
| Southwest | threat in 2020 Q2-Q4 | 129 |
| Spirit | control | 5811 |
| Spirit | threatened | 1188 |
| Spirit | served or threatened in 2014 | 347 |
| Spirit | entered at once | 165 |
| Spirit | threat in 2020 Q2-Q4 | 38 |
| Frontier | control | 2931 |
| Frontier | threatened | 2772 |
| Frontier | served or threatened in 2014 | 1609 |
| Frontier | entered at once | 134 |
| Frontier | threat after 2023 | 103 |
| Frontier | entered without threat | 1 |

## The paper's Section 2 example, recomputed (results/paper_example.csv)

R is the incumbent's gain from deterring entry (monopoly minus Cournot profit). Every value matches the payoff list
on p. 447 of the paper and the thresholds on pp. 447–449. The least separating output is my addition.

| Quantity | Value |
|---|---|
| R: incumbent low, entrant low | 10.3125 |
| entrant profit less K: incumbent low, entrant low | -0.75 |
| R: incumbent low, entrant high | 9.1181 |
| entrant profit less K: incumbent low, entrant high | -2.3056 |
| R: incumbent high, entrant low | 9.75 |
| entrant profit less K: incumbent high, entrant low | 2.0 |
| R: incumbent high, entrant high | 8.8889 |
| entrant profit less K: incumbent high, entrant high | 0.1111 |
| monopoly output, low-cost incumbent | 4.75 |
| monopoly price, low-cost incumbent | 5.25 |
| monopoly profit, low-cost incumbent | 22.5625 |
| monopoly output, high-cost incumbent | 4.0 |
| monopoly price, high-cost incumbent | 6.0 |
| monopoly profit, high-cost incumbent | 16.0 |
| least separating output | 7.1225 |
| separating output in the paper | 7.2 |
| price at the separating output | 2.8 |
| markdown below the low-cost monopoly price | 0.4667 |
| low-cost payoff at 7.2 if every entrant stays out (p = 0) | 26.8725 |
| high-cost payoff from copying 7.2 (p = 0) | 15.51 |
| pooling: low-cost entrant comes in when q exceeds | 0.2727 |
| pooling: high-cost entrant comes in when q exceeds | 0.954 |

## Figures

- `results/southwest_threat_split.png`: Southwest event study, routes later entered against routes never entered,
  with 95% intervals.
- `results/threat_by_entrant.png`: event-study paths for Southwest, Spirit and Frontier.
