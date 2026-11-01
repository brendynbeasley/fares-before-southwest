"""Collapse the DOT airline ticket sample (DB1B Market, 2014-2024) into two quarterly tables.

DB1B is a 10% random sample of domestic airline tickets, published every quarter by the Bureau of
Transportation Statistics. Each quarterly zip is about 100 MB (1.6 GB unzipped), so the 44 raw files
are fetched into data/raw/db1b/ when they are missing and are ignored by git. This script reads only
the columns it needs, applies the ticket filters below and writes two compact tables that
src/limit_pricing.py reads:

  data/derived/route_quarter_*.csv.gz  airport pair x quarter: sampled passengers and fare revenue in
                                       total, for each watched airline, and for the three largest
                                       ticketing airlines on the pair
  data/derived/airport_quarter.csv.gz  airport x airline x quarter: sampled passengers the airline
                                       itself flew out of or into the airport (its presence there)

Airport pairs are non-directional (ATL-BOS and BOS-ATL are one route). Counts are sample counts
(multiply by ten for all passengers). Fares are nominal dollars per one-way market trip.

Usage (from the repository root):
    python src/build_panel.py                          # fetches any missing zip from BTS
    python src/build_panel.py --raw-dir path/to/zips --workers 4
"""

import argparse
import zipfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.csv as pv
import requests

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "db1b"
OUT = ROOT / "data" / "derived"
URL = "https://transtats.bts.gov/PREZIP/Origin_and_Destination_Survey_DB1BMarket_{y}_{q}.zip"

YEARS = range(2014, 2025)
FARE_MIN, FARE_MAX = 25.0, 2500.0  # one-way fare bounds: below are award and employee tickets, above are
                                   # coding errors (the usual cut in work with DB1B)
MAX_COUPONS = 3                    # at most two connections in a direction
MIN_ROUTE_PAX = 50                 # route-quarters with fewer sampled tickets (about 500 real) are dropped
WATCHED = ["WN", "NK", "F9", "G4", "B6"]  # Southwest, Spirit, Frontier, Allegiant, JetBlue

COLS = ["MktCoupons", "Origin", "Dest", "TkCarrierChange", "OpCarrierChange", "TkCarrier", "OpCarrier",
        "BulkFare", "Passengers", "MktFare", "NonStopMiles"]


def fetch(raw_dir, year, quarter):
    path = raw_dir / f"Origin_and_Destination_Survey_DB1BMarket_{year}_{quarter}.zip"
    if path.exists():
        return path
    raw_dir.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".part")
    print(f"  downloading {URL.format(y=year, q=quarter)}", flush=True)
    with requests.get(URL.format(y=year, q=quarter), stream=True, timeout=900) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    tmp.rename(path)
    return path


def one_quarter(args):
    raw_dir, year, quarter = args
    path = fetch(raw_dir, year, quarter)
    with zipfile.ZipFile(path) as z:
        name = [n for n in z.namelist() if n.endswith(".csv")][0]
        with z.open(name) as f:
            d = pv.read_csv(f, convert_options=pv.ConvertOptions(include_columns=COLS)).to_pandas()
    n0 = len(d)

    keep = ((d.BulkFare == 0) & d.MktFare.between(FARE_MIN, FARE_MAX)
            & (d.MktCoupons <= MAX_COUPONS) & (d.TkCarrierChange == 0))
    d = d[keep].copy()
    d["a"] = np.minimum(d.Origin, d.Dest)
    d["b"] = np.maximum(d.Origin, d.Dest)
    d["rev"] = d.MktFare * d.Passengers
    d["ns"] = np.where(d.MktCoupons == 1, d.Passengers, 0.0)
    # the ticketing airline flew the trip itself (no regional partner or codeshare in the market)
    own = (d.OpCarrierChange == 0) & (d.OpCarrier == d.TkCarrier)

    # airport presence: passengers an airline itself flew out of or into each airport
    o = d[own].groupby(["Origin", "TkCarrier"]).Passengers.sum()
    o.index.names = ["airport", "carrier"]
    t = d[own].groupby(["Dest", "TkCarrier"]).Passengers.sum()
    t.index.names = ["airport", "carrier"]
    ap = o.add(t, fill_value=0).rename("pax").reset_index()
    ap["year"], ap["quarter"] = year, quarter

    # route x carrier totals
    rc = d.groupby(["a", "b", "TkCarrier"]).agg(pax=("Passengers", "sum"), rev=("rev", "sum"),
                                                ns=("ns", "sum")).reset_index()
    route = d.groupby(["a", "b"]).agg(pax=("Passengers", "sum"), rev=("rev", "sum"), ns=("ns", "sum"),
                                      miles=("NonStopMiles", "median"))
    for c in WATCHED:
        sub = rc[rc.TkCarrier == c].set_index(["a", "b"])
        route[f"pax_{c}"] = sub.pax
        route[f"rev_{c}"] = sub.rev
        route[f"ns_{c}"] = sub.ns
    rc = rc.sort_values(["a", "b", "pax"], ascending=[True, True, False])
    rc["rank"] = rc.groupby(["a", "b"]).cumcount() + 1
    for k in (1, 2, 3):
        sub = rc[rc["rank"] == k].set_index(["a", "b"])
        route[f"c{k}"] = sub.TkCarrier
        route[f"pax{k}"] = sub.pax
        route[f"rev{k}"] = sub.rev
    route = route.reset_index()
    n_routes = len(route)
    route = route[route.pax >= MIN_ROUTE_PAX]
    num = [c for c in route.columns if c.startswith(("pax", "rev", "ns"))]
    route[num] = route[num].fillna(0).round().astype("int64")
    route["year"], route["quarter"] = year, quarter
    msg = (f"{year} Q{quarter}: {n0:,} market records; kept {keep.sum():,} after fare, bulk, coupon and "
           f"interline filters, dropped {(~keep).sum():,}; {n_routes:,} airport pairs, kept {len(route):,} "
           f"with >= {MIN_ROUTE_PAX} sampled passengers")
    return msg, route, ap


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-dir", type=Path, default=RAW)
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()

    jobs = [(args.raw_dir, y, q) for y in YEARS for q in (1, 2, 3, 4)]
    routes, airports = [], []
    with ProcessPoolExecutor(args.workers) as ex:
        for msg, r, a in ex.map(one_quarter, jobs):
            print(msg, flush=True)
            routes.append(r)
            airports.append(a)

    OUT.mkdir(parents=True, exist_ok=True)
    route = pd.concat(routes, ignore_index=True)
    for lo, hi in ((2014, 2019), (2020, 2024)):  # two files, each under 10 MB
        part = route[route.year.between(lo, hi)]
        part.to_csv(OUT / f"route_quarter_{lo}_{hi}.csv.gz", index=False)
        print(f"wrote data/derived/route_quarter_{lo}_{hi}.csv.gz ({len(part):,} route-quarters)")
    airport = pd.concat(airports, ignore_index=True)
    airport = airport[airport.pax > 0]
    airport.to_csv(OUT / "airport_quarter.csv.gz", index=False)
    print(f"wrote data/derived/airport_quarter.csv.gz ({len(airport):,} airport-airline-quarters)")


if __name__ == "__main__":
    main()
