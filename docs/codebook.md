# Coding codebook

One row per label. Identifier columns (brand, nonproprietary_name, payload, payload_class) are pre-filled; code every other column. Use the allowed values exactly as written (lowercase with underscores). A detail may follow a code in parentheses, eg, `monitor (strong CYP3A4 inhibitors)`; the agreement script ignores parenthetical text. Section numbers refer to the Full Prescribing Information; [HIGHLIGHTS] marks Highlights text.

General rules: code what the label says, not what is known about the drug elsewhere. "Payload" means the unconjugated or released cytotoxic small molecule. When a label is silent, use `not_stated` (substrate columns) or `none` (Section 7 columns).

| Column | Allowed values | Definition and where to look |
|---|---|---|
| `initial_us_approval` | Year (YYYY) | Year stated as "Initial U.S. Approval" in the Highlights (document title line). |
| `section7_present` | yes; no | yes if the Full Prescribing Information contains Section 7 Drug Interactions (heading "7 DRUG INTERACTIONS", LOINC 34073-7). Highlights alone do not count. |
| `section7_content` | payload_pk; other_only; none | payload_pk: Section 7 addresses any pharmacokinetic interaction affecting the ADC or its payload. other_only: Section 7 addresses only pharmacodynamic interactions (eg, QT-prolonging drugs). none: no Section 7. |
| `cyp3a_substrate` | yes; no; not_stated | Section 12.3. yes: the payload (unconjugated or released form) is a substrate of, or is metabolized by, CYP3A (CYP3A4 or CYP3A4/5). no: the label states the payload is not a substrate of CYP3A or of CYP enzymes. not_stated: CYP3A metabolism of the payload is not described. |
| `cyp3a_evidence` | clinical_study; clinical_study_no_significant_change; pbpk; extrapolation_same_payload; population_pk_with_in_vitro; clinical_or_model_informed_no_significant_change; in_vitro; blank | Only when cyp3a_substrate is yes; otherwise leave blank. Code the most direct evidence in Section 12.3 for the CYP3A interaction statement, in this order of directness: clinical_study (clinical interaction study showing increased exposure); clinical_study_no_significant_change (clinical study showing no clinically significant change); clinical_or_model_informed_no_significant_change (clinical and model-informed evaluation together showing no clinically significant change); pbpk (PBPK or other model-based prediction of an exposure change); extrapolation_same_payload (exposure changes reported for a different ADC with the same payload); population_pk_with_in_vitro (population pharmacokinetic covariate comparison of patients with and without concomitant inhibitors, alongside in vitro data); in_vitro (in vitro statements only). |
| `cyp3a_section7` | avoid; monitor; mentioned; none | Highest level stated in Section 7 for CYP3A inhibitors. avoid: avoid concomitant use (with or without instructions if unavoidable). monitor: monitor or closely monitor for adverse reactions or toxicity. mentioned: interaction or exposure effect stated without a management instruction. none: CYP3A not addressed or no Section 7. |
| `cyp3a_section7_includes_moderate_inhibitors` | yes; no | yes if the Section 7 CYP3A guidance explicitly applies to moderate CYP3A inhibitors; no otherwise (including no Section 7). |
| `pgp_substrate` | yes; possible; no; not_stated | Section 12.3. possible: the label describes the payload as a possible or potential P-gp substrate. Other values as for cyp3a_substrate. |
| `pgp_section7` | avoid; monitor; mentioned; none | As for cyp3a_section7, coded only if Section 7 names P-gp or a P-gp-defined inhibitor class (eg, "dual P-gp and strong CYP3A4 inhibitors"). |
| `bcrp_substrate` | yes; no; not_stated | Section 12.3, as for cyp3a_substrate. |
| `bcrp_section7` | avoid; monitor; mentioned; none | As for pgp_section7, for BCRP. |
| `oatp1b_substrate` | yes; no; not_stated | Section 12.3: substrate of OATP1B1 and/or OATP1B3. |
| `oatp1b_section7` | avoid; monitor; mentioned; none | As for pgp_section7, for OATP1B. |
| `other_transporters_substrate` | names separated by "; " (eg, MRP1; BSEP); no; not_stated | Transporters other than P-gp, BCRP, and OATP1B for which Section 12.3 designates the payload a substrate (yes or possible), listed by the names used in the label. |
| `other_transporters_section7` | avoid; monitor; mentioned; none | As for pgp_section7, for those transporters. |
| `ugt1a1_substrate` | yes; no; not_stated | Section 12.3 (or Section 12.5 if present): the payload is metabolized (glucuronidated) by UGT1A1. |
| `ugt1a1_section7` | avoid; monitor; mentioned; none | As for cyp3a_section7, for UGT1A1 inhibitors or inducers. |
| `strong_cyp3a_inhibitor_change` | signed percent (eg, +34%) or blank | Change in unconjugated payload exposure with a strong CYP3A inhibitor reported in Section 12.3. Use the AUC estimate if both AUC and Cmax are given; convert fold changes to percent (1.4-fold = +40%). Blank if no quantitative estimate. |
| `strong_cyp3a_inducer_change` | signed percent (eg, -46%) or blank | As above, for a strong CYP3A inducer. |
| `change_metric` | AUC; Cmax; or the label's wording (eg, MMAE exposure); blank | Metric for the two change columns above. |
| `inducer_section7` | avoid; monitor; mentioned; mentioned_highlights_only; none; not_applicable | For labels reporting a payload exposure change with a strong CYP3A inducer: how Section 7 addresses inducers. mentioned_highlights_only: inducers addressed only in the Highlights drug interaction summary, not in Full Prescribing Information Section 7. none: not addressed. not_applicable: Section 12.3 reports no inducer effect. |
| `inducer_clinical_significance_stated` | yes; no; not_applicable | yes if Section 7 or 12.3 states whether the inducer-associated decrease is clinically significant (including "no clinically significant" or "unknown"); not_applicable if no inducer effect is reported. |
| `example_drugs_listed` | yes; no | yes if Section 7 names individual drugs within an interacting class (eg, ketoconazole). no if it does not, or if there is no Section 7. |
| `fda_list_referenced` | yes; no | yes if Section 7 refers readers to FDA's online list of CYP- and transporter-based interacting drugs. |
| `genotype_guided_dosing` | yes; no; not_applicable | Section 2: a starting dose or dose modification by genotype. not_applicable if the label states no pharmacogenomic liability for the payload. |
| `notes` | free text | Anything relevant to the codes in this row. Begin with UNCERTAIN: when a code is a judgment call. |
