"""Recompute the two-type example in Section 2 of Milgrom and Roberts (1982) from its own formulas.

Inverse demand P = a - bQ with a = 10, b = 1; entry cost K = 7; no discounting. The incumbent's unit
cost is 0.5 (low) or 2.0 (high); the entrant's is 1.5 (low) or 2.0 (high). After entry the two firms
learn each other's costs and play Cournot. The script reproduces the payoff table on p. 447, the
separating equilibrium (low-cost incumbent produces 7.2 rather than its monopoly 4.75) and the
pooling thresholds q = 0.273 and 0.954, and adds the smallest output that still separates.

Usage (from the repository root):
    python src/paper_example.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
A, B, K = 10.0, 1.0, 7.0          # demand intercept, slope and entry cost (paper, p. 447)
C1_LO, C1_HI = 0.5, 2.0           # incumbent's two possible unit costs
C2_LO, C2_HI = 1.5, 2.0           # entrant's two possible unit costs
Q_SEP = 7.2                       # separating output the paper uses for the low-cost incumbent


def monopoly_profit(c):
    return (A - c) ** 2 / (4 * B)


def cournot_profit(c_own, c_other):
    return (A - 2 * c_own + c_other) ** 2 / (9 * B)


def reward(c1, c2):
    """Incumbent's gain from keeping the entrant out: monopoly minus Cournot profit."""
    return monopoly_profit(c1) - cournot_profit(c1, c2)


def main():
    rows = []
    for c1, n1 in ((C1_LO, "low"), (C1_HI, "high")):
        for c2, n2 in ((C2_LO, "low"), (C2_HI, "high")):
            rows.append((f"R: incumbent {n1}, entrant {n2}", reward(c1, c2)))
            rows.append((f"entrant profit less K: incumbent {n1}, entrant {n2}", cournot_profit(c2, c1) - K))
    for c1, n1 in ((C1_LO, "low"), (C1_HI, "high")):
        m = (A - c1) / (2 * B)
        rows += [(f"monopoly output, {n1}-cost incumbent", m), (f"monopoly price, {n1}-cost incumbent", A - B * m),
                 (f"monopoly profit, {n1}-cost incumbent", monopoly_profit(c1))]

    # the high-cost incumbent will not copy output Q if (A - BQ - c) Q + R(c, c2 low) <= its monopoly profit;
    # the larger root of that quadratic is the least output that still tells the two types apart
    r_hi = reward(C1_HI, C2_LO)
    q_min = ((A - C1_HI) + np.sqrt((A - C1_HI) ** 2 - 4 * B * (monopoly_profit(C1_HI) - r_hi))) / (2 * B)
    low_payoff = (A - B * Q_SEP - C1_LO) * Q_SEP + reward(C1_LO, C2_LO)
    mimic_payoff = (A - B * Q_SEP - C1_HI) * Q_SEP + reward(C1_HI, C2_LO)
    rows += [("least separating output", q_min), ("separating output in the paper", Q_SEP),
             ("price at the separating output", A - B * Q_SEP),
             ("markdown below the low-cost monopoly price", 1 - (A - B * Q_SEP) / (A - B * (A - C1_LO) / (2 * B))),
             ("low-cost payoff at 7.2 if every entrant stays out (p = 0)", low_payoff),
             ("high-cost payoff from copying 7.2 (p = 0)", mimic_payoff)]

    # pooling: the entrant sees nothing and enters if q * profit(high inc.) + (1 - q) * profit(low inc.) >= 0
    for c2, n2 in ((C2_LO, "low"), (C2_HI, "high")):
        lo, hi = cournot_profit(c2, C1_LO) - K, cournot_profit(c2, C1_HI) - K
        rows.append((f"pooling: {n2}-cost entrant comes in when q exceeds", -lo / (hi - lo)))

    out = pd.DataFrame(rows, columns=["quantity", "value"])
    out["value"] = out.value.round(4)
    path = ROOT / "results" / "paper_example.csv"
    path.parent.mkdir(exist_ok=True)
    out.to_csv(path, index=False)
    print(out.to_string(index=False))
    print("wrote results/paper_example.csv")


if __name__ == "__main__":
    main()
