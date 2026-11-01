# Methods review: Milgrom and Roberts (1982)

- **Paper:** Paul Milgrom and John Roberts, "Limit Pricing and Entry under Incomplete Information: An Equilibrium
  Analysis," *Econometrica* 50(2), March 1982, pp. 443–459. Manuscript received March 1980, revised December 1980.
- **Statistical focus:** the two-type numerical example of Section 2 (the separating equilibrium in which the
  low-cost incumbent produces 7.2 rather than its monopoly output of 4.75, the pooling equilibrium at 4.75, and the
  resulting entry probabilities q and 1 − p), and the general claim of Section 3 that a rational entrant's
  expectations cannot be biased on average by the incumbent's pre-entry action.
- **Review standard:** internal consistency of the formal results, explicitness of assumptions, and the testability
  of the predictions.
- **What was read:** the full published article (a scan of the *Econometrica* pages, retrieved from the working
  paper archive at dklevine.com), including footnotes and the reference list. Biographical context came from
  Milgrom's autobiography on NobelPrize.org and Roberts's faculty page at Stanford. No other secondary account was
  used for the content of the paper.

## Methods summary

### Research design

A game-theoretic model of entry with two-sided private information about unit costs, solved for Nash equilibria
(in the Harsanyi formulation), with explicit examples. Section 2 works a linear-demand, constant-cost model with
two-point and then continuous cost distributions. Section 3 sketches a general two-period model and states a
property of all its equilibria. There is no empirical component.

### Sampling strategy

Does not apply. The paper uses no data.

### Sample size

Does not apply.

### Inclusion and exclusion criteria

Does not apply as a data rule. The analogous choices are modeling restrictions. The incumbent's post-entry profit
is normalized to zero, post-entry competition is complete-information Cournot, the model has two periods, the
entrant observes the incumbent's output exactly in Section 2, and costs are independently distributed.

### Independent and dependent variables

In the theory, the primitives are the incumbent's cost $`c_1`$, the entrant's cost $`c_2`$, demand parameters
$`a, b`$, entry cost $`K`$, discount factors and the cost distributions. The endogenous outcomes are the incumbent's
pre-entry output (equivalently price) and the entry decision. The comparison of interest is the equilibrium entry
probability against the full-information benchmark.

### Statistical methods

None in the econometric sense. The "statistics" are closed-form payoffs, equilibrium strategies and threshold
probabilities, verified by direct substitution, plus a differential equation characterizing separating equilibria
with a continuum of types and a sufficient condition for pseudo-concavity.

### Reported effect sizes

The effect sizes are the example's equilibrium quantities. The low-cost incumbent's separating output of 7.2
against a monopoly output of 4.75 implies a price of 2.80 against 5.25, a markdown of 47%. Entry probability is q in
any separating equilibrium and 1 − p in the pooling equilibrium shown.

### Confidence intervals

Does not apply. Results are exact under the stated assumptions.

### p-values, if applicable

Does not apply.

### Missing data treatment

Does not apply.

### Stated limitations

