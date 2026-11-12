"""Search FDA approval letters for payload-related postmarketing requirements or commitments.

Retrieves each application's document list from the openFDA drugsfda endpoint, downloads every approval
letter (original and supplemental) listed there, extracts text with pdftotext (Poppler), and flags lines
mentioning interactions, CYP enzymes, transporters, PBPK, or UGT1A1. Output: ../data/fda_letters_scan.csv.
Flagged lines were then read in context to classify each item (see manuscript Supplementary Table S5).
"""
import csv, json, re, subprocess, tempfile, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
UA = {"User-Agent": "Mozilla/5.0 (research script)"}
BRANDS = ["ADCETRIS", "PADCEV", "POLIVY", "TIVDAK", "EMRELIS", "BLENREP", "KADCYLA", "ELAHERE", "ENHERTU",
          "DATROWAY", "TRODELVY", "ZYNLONTA", "DECNUPAZ", "BESPONSA", "MYLOTARG"]
KW = re.compile(r"interact|CYP3A|CYP\d|ketoconazole|itraconazole|rifamp|inducer|transporter|P-gp|PBPK|physiologic|UGT1A1", re.I)

def get(url, timeout=120):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()

jobs = []
for b in BRANDS:
    d = json.loads(get("https://api.fda.gov/drug/drugsfda.json?search=openfda.brand_name:%22" + urllib.parse.quote(b) + "%22&limit=5"))
    for r in d["results"]:
        seen = set()
        for s in r.get("submissions", []):
            for doc in s.get("application_docs") or []:
                url = doc.get("url", "").replace("http://", "https://")
                if doc.get("type") == "Letter" and url not in seen:
                    seen.add(url)
                    jobs.append((b, r["application_number"], s.get("submission_type"), s.get("submission_number"), s.get("submission_status_date"), url))

def scan(job):
    b, app, st, sn, date, url = job
    with tempfile.NamedTemporaryFile(suffix=".pdf") as fh:
        fh.write(get(url.replace(" ", "%20"))); fh.flush()
        text = subprocess.run(["pdftotext", "-layout", fh.name, "-"], capture_output=True, text=True).stdout
    lines = [re.sub(r"\s+", " ", l).strip() for l in text.splitlines() if KW.search(l)]
    return [b, app, f"{st} {sn}", date, url, len(text), " | ".join(lines)]

with ThreadPoolExecutor(8) as ex:
    rows = list(ex.map(scan, jobs))
with open(DATA / "fda_letters_scan.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["brand", "application", "submission", "action_date", "letter_url", "text_chars", "flagged_lines"])
    w.writerows(sorted(rows, key=lambda r: (r[0], r[3])))
print(f"{len(rows)} letters scanned; {sum(1 for r in rows if r[6])} with flagged lines")
