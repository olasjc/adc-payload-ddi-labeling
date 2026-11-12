"""Identify US antibody-drug conjugate (ADC) labels and extract interaction-relevant sections.

Step 1: structured openFDA search for labels describing the product as an antibody-drug or antibody and agent conjugate.
Step 2: download the current structured product labeling (SPL) for each included ADC from DailyMed (web services v2)
        and extract sections by LOINC code: Drug Interactions 34073-7, Pharmacokinetics 43682-4,
        Dosage and Administration 34068-7, Warnings and Precautions 43685-7, Contraindications 34070-3;
        12.5 Pharmacogenomics is located by section title.
Outputs (written to ../data): openfda_search_results.csv, labels_extracted.json, label_inventory.csv
Labels change frequently; rerunning on a later date may return newer versions.
"""
import csv, json, re, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
UA = {"User-Agent": "Mozilla/5.0 (research script)"}
NS = {"v3": "urn:hl7-org:v3"}

def get(url, timeout=120):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()

# ---------------- Step 1: openFDA universe search ----------------
QUERIES = [(f, t) for f in ["indications_and_usage", "description"]
           for t in ['"antibody-drug conjugate"', '"drug conjugate"', '"inhibitor conjugate"', '"agent conjugate"', '"antibody and"']]
hits = {}
for field, term in QUERIES:
    q = f"{field}:{term}"
    try:
        d = json.loads(get("https://api.fda.gov/drug/label.json?search=" + urllib.parse.quote(q) + "&limit=100"))
        n = d["meta"]["results"]["total"]
    except Exception:  # openFDA returns HTTP 404 when a query has no matches
        d, n = {"results": []}, 0
    print(f"{q:45s} {n:3d} labels")
    for r in d["results"]:
        of = r.get("openfda", {})
        brand = (of.get("brand_name") or [""])[0]
        if not brand:
            brand = "[no openfda fields] " + (r.get("spl_product_data_elements") or [""])[0][:80]
        h = hits.setdefault(r["set_id"], dict(set_id=r["set_id"], brand=brand, generic=(of.get("generic_name") or [""])[0],
                                                 product_type=(of.get("product_type") or [""])[0], effective=r.get("effective_time", ""), queries=set()))
        h["queries"].add(q)

# Included ADCs (brand: nonproprietary name). Screening of all hits is documented in openfda_search_results.csv;
# a superseded 2022 belantamab mafodotin SPL (issued before the 2022 withdrawal) is excluded in favor of the current label.
ADCS = {"ADCETRIS": "brentuximab vedotin", "PADCEV": "enfortumab vedotin", "POLIVY": "polatuzumab vedotin",
        "TIVDAK": "tisotumab vedotin", "EMRELIS": "telisotuzumab vedotin", "BLENREP": "belantamab mafodotin",
        "KADCYLA": "ado-trastuzumab emtansine", "ELAHERE": "mirvetuximab soravtansine", "ENHERTU": "fam-trastuzumab deruxtecan",
        "DATROWAY": "datopotamab deruxtecan", "TRODELVY": "sacituzumab govitecan", "ZYNLONTA": "loncastuximab tesirine",
        "DECNUPAZ": "pivekimab sunirine", "BESPONSA": "inotuzumab ozogamicin", "MYLOTARG": "gemtuzumab ozogamicin"}
def is_adc(brand):
    b = brand.upper().replace("[NO OPENFDA FIELDS] ", "")
    return any(b.startswith(k) for k in ADCS)
with open(DATA / "openfda_search_results.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["set_id", "brand_name", "generic_name", "product_type", "effective_time", "adc_label", "matched_queries"])
    for h in sorted(hits.values(), key=lambda x: x["brand"].upper()):
        w.writerow([h["set_id"], h["brand"], h["generic"], h["product_type"], h["effective"], "yes" if is_adc(h["brand"]) else "no",
                    "; ".join(sorted(h["queries"]))])
print("unique labels returned:", len(hits), "| ADC labels among them:", sum(is_adc(h["brand"]) for h in hits.values()))

# ---------------- Step 2: DailyMed retrieval and section extraction ----------------
def text(el):
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip() if el is not None else ""

out = {}
for brand, generic in ADCS.items():
    lst = json.loads(get("https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name=" + urllib.parse.quote(brand)))["data"]
    lst = [d for d in lst if brand.lower() in d["title"].lower()] or lst
    rec = max(lst, key=lambda d: d["published_date"]) if len(lst) > 1 else lst[0]
    raw = get(f'https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{rec["setid"]}.xml')
    root = ET.fromstring(raw)
    flat = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw.decode("utf-8", "ignore"))).replace("\xa0", " ")
    approval = re.search(r"Initial\s+U\.?\s*S\.?\s*Approval\s*:?\s*(\d{4})", flat, re.I)
    labeler = root.find(".//v3:author//v3:representedOrganization/v3:name", NS)
    version = root.find("v3:versionNumber", NS)
    sections = {}
    for s in root.iter("{urn:hl7-org:v3}section"):
        c = s.find("v3:code", NS)
        sections.setdefault(c.get("code") if c is not None else "", []).append((text(s.find("v3:title", NS)), text(s)))
    first = lambda code: sections.get(code, [("", "")])[0][1]
    pgx = next((tx for v in sections.values() for ti, tx in v if re.search(r"12\.5\s*Pharmacogenomics", ti, re.I)), "")
    out[brand] = dict(brand=brand, generic=generic, setid=rec["setid"], published=rec["published_date"],
                      spl_version=version.get("value") if version is not None else "", title=rec["title"],
                      initial_us_approval=approval.group(1) if approval else None, labeler=labeler.text if labeler is not None else None,
                      section7=first("34073-7"), section12_3=first("43682-4"), section12_5=pgx,
                      section2=first("34068-7"), section5=first("43685-7"), section4=first("34070-3"))
    print(f'{brand:9s} {rec["setid"]}  {rec["published_date"]}  approval {out[brand]["initial_us_approval"]}  Section 7: {"yes" if out[brand]["section7"] else "no"}')
json.dump(out, open(DATA / "labels_extracted.json", "w"), indent=1, ensure_ascii=False)
with open(DATA / "label_inventory.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["brand", "nonproprietary_name", "labeler", "dailymed_set_id", "spl_version", "version_date", "initial_us_approval", "section7_present"])
    for r in out.values():
        w.writerow([r["brand"], r["generic"], r["labeler"], r["setid"], r["spl_version"], r["published"], r["initial_us_approval"], "yes" if r["section7"] else "no"])
