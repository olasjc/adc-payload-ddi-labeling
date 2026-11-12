"""Inter-rater agreement between two independent codings of the labels.

Usage:  python3 code/04_agreement.py data/coding_sheet.csv data/coding_sheet_coder2.csv
Both files must have the same columns and one row per label (matched on 'brand').
Coder 2 should code blind, starting from a copy of coding_sheet.csv with every coded column cleared.
Reports percent agreement and Cohen's kappa for each coded variable and pooled across variables,
and writes a disagreement list for consensus review (data/disagreements.csv).
"""
import csv, sys
from collections import Counter

CODED = ["section7_present", "section7_content", "cyp3a_substrate", "cyp3a_evidence", "cyp3a_section7",
         "cyp3a_section7_includes_moderate_inhibitors", "pgp_substrate", "pgp_section7", "bcrp_substrate", "bcrp_section7",
         "oatp1b_substrate", "oatp1b_section7", "ugt1a1_substrate", "ugt1a1_section7", "inducer_section7",
         "inducer_clinical_significance_stated", "example_drugs_listed", "fda_list_referenced", "genotype_guided_dosing"]

def norm(v):
    v = (v or "").strip().lower()
    return v.split(" (")[0]  # ignore parenthetical detail, e.g. "yes (11 strong CYP3A4 inhibitors)"

def kappa(pairs):
    n = len(pairs)
    if n == 0: return float("nan")
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)

def main(f1, f2):
    a = {r["brand"]: r for r in csv.DictReader(open(f1, encoding="utf-8"))}
    b = {r["brand"]: r for r in csv.DictReader(open(f2, encoding="utf-8"))}
    brands = sorted(set(a) & set(b))
    missing = sorted(set(a) ^ set(b))
    if missing: print("Labels present in only one file:", missing)
    pooled, dis = [], []
    print(f"{'variable':45s} {'agree':>7s} {'kappa':>7s}")
    for v in CODED:
        pairs = [(norm(a[x].get(v)), norm(b[x].get(v))) for x in brands]
        pooled += pairs
        agree = sum(p == q for p, q in pairs) / len(pairs)
        k = kappa(pairs)
        print(f"{v:45s} {agree:7.0%} {k:7.2f}" if k == k else f"{v:45s} {agree:7.0%}     n/a")
        dis += [(x, v, a[x].get(v), b[x].get(v)) for x in brands if norm(a[x].get(v)) != norm(b[x].get(v))]
    agree = sum(p == q for p, q in pooled) / len(pooled)
    print(f"\nPooled across {len(CODED)} variables x {len(brands)} labels: agreement {agree:.1%}, kappa {kappa(pooled):.2f}")
    print(f"Disagreements: {len(dis)} (written to data/disagreements.csv)")
    with open("data/disagreements.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["brand", "variable", "coder1", "coder2", "consensus"]); w.writerows([d + ("",) for d in dis])

if __name__ == "__main__":
    if len(sys.argv) != 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