The authors state that the example has special features (linear demand and cost, full-information Cournot after
entry) that they argue do not drive the results. They acknowledge a continuum of separating and pooling equilibria,
discuss narrowing it by sequential-equilibrium and Pareto-efficiency arguments, note that their equilibria already
satisfy the sequential condition so multiplicity remains, call Section 3 an "admittedly incomplete analysis," and
name multi-period models with predation and reputation as the needed extension.

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| R(low incumbent, low entrant) | 10.31, profit units | p. 447, payoff list | Low-cost incumbent's gain from deterring a low-cost entrant | Any magnitude in a real market |
| R(low incumbent, high entrant) | 9.12 (printed value partly illegible in the scan; recomputed) | p. 447 | Same, high-cost entrant | |
| R(high incumbent, low entrant) | 9.75 | p. 447 | High-cost incumbent's gain from deterring a low-cost entrant | |
| R(high incumbent, high entrant) | 8.89 | p. 447 | Same, high-cost entrant | |
| Entrant's net entry profit, four cases | −0.75, −2.31, 2.00, 0.11 | p. 447 | Profit after entry cost K = 7 against a low or high-cost incumbent | That entry decisions in practice hinge on cost alone |
| Monopoly output and profit | 4.75 and 22.56 (low cost); 4.00 and 16.00 (high cost) | p. 447 | Short-run optimum for each type | |
| Pooling entry thresholds on q | 0.273 and 0.954 | p. 447 | Prior probability of a high-cost incumbent above which each entrant type enters when the price is uninformative | |
| Separating output, low-cost type | 7.2 | p. 448 | Output that deters entry and that the high-cost type will not copy | That 7.2 is the unique or most plausible separating output (any output above about 7.12 works) |
| High-cost payoff from copying 7.2 | 15.51 − 0.86p, against 16 from its monopoly output | p. 448 | No-mimic condition | |
| Low-cost payoff at 7.2 | 26.87 − 1.19p, against 22.56 | p. 448 | Low type prefers to separate | |
| Pooling output | 4.75 for both types | p. 449 | Equilibrium with uninformative price | That pooling is more or less likely than separating |
| Pooling existence condition | p > 0.063, from 15.44 + 8.89p > 16 | p. 449 | Range in which the high-cost type does not deviate | |
| Entry probability | q (separating), 1 − p (pooling) | pp. 448–449 | Equilibrium entry relative to full information | The direction of any difference in a given market |
| Sufficient condition, continuum example | a < 48bK/13 | p. 453 | Guarantees the first-order solution is an equilibrium | Necessity |
| Unbiased expectations | Expected profit estimate with signal equals estimate without | p. 457, expression (3) | Entrant cannot be fooled on average | That entry is unchanged in any particular market |

## Interpretation notes

- The paper's central claim is a possibility result. Limit pricing can arise in equilibrium, and entry can be
  higher, equal or lower than with full information. It does not say which happens.
- The sharpest testable implication comes from the separating equilibrium. The incumbent types that face entry are
  the ones that did not distort their price, so pre-entry price cuts should be concentrated where entry does not
  follow. Pooling predicts the same cut whether or not entry follows.
- All payoffs, thresholds and strategies in the example are internally consistent. Recomputing them from the
  paper's own formulas (`src/paper_example.py`) gives values that agree with every legible printed value to the
  reported precision. This is arithmetic on the paper's stated formulas, not an independent replication of its
  analysis.
- The choice of 7.2 in the example is one point in a continuum; the least output satisfying the no-mimic condition
  for all p is about 7.12. The paper says this explicitly (the continuum is parameterized by the critical output).
- The policy conclusion, that limit pricing should not be discouraged, is conditional on pre-entry prices not
  affecting post-entry demand and on the two-period structure, as the authors state.
- How the modern rerun relates. The repository tests the separating signature on US airline routes, 2014 to 2024,
  with Southwest's arrival at both endpoints as the threat. That is a test of the theory's predictions on new data,
  not a reproduction of anything in the paper, which reports no data.

## Unanswered questions

- Which equilibrium should be expected in practice. The paper offers Pareto-efficiency and boundary-condition
  arguments but no criterion that would select between separating and pooling.
- How the results change when the entrant observes price with noise. Section 3 argues exact inference becomes
  unlikely, but the size of the resulting entry effect is not worked out.
- How limit pricing interacts with repeated play and reputation, which the authors leave to later work.
- Whether incumbents' private information is mainly about cost, as modeled, or about demand, which would change
  what a low price signals.

## Items requiring expert verification

- The value of R(low incumbent, high entrant) is not legible in the scanned payoff list. The recomputed 9.12 is
  consistent with the printed payoff 26.87 − 1.19p, but a clean copy of p. 447 should be checked.
- The comparative statics for the continuum example (pp. 453–454) were read but not re-derived here.
- The claim that every perfect equilibrium is sequential is attributed by the paper to Kreps and Wilson; this review
  did not check that source.
- No published correction or comment on this paper was located in the sources read. That is a limit of the search,
  not evidence that none exists.
