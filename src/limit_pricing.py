"""Milgrom and Roberts (1982) on airline routes, 2014-2024: do incumbents limit price, and does it work?

Reads the two quarterly tables written by src/build_panel.py (data/derived/) and the CPI from FRED
(data/raw/CPIAUCSL.csv). For one potential entrant at a time (Southwest for the main test; Spirit and
Frontier for the extension) it:

  1. finds the quarter in which the entrant first has regular service at both ends of a route it does
     not yet compete on (the "threat"), and the quarter, if any, in which it starts competing (5% of the
     route's tickets, nonstop or connecting, or nonstop service);
  2. estimates incumbents' fares and passengers around the threat, against routes the entrant never
     reached, with route-by-season and quarter fixed effects (an event study);
  3. splits the threatened routes by whether the entrant later came in. Milgrom and Roberts's separating
     equilibrium says the incumbent that ends up facing entry is the one that did not cut its price;
  4. asks whether a bigger fare cut in the first year of the threat made entry less likely.

Writes CSVs to results/; src/figures.py draws the two charts from results/event_study.csv. The paper's own
numerical example is in src/paper_example.py.

Usage (from the repository root):
    python src/limit_pricing.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DER = ROOT / "data" / "derived"
RES = ROOT / "results"

PRESENCE_MIN = 300     # sampled passengers an airline itself flies out of or into an airport in a quarter
                       # (about 3,000 real, a few daily flights) to count as regular service there
NS_MIN = 100           # sampled nonstop passengers on the route in a quarter (about 1,000 real) to count
                       # as flying it nonstop
ENTRY_SHARE = 0.05     # the entrant "competes" on a route once it sells 5% of the route's tickets (nonstop or
                       # connecting) or flies it nonstop; presence and entry must each hold two quarters running
MIN_MILES = 100        # shorter airport pairs are mostly ground-transport markets
MIN_INC_PAX = 100      # route needs at least this many sampled incumbent passengers per quarter on average
MIN_QUARTERS = 32      # ... and must appear in at least 32 of the 41 usable quarters
MIN_Q_INC_PAX = 20     # a route-quarter's incumbent fare is used only with at least 20 sampled tickets
PANDEMIC = [25, 26, 27]  # 2020 Q2-Q4 (quarter index from 2014 Q1 = 0), dropped: travel fell by 60-90%
LAST_ONSET = 39        # threats must start by 2023 Q4 so at least four later quarters are seen
SPLIT_ONSET = 31       # for the entered / never-entered split, threats must start by 2021 Q4 (12 quarters seen)
ENTRY_WINDOW = 12      # entry "within three years" of the threat, in quarters
KMIN, KMAX = -8, 12    # event-time window in quarters, end points binned
ENTRANTS = {"WN": "Southwest", "NK": "Spirit", "F9": "Frontier"}
LOW_FARE = ["WN", "NK", "F9", "G4", "B6"]  # carriers dropped from the "network incumbents" fare (robustness)
NAMES = {"AA": "American", "DL": "Delta", "UA": "United", "AS": "Alaska", "B6": "JetBlue", "WN": "Southwest",
         "NK": "Spirit", "F9": "Frontier", "G4": "Allegiant", "HA": "Hawaiian", "SY": "Sun Country",
         "US": "US Airways", "VX": "Virgin America", "MX": "Breeze"}

def qlabel(t):
    return f"{2014 + t // 4} Q{t % 4 + 1}"

def load():
    r = pd.concat([pd.read_csv(f, keep_default_na=False, na_values=[""])
                   for f in sorted(DER.glob("route_quarter_*.csv.gz"))], ignore_index=True)
    a = pd.read_csv(DER / "airport_quarter.csv.gz", keep_default_na=False, na_values=[""])
    for d in (r, a):
        d["t"] = (d.year - 2014) * 4 + d.quarter - 1
    cpi = pd.read_csv(ROOT / "data" / "raw" / "CPIAUCSL.csv", parse_dates=["observation_date"])
    cpi["t"] = (cpi.observation_date.dt.year - 2014) * 4 + (cpi.observation_date.dt.month - 1) // 3
    cpi = cpi.groupby("t").CPIAUCSL.mean()
    base = cpi.loc[40:43].mean()  # 2024 dollars
    r["deflator"] = r.t.map(base / cpi)
    print(f"loaded {len(r):,} route-quarters ({r[['a', 'b']].drop_duplicates().shape[0]:,} airport pairs) and "
          f"{len(a):,} airport-airline-quarters, {qlabel(r.t.min())} to {qlabel(r.t.max())}")
    return r, a

def first_run(flags):
    """First quarter index at which a boolean series (indexed by quarter) is true twice running."""
    f = flags.reindex(range(44), fill_value=False).to_numpy()
    hits = np.where(f[:-1] & f[1:])[0]
    return int(hits[0]) if len(hits) else np.inf

def classify(r, a, carrier):
    """One row per airport pair with the threat quarter, the entry quarter and the sample group."""
    pres = a[(a.carrier == carrier) & (a.pax >= PRESENCE_MIN)]
    est = pres.groupby("airport").t.apply(lambda s: first_run(pd.Series(True, index=s.values)))
    comp = r[(r[f"ns_{carrier}"] >= NS_MIN) | (r[f"pax_{carrier}"] >= ENTRY_SHARE * r.pax)]
    entry = comp.groupby(["a", "b"]).t.apply(lambda s: first_run(pd.Series(True, index=s.values)))
    fly = r[r[f"ns_{carrier}"] >= NS_MIN]
    nonstop = fly.groupby(["a", "b"]).t.apply(lambda s: first_run(pd.Series(True, index=s.values)))
    fly_2014 = set(map(tuple, comp[comp.t < 4][["a", "b"]].to_numpy()))

    r = r.copy()
    r["inc_pax"] = r.pax - r[f"pax_{carrier}"]
    r = r[(r.inc_pax > 0) & ~r.t.isin(PANDEMIC)]
    g = r.groupby(["a", "b"]).agg(miles=("miles", "median"), n_q=("t", "nunique"), inc_pax=("inc_pax", "mean"))
    g = g.reset_index()
    g["est_a"] = g.a.map(est).fillna(np.inf)
    g["est_b"] = g.b.map(est).fillna(np.inf)
    g["onset"] = g[["est_a", "est_b"]].max(axis=1)
    g["trigger"] = np.where(g.est_a >= g.est_b, g.a, g.b)
    g["entry"] = [entry.get((x, y), np.inf) for x, y in zip(g.a, g.b)]
    g["nonstop"] = [nonstop.get((x, y), np.inf) for x, y in zip(g.a, g.b)]
    g["flew_2014"] = [(x, y) in fly_2014 for x, y in zip(g.a, g.b)]

    n0 = len(g)
    keep = (g.miles >= MIN_MILES) & (g.n_q >= MIN_QUARTERS) & (g.inc_pax >= MIN_INC_PAX)
    print(f"  {ENTRANTS[carrier]}: {n0:,} airport pairs; kept {keep.sum():,} with >= {MIN_MILES} miles, "
          f">= {MIN_QUARTERS} usable quarters and >= {MIN_INC_PAX} incumbent passengers a quarter")
    g = g[keep].copy()
    grp = pd.Series("other", index=g.index)
    grp[g.flew_2014 | (g.onset < 4)] = "served or threatened in 2014"
    ctrl = np.isinf(g.onset) & np.isinf(g.entry)
    grp[ctrl] = "control"
    late = (g.onset >= 4) & np.isfinite(g.onset) & ~g.flew_2014
    grp[late & (g.entry <= g.onset)] = "entered at once"
    grp[late & (g.onset > LAST_ONSET)] = "threat after 2023"
    grp[late & g.onset.isin(PANDEMIC)] = "threat in 2020 Q2-Q4"
    thr = late & (g.entry > g.onset) & (g.onset <= LAST_ONSET) & ~g.onset.isin(PANDEMIC)
    grp[thr] = "threatened"
    grp[np.isinf(g.onset) & np.isfinite(g.entry) & ~g.flew_2014] = "entered without threat"
    g["group"] = grp
    print("  " + "; ".join(f"{k} {v:,}" for k, v in g.group.value_counts().items()))
    return g

def two_way_demean(df, cols, g1, g2, iters=200, tol=1e-10):
    """Sweep out two sets of fixed effects by alternating projections."""
    x = df[cols].to_numpy(dtype=float).copy()
    k1, k2 = pd.factorize(df[g1])[0], pd.factorize(df[g2])[0]
    n1, n2 = np.bincount(k1), np.bincount(k2)
    for _ in range(iters):
        old = x.copy()
        for k, n in ((k1, n1), (k2, n2)):
            sums = np.zeros((n.size, x.shape[1]))
            np.add.at(sums, k, x)
            x -= (sums / n[:, None])[k]
        if np.abs(x - old).max() < tol:
            break
    return pd.DataFrame(x, columns=cols, index=df.index)

def lincom(fit, names, weights=None):
    w = np.ones(len(names)) / len(names) if weights is None else np.asarray(weights)
    b = fit.params[names].to_numpy() @ w
    v = w @ fit.cov_params().loc[names, names].to_numpy() @ w
    return b, np.sqrt(v)

def panel(r, g, carrier):
    keep = g[g.group.isin(["threatened", "control"])][["a", "b", "onset", "entry", "nonstop", "group", "trigger"]]
    d = r.merge(keep, on=["a", "b"])
    d = d[~d.t.isin(PANDEMIC)].copy()
    d["inc_pax"] = d.pax - d[f"pax_{carrier}"]
    d["inc_rev"] = d.rev - d[f"rev_{carrier}"]
    n0 = len(d)
    d = d[d.inc_pax >= MIN_Q_INC_PAX]
    d["ln_fare"] = np.log(d.inc_rev / d.inc_pax * d.deflator)
    d["ln_pax"] = np.log(d.inc_pax)
    # network incumbents only: drop every low-fare airline, so a rival low-fare entrant cannot move the mix
    net_pax = d.pax - sum(d[f"pax_{c}"] for c in LOW_FARE)
    net_rev = d.rev - sum(d[f"rev_{c}"] for c in LOW_FARE)
    ok = (net_pax >= MIN_Q_INC_PAX) & (net_rev > 0)
    d["ln_fare_net"] = np.log((net_rev / net_pax * d.deflator).where(ok))
    d["route"] = d.a + "-" + d.b
    d["route_season"] = d.route + "_" + d.quarter.astype(str)
    print(f"  panel: {n0:,} route-quarters; kept {len(d):,} with >= {MIN_Q_INC_PAX} sampled incumbent tickets")
    return d

def event_study(d, outcome, split=None, cluster="route"):
    """ln outcome on threat event-time dummies (k = -1 omitted), post-entry dummies, FE; clustered SE."""
    d = d.copy()
    thr = d.group == "threatened"
    k = (d.t - d.onset).clip(KMIN, KMAX)
    cols = []
    groups = [("", thr)] if split is None else [(f"{s}_", thr & split.eq(s)) for s in split[thr].unique()]
    for tag, mask in groups:
        for kk in range(KMIN, KMAX + 1):
            if kk == -1:
                continue
            c = f"{tag}k{kk}"
            d[c] = ((k == kk) & mask).astype(float)
            cols.append(c)
    since = d.t - d.entry
    for lo, hi, c in ((0, 3, "in0_3"), (4, 7, "in4_7"), (8, 99, "in8p")):
        d[c] = (thr & (since >= lo) & (since <= hi)).astype(float)
        cols.append(c)
    dm = two_way_demean(d, [outcome] + cols, "route_season", "t")
    use = [c for c in cols if dm[c].abs().sum() > 0]
    fit = sm.OLS(dm[outcome], dm[use]).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d[cluster])[0]})
    return fit

def summarize_es(fit, tag=""):
    yr1 = [f"{tag}k{k}" for k in range(0, 4)]
    pre = [f"{tag}k{k}" for k in (-4, -3, -2)]
    b1, s1 = lincom(fit, yr1)
    b0, s0 = lincom(fit, pre)
    return b1, s1, b0, s0

def route_cuts(d, carrier):
    """Route-level fare change in the first year of the threat, net of the control-route path."""
    ctrl = d[d.group == "control"].copy()
    ctrl["dev"] = ctrl.ln_fare - ctrl.groupby("route_season").ln_fare.transform("mean")
    phi = ctrl.groupby("t").dev.mean()
    th = d[d.group == "threatened"].copy()
    th["adj"] = th.ln_fare - th.t.map(phi)
    ctrl["dev_net"] = ctrl.ln_fare_net - ctrl.groupby("route_season").ln_fare_net.transform("mean")
    th["adj_net"] = th.ln_fare_net - th.t.map(ctrl.groupby("t").dev_net.mean())
    th["padj"] = th.ln_pax - th.t.map(ctrl.assign(pd_=ctrl.ln_pax - ctrl.groupby("route_season").ln_pax
                                                   .transform("mean")).groupby("t").pd_.mean())
    rows = []
    for route, s in th.groupby("route"):
        T, E = s.onset.iloc[0], s.entry.iloc[0]
        s = s.sort_values("t")
        pre = s[s.t < T].tail(4)
        post = s[(s.t >= T) & (s.t < E)].head(4)
        post = post[post.t <= T + 3 + 3 * (T == 24)]  # a 2020 Q1 threat skips the dropped quarters
        if len(pre) < 4 or len(post) < 1:
            continue
        raw = post.ln_fare.mean() - pre.ln_fare.mean()
        rows.append(dict(route=route, a=s.a.iloc[0], b=s.b.iloc[0], onset=T, entry=E, trigger=s.trigger.iloc[0],
                         raw_change=raw, control_change=raw - (post.adj.mean() - pre.adj.mean()),
                         cut=post.adj.mean() - pre.adj.mean(), pax_change=post.padj.mean() - pre.padj.mean(),
                         pre_fare=np.exp(pre.ln_fare.mean()), post_fare=np.exp(post.ln_fare.mean()),
                         pre_pax=pre.inc_pax.mean() * 10, miles=s.miles.median(), n_post=len(post),
                         net_pre_fare=np.exp(pre.ln_fare_net.mean()), net_post_fare=np.exp(post.ln_fare_net.mean()),
                         cut_net=post.adj_net.mean() - pre.adj_net.mean()))
    return pd.DataFrame(rows)

def entry_regression(c, carrier, a):
    """Linear probability of entry within ENTRY_WINDOW quarters on the first-year fare cut."""
    c = c[c.onset <= SPLIT_ONSET].copy()
    c["entered"] = (c.entry - c.onset <= ENTRY_WINDOW).astype(float)
    trig = a[a.carrier == carrier].set_index(["airport", "t"]).pax
    c["ln_trigger_pax"] = np.log([trig.get((x, int(t)), PRESENCE_MIN) for x, t in zip(c.trigger, c.onset)])
    c["ln_miles"], c["ln_pre_pax"], c["ln_pre_fare"] = np.log(c.miles), np.log(c.pre_pax), np.log(c.pre_fare)
    c["ln_post_fare"] = np.log(c.post_fare)
    base = ["ln_miles", "ln_pre_pax", "ln_trigger_pax"]
    late = c[c.entry > c.onset + 3].copy()
    late["entered"] = ((late.entry - late.onset >= 4) & (late.entry - late.onset <= ENTRY_WINDOW + 3)).astype(float)
    out = []
    for name, data, cols, key in (("cut only", c, ["cut"], "cut"),
                                  ("cut with route controls", c, ["cut"] + base, "cut"),
                                  ("cut, also holding the pre-threat fare", c, ["cut", "ln_pre_fare"] + base, "cut"),
                                  ("cut, routes not entered in year 1", late, ["cut"] + base, "cut"),
                                  ("cut only, threats starting 2015-2019", c[c.onset <= 23], ["cut"], "cut"),
                                  ("fare level during threat", c, ["ln_post_fare"] + base, "ln_post_fare")):
        yrs = pd.get_dummies((data.onset // 4 + 2014).astype(int), prefix="y", drop_first=True, dtype=float)
        X = sm.add_constant(pd.concat([data[cols], yrs], axis=1))
        fit = sm.OLS(data.entered, X).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(data.trigger)[0]})
        out.append(dict(entrant=ENTRANTS[carrier], spec=name, regressor=key, coef=fit.params[key],
                        se=fit.bse[key], p=fit.pvalues[key], n_routes=int(fit.nobs),
                        n_clusters=data.trigger.nunique(), entry_rate=data.entered.mean()))
    q = pd.qcut(c.cut, 4, labels=["largest cuts", "second", "third", "smallest cuts or rises"])
    tab = c.groupby(q, observed=True).agg(routes=("cut", "size"), mean_cut=("cut", "mean"),
                                          entry_rate=("entered", "mean")).reset_index()
    tab.insert(0, "entrant", ENTRANTS[carrier])
    tab["mean_cut_pct"] = 100 * (np.exp(tab.mean_cut) - 1)
    return pd.DataFrame(out), tab, c

def leading_incumbent(r, c, carrier):
    """Largest non-entrant ticketing airline on each route over the four quarters before the threat."""
    lead = {}
    for row in c.itertuples():
        s = r[(r.a == row.a) & (r.b == row.b) & (r.t < row.onset) & (r.t >= row.onset - 4)]
        tot = {}
        for k in (1, 2, 3):
            for code, p in zip(s[f"c{k}"], s[f"pax{k}"]):
                if isinstance(code, str) and code != carrier:
                    tot[code] = tot.get(code, 0) + p
        lead[row.route] = max(tot, key=tot.get) if tot else ""
    return c.route.map(lead)

def coef_rows(fit, carrier, outcome, group, tag=""):
    return [dict(entrant=ENTRANTS[carrier], outcome=outcome, group=group, k=kk,
                 coef=0.0 if kk == -1 else fit.params.get(f"{tag}k{kk}", np.nan),
                 se=0.0 if kk == -1 else fit.bse.get(f"{tag}k{kk}", np.nan)) for kk in range(KMIN, KMAX + 1)]

def run(r, a, carrier):
    print(f"\n=== potential entrant: {ENTRANTS[carrier]} ===")
    g = classify(r, a, carrier)
    d = panel(r, g, carrier)
    n_thr, n_ctl = d[d.group == "threatened"].route.nunique(), d[d.group == "control"].route.nunique()
    out = {"entrant": ENTRANTS[carrier], "threatened_routes": n_thr, "control_routes": n_ctl,
           "route_quarters": len(d)}
    es_rows = []
    for outcome in ("ln_fare", "ln_pax"):
        fit = event_study(d, outcome)
        b1, s1, b0, s0 = summarize_es(fit)
        out[f"{outcome}_year1"], out[f"{outcome}_year1_se"] = b1, s1
        out[f"{outcome}_pre"], out[f"{outcome}_pre_se"] = b0, s0
        e1, es1 = lincom(fit, ["in0_3"])
        out[f"{outcome}_entry0_3"], out[f"{outcome}_entry0_3_se"] = e1, es1
        es_rows += coef_rows(fit, carrier, outcome, "all threatened")
        out["n_obs"] = int(fit.nobs)

    ts = g[(g.group == "threatened") & (g.onset <= SPLIT_ONSET)]
    out["split_routes"] = len(ts)
    out["entry_rate_3y"] = (ts.entry - ts.onset <= ENTRY_WINDOW).mean()
    out["nonstop_rate_3y"] = (ts.nonstop - ts.onset <= ENTRY_WINDOW).mean()
    out["entered_ever"] = np.isfinite(ts.entry).mean()
    out["median_quarters_to_entry"] = (ts.entry - ts.onset)[np.isfinite(ts.entry)].median()

    # separating-equilibrium signature: entered vs never entered, threats starting by 2021 Q4
    ds = d[(d.group == "control") | (d.onset <= SPLIT_ONSET)].copy()
    split = pd.Series(np.where(np.isfinite(ds.entry), "entered", "never"), index=ds.index)
    fit = event_study(ds, "ln_fare", split)
    for tag in ("entered", "never"):
        b1, s1, b0, s0 = summarize_es(fit, f"{tag}_")
        out[f"fare_year1_{tag}"], out[f"fare_year1_{tag}_se"] = b1, s1
        out[f"fare_pre_{tag}"], out[f"fare_pre_{tag}_se"] = b0, s0
        out[f"routes_{tag}"] = ds[(ds.group == "threatened") & split.eq(tag)].route.nunique()
        es_rows += coef_rows(fit, carrier, "ln_fare", tag, f"{tag}_")
    names = [f"entered_k{k}" for k in range(4)] + [f"never_k{k}" for k in range(4)]
    diff, dse = lincom(fit, names, [0.25] * 4 + [-0.25] * 4)
    out["fare_year1_diff"], out["fare_year1_diff_se"] = diff, dse
    pre19 = ds[(ds.group == "control") | (ds.onset <= 23)]
    fit = event_study(pre19, "ln_fare", split[pre19.index])
    for tag in ("entered", "never"):
        b1, s1, _, _ = summarize_es(fit, f"{tag}_")
        out[f"fare_year1_{tag}_2015_19"], out[f"fare_year1_{tag}_2015_19_se"] = b1, s1
        out[f"routes_{tag}_2015_19"] = pre19[(pre19.group == "threatened") & split[pre19.index].eq(tag)].route.nunique()

    rob, ctl = [], d.group == "control"
    for label, sub, cl, y in (("all threats, SE by route", d, "route", "ln_fare"),
                              ("all threats, SE by newly served airport", d, "trigger", "ln_fare"),
                              ("threats starting 2015-2019 only", d[ctl | (d.onset <= 23)], "route", "ln_fare"),
                              ("threats starting 2021-2023 only", d[ctl | (d.onset >= 28)], "route", "ln_fare"),
                              ("network incumbents only (no low-fare airlines)", d[d.ln_fare_net.notna()], "route",
                               "ln_fare_net")):
        sub = sub.assign(trigger=sub.trigger.where(sub.group == "threatened", sub.route))
        f = event_study(sub, y, cluster=cl)
        b1, s1, b0, s0 = summarize_es(f)
        rob.append(dict(entrant=ENTRANTS[carrier], sample=label, fare_year1=b1, se=s1, pre=b0, pre_se=s0,
                        threatened_routes=sub[sub.group == "threatened"].route.nunique()))
    out["robust"] = rob
    cuts = route_cuts(d, carrier)
    reg, quart, cuts_split = entry_regression(cuts, carrier, a)
    cuts_split["lead"] = leading_incumbent(r, cuts_split, carrier)
    cuts_split["entrant"] = ENTRANTS[carrier]
    counts = g.group.value_counts().rename_axis("group").reset_index(name="routes")
    counts.insert(0, "entrant", ENTRANTS[carrier])
    return out, pd.DataFrame(es_rows), reg, quart, cuts_split, counts, g

def main():
    RES.mkdir(exist_ok=True)
    r, a = load()
    summ, ess, regs, quarts, cutl, cnts = [], [], [], [], [], []
    for carrier in ENTRANTS:
        out, es, reg, quart, cuts, counts, g = run(r, a, carrier)
        summ.append(out); ess.append(es); regs.append(reg); quarts.append(quart); cutl.append(cuts)
        cnts.append(counts)
        if carrier == "WN":
            imm = g[g.group == "entered at once"]
            print(f"  routes Southwest flew in the same quarter it reached both ends: {len(imm):,}")
    pd.DataFrame([x for o in summ for x in o.pop("robust")]).to_csv(RES / "robustness.csv", index=False)
    summary = pd.DataFrame(summ)
    for c in [c for c in summary.columns if c.startswith(("ln_fare", "ln_pax", "fare_")) and not c.endswith("_se")]:
        summary[c + "_pct"] = 100 * (np.exp(summary[c].astype(float)) - 1)  # log points to percent
        if c + "_se" in summary:
            b, se = summary[c].astype(float), summary[c + "_se"].astype(float)
            summary[c + "_ci_lo"], summary[c + "_ci_hi"] = b - 1.96 * se, b + 1.96 * se
            summary[c + "_p"] = 2 * stats.norm.sf(np.abs(b / se))
    summary.to_csv(RES / "threat_summary.csv", index=False)
    es = pd.concat(ess)
    es.to_csv(RES / "event_study.csv", index=False)
    pd.concat(regs).to_csv(RES / "entry_regression.csv", index=False)
    pd.concat(quarts).to_csv(RES / "entry_by_cut_quartile.csv", index=False)
    pd.concat(cnts).to_csv(RES / "sample_groups.csv", index=False)
    cuts = pd.concat(cutl)
    cuts["entered_within_3y"] = cuts.entered.astype(bool)
    cuts["onset_quarter"] = cuts.onset.astype(int).map(qlabel)
    cuts["entry_quarter"] = [qlabel(int(e)) if np.isfinite(e) else "" for e in cuts.entry]
    cuts["lead_name"] = cuts.lead.map(NAMES).fillna(cuts.lead)
    keep = ["entrant", "route", "lead", "lead_name", "miles", "pre_pax", "pre_fare", "post_fare", "raw_change",
            "control_change", "cut", "net_pre_fare", "net_post_fare", "cut_net", "pax_change", "onset_quarter",
            "entry_quarter", "entered_within_3y", "trigger"]
    cuts[keep].round(4).to_csv(RES / "threatened_routes.csv", index=False)
    wn = cuts[cuts.entrant == "Southwest"]
    by_lead = wn.groupby("lead_name").agg(routes=("cut", "size"), mean_cut=("cut", "mean"),
                                          median_pre_fare=("pre_fare", "median"),
                                          entry_rate=("entered", "mean")).reset_index()
    by_lead = by_lead[by_lead.routes >= 10].sort_values("routes", ascending=False)
    by_lead["mean_cut_pct"] = 100 * (np.exp(by_lead.mean_cut) - 1)
    by_lead.round(4).to_csv(RES / "southwest_by_incumbent.csv", index=False)
    trig = wn.groupby("trigger").agg(routes=("cut", "size"), onset=("onset_quarter", "first"),
                                     mean_cut=("cut", "mean"), entry_rate=("entered", "mean"),
                                     mean_cut_net=("cut_net", "mean")).reset_index()
    trig["mean_cut_pct"] = 100 * (np.exp(trig.mean_cut) - 1)
    trig["mean_cut_net_pct"] = 100 * (np.exp(trig.mean_cut_net) - 1)
    trig.sort_values("routes", ascending=False).round(4).to_csv(RES / "southwest_by_new_airport.csv", index=False)
    print("\nwrote results/threat_summary.csv, event_study.csv, entry_regression.csv, entry_by_cut_quartile.csv,")
    print("      sample_groups.csv, threatened_routes.csv, southwest_by_incumbent.csv, southwest_by_new_airport.csv")
    pd.set_option("display.width", 200)
    print(summary.T.to_string())

if __name__ == "__main__":
    main()
