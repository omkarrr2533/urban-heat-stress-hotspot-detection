# Urban Heat Stress Project Report

## Deliverables

- `Urban_Heat_Stress_Hotspot_Detection_Project_Report.docx` — editable Microsoft Word report.
- `Urban_Heat_Stress_Hotspot_Detection_Project_Report.pdf` — rendered PDF companion for quick review and printing.

The checked render is **55 pages**: 9 preliminary pages, 42 numbered main-report pages, 3 appendix pages, and 1 references page. It contains **23 figures** and **31 tables**. Body text and captions are Times New Roman 12 pt; headings are Times New Roman 14 pt.

## Before institutional submission

Replace the editable placeholders on the cover and certificate:

- `[Student Name 1]`–`[Student Name 4]`
- `[Exam No. 1]`–`[Exam No. 4]`

Then complete signatures, submission date, Appendix B publication/presentation details if applicable, and Appendix C with the institute-approved plagiarism/similarity report. No publication outcome or plagiarism percentage has been invented.

The retained academic details are CSMSS Chhatrapati Shahu College of Engineering, DBATU, Computer Science and Engineering, 2026–2027, with Dr. G. J. Sahani, Dr. S. P. Abhang, and Dr. G. B. Dongare as reference signatories.

## Evidence and reproducibility

- `validation_results.json` — 26/26 read-only project checks passed, including API/inference parity and independent V3 spatial-CV reproduction.
- `evidence/v3_oof.npz` — observed and reproduced out-of-fold V3 predictions used for the residual figure.
- `evidence/software_versions.json` — report-preparation environment versions.
- `evidence/layout_qa.json` — page-count, font, caption-page, placeholder, and overflow checks.
- `report_manifest.json` — figure/table/contents page registry used by the builder.
- `assets/` — original diagrams, data plots, college logo, notebook SHAP image, and local dashboard captures.
- `tools/validate_project.py` — read-only technical validation and spatial-CV reproduction.
- `tools/make_figures.py` — regenerates report diagrams and analytical plots from repository data.
- `tools/build_report.py` — regenerates the DOCX and page registry.

From the repository root, with the project and report dependencies installed:

```bash
python report/tools/validate_project.py
python report/tools/make_figures.py
python report/tools/build_report.py
```

The report deliberately separates historical Dataset V2 results from final Dataset V3 results, and separates assumption-based cooling simulations from validated causal effects. Microsoft Word pagination can vary slightly with printer/font metrics; the DOCX uses explicit page breaks and conservative margins, and the supplied PDF is the checked 55-page render.
