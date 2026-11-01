"""Draw the two event-study charts in results/ from results/event_study.csv (written by src/limit_pricing.py).

Usage (from the repository root):
    python src/figures.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
KMIN, KMAX = -8, 12    # event-time window in quarters, end points binned (as in src/limit_pricing.py)


def finish(ax, fig, path, title, xlabel):
    ax.axhline(0, color="#888", lw=0.8)
    ax.axvline(-0.5, color="#888", lw=0.8, ls="--")
    ticks = list(range(KMIN, KMAX + 1, 2))
    ax.set_xticks(ticks, [f"≤{t}" if t == KMIN else f"≥{t}" if t == KMAX else str(t) for t in ticks])
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Incumbents' fare vs. the quarter before (%)")
    ax.set_title(title, fontsize=11, loc="left")
    ax.legend(frameon=False, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_split(es, path):
    s = es[(es.entrant == "Southwest") & (es.outcome == "ln_fare") & es.group.isin(["entered", "never"])]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    styles = {"never": ("#1f5f8b", "Southwest never came"), "entered": ("#c8553d", "Southwest came later")}
    for grp, (col, lab) in styles.items():
        x = s[s.group == grp]
        off = -0.12 if grp == "never" else 0.12
        pct = 100 * (np.exp(x.coef) - 1)
        lo, hi = 100 * (np.exp(x.coef - 1.96 * x.se) - 1), 100 * (np.exp(x.coef + 1.96 * x.se) - 1)
        ax.errorbar(x.k + off, pct, yerr=[pct - lo, hi - pct], fmt="o-", color=col, ms=3.5, lw=1.4,
                    elinewidth=0.8, capsize=0, label=lab)
    finish(ax, fig, path, "Incumbent fares after Southwest lands at both ends of a route",
           "Quarters since Southwest began serving both airports")


def plot_entrants(es, path):
    s = es[(es.outcome == "ln_fare") & (es.group == "all threatened")]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    cols = {"Southwest": "#1f5f8b", "Spirit": "#d4a017", "Frontier": "#3c8d5a"}
    for i, (name, col) in enumerate(cols.items()):
        x = s[s.entrant == name]
        ax.plot(x.k + (i - 1) * 0.1, 100 * (np.exp(x.coef) - 1), "o-", color=col, ms=3.5, lw=1.4, label=name)
    finish(ax, fig, path, "Incumbent fares after a low-fare airline lands at both ends of a route",
           "Quarters since the airline began serving both airports")


def main():
    es = pd.read_csv(RES / "event_study.csv")
    print(f"loaded {len(es):,} event-study coefficients from results/event_study.csv")
    plot_split(es, RES / "southwest_threat_split.png")
    plot_entrants(es, RES / "threat_by_entrant.png")
    print("wrote results/southwest_threat_split.png, results/threat_by_entrant.png")


if __name__ == "__main__":
    main()
