# Payload-level drug interaction labeling of antibody-drug conjugates: data and code

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24174267.svg)](https://doi.org/10.5281/zenodo.24174267)

Data and code for a cross-sectional analysis of drug interaction guidance in the US prescribing information of the 15 FDA-approved antibody-drug conjugates (ADCs) with current labeling. For each label, the study coded where payload interaction liabilities appear (Section 12.3, Clinical Pharmacology, versus Section 7, Drug Interactions), the evidence behind any Section 7 guidance, and consistency among products that share a payload. FDA approval letters and selected FDA reviews were examined for the regulatory basis of the recommendations. Labels were retrieved from DailyMed on November 12, 2026.

Associated manuscript (under review): *Payload-Class Consistency of Drug Interaction Guidance in US Labeling of Antibody-Drug Conjugates: A Cross-Sectional Analysis.*

## Contents

| Path | Description |
|---|---|
| `code/01_identify_and_extract.py` | Runs the openFDA universe search, downloads current structured product labeling (SPL) from DailyMed, and extracts Sections 2, 4, 5, 7, 12.3, and 12.5. Writes the files marked *generated*. |
| `code/02_make_figures.py` | Draws Figures 1 and 2 from the coded values into `fig/` (PNG 300 dpi, TIFF 600 dpi, vector PDF, JPG). |
| `code/03_regulatory_records.py` | Downloads every FDA approval letter listed for the 15 applications in the openFDA drugsfda endpoint and flags lines about interactions, CYP enzymes, transporters, PBPK, or UGT1A1. Requires Poppler `pdftotext`. |
| `code/04_agreement.py` | Percent agreement and Cohen's kappa between two independent codings, with a disagreement list for consensus. |
| `data/coding_sheet.csv` | Analysis dataset: one row per label, coded as defined in `docs/codebook.md`. |
| `data/coding_sheet_BLANK.csv` | The coding sheet with only identifiers filled, for independent second coding. |
| `data/label_inventory.csv` | *Generated.* One row per included label: set ID, SPL version and date, labeler, initial US approval. |
| `data/labels_extracted.json` | *Generated.* Extracted section text for the 15 labels. |
| `data/label_full_text/` | Full text of each label's SPL as retrieved, with section headings, LOINC codes, and Highlights marked. |
| `data/section7_text.csv` | Section 7 text of the 10 labels that have one. |
| `data/openfda_search_results.csv` | *Generated.* All 73 labels returned by the 10 openFDA phrase searches, with the queries each matched and an ADC flag. |
| `data/fda_letters_scan.csv` | *Generated.* 89 approval letters with URLs and flagged lines. |
| `data/fda_review_excerpts.csv` | Verbatim excerpts from the FDA letters and reviews cited in the manuscript, with URLs and PDF page numbers. |
| `docs/codebook.md` | Definition and allowed values of every coded column. |
| `sources/fda/` | The cited FDA approval letters and the cited pages of 4 FDA reviews; `index.csv` gives each source URL and original page numbers. |
| `fig/` | Figure files produced by `02_make_figures.py`. |

## Reproducing the analysis

Requires Python 3.10 or later (tested with 3.12) and the packages in `requirements.txt`; `01` and `03` need internet access, and `03` needs Poppler `pdftotext`.

```bash
pip install -r requirements.txt
cd data && python3 ../code/01_identify_and_extract.py && cd ..   # search, download, extract
python3 code/02_make_figures.py                                   # figures
python3 code/03_regulatory_records.py                             # approval-letter scan
python3 code/04_agreement.py data/coding_sheet.csv data/coding_sheet_coder2.csv   # after second coding
```

Labels are revised often, so rerunning `01` later may retrieve newer versions and overwrite the generated files. To compare with the analyzed versions, run it in a copy of the repository and compare `label_inventory.csv` with the version dates listed here.

## Coding

Codes were assigned against the verbatim label text using `docs/codebook.md`. Substrate columns record whether Section 12.3 designates the unconjugated payload a substrate of each pathway; Section 7 columns record the highest level of guidance for that pathway (`avoid`, `monitor`, `mentioned`, or `none`); `cyp3a_evidence` records the most direct evidence cited for the CYP3A statement. For independent second coding, copy `coding_sheet_BLANK.csv` to `coding_sheet_coder2.csv`, code it from `data/label_full_text/` without viewing `coding_sheet.csv`, and run `04_agreement.py`, which also writes `data/disagreements.csv` for consensus. Perpetrator potential of the payload and interactions involving the antibody were not coded.

## Sources and third-party content

Label text was obtained from DailyMed (US National Library of Medicine) and openFDA. FDA approval letters and review pages were obtained from Drugs@FDA; source URLs are in `data/fda_letters_scan.csv` and `sources/fda/index.csv`. This third-party content is included so that every code can be checked against its source; it is not covered by the licenses below and remains subject to the terms of its source.

## Licenses

Code in `code/` is released under the MIT License (`LICENSE`). Data and documentation created for this study (the coding sheets, inventory and search-result tables, codebook, and figures) are released under CC BY 4.0 (`LICENSE-DATA`).

## Citation

Li R, Chen ZS. Payload-level drug interaction labeling of antibody-drug conjugates: data and code. Zenodo; 2026. doi:10.5281/zenodo.24174267

This DOI covers all versions and resolves to the latest. To cite the exact version analyzed in the associated manuscript, use version 1.0.1: doi:10.5281/zenodo.24174501. Citation metadata are in `CITATION.cff` (GitHub: "Cite this repository").

## Contact

Corresponding author: Zhe-Sheng Chen, Department of Pharmaceutical Sciences, College of Pharmacy and Health Sciences, St. John's University, Queens, NY, USA (chenz@stjohns.edu).
