# Formatting Report
**Manuscript:** Climate Change and Diversity and Quality of Food-away-from-home: Evidence from a Large-scale Chain Restaurant
**Authors:** Chen Zhu, Rigoberto Lopez, Xiaoou Liu, Xun Li
**Target journal:** Australian Journal of Agricultural and Resource Economics (AJARE)
**Date formatted:** 2026-02-24

---

## Summary

| Item | Before | After |
|------|--------|-------|
| Abstract | Unstructured (continuous text) | Structured with Introduction/Methods/Results/Conclusion labels |
| Plain Language Summary | Absent | Auto-drafted (DRAFT — requires author review) |
| Methods section heading | "Data and method" | "Materials and methods" |
| Sub-heading case | 2 headings had incorrect case | Fixed to sentence case |
| Discussion section | "Policy implications" (missing Discussion) | "Discussion" (see author action below) |
| Author block | Inline in manuscript | Flagged for removal to separate title page |
| Data availability statement | Absent | Auto-drafted template (DRAFT) |
| Funding statement | Absent | Auto-drafted template (DRAFT) |
| Conflict of interest | Absent | Auto-drafted template (DRAFT) |
| Reference format | Unchanged | Unchanged (AJARE free format submission) |
| Word count | ~7,200 words | ~7,361 words (within 6,000–10,000 limit) |

---

## Changes Made

### 1. Abstract — Restructured

**Before:** Unstructured abstract (continuous paragraph)

**After:** Structured abstract with four bolded sub-section labels:
- **Introduction:** — context and study aim
- **Methods:** — dataset, models, approach
- **Results:** — key findings
- **Conclusion:** — implications

*AJARE requires a structured abstract. The original text was preserved verbatim; labels were added based on the natural paragraph breaks.*

---

### 2. Plain Language Summary — Auto-drafted

**Before:** Absent

**After:** DRAFT section added below the abstract (marked `<!-- DRAFT: requires author review -->`)

*AJARE encourages (but does not require) a Plain Language Summary of ≤200 words with no technical jargon. The auto-drafted text (~152 words) summarises the study's key message for a general audience. The author should review and revise as appropriate.*

---

### 3. Methods Section Heading — Renamed

**Before:** `## 2. Data and method`

**After:** `## 2. Materials and methods`

*AJARE's accepted headings include "Materials and Methods", "Methods", "Methodology", and "Data and Methods". "Data and method" (singular) is non-standard and was renamed to the preferred form.*

---

### 4. Sub-heading Case — Corrected

Two sub-headings had words capitalised that should not be under sentence case:

| Before | After |
|--------|-------|
| `### 2.4 Empirical Models` | `### 2.4 Empirical models` |
| `### 3.6 Robustness check: Impacts by group size` | `### 3.6 Robustness check: impacts by group size` |

*Sentence case is standard for Wiley journals including AJARE. All other headings were already in sentence case.*

---

### 5. Section "Policy Implications" — Renamed to "Discussion"

**Before:** `## 4. Policy implications`

**After:** `## 4. Discussion`

**⚠️ Author decision required.** AJARE requires a Discussion section. The original manuscript had "Policy implications" but no separate Discussion section. Two options:

- **Option A (recommended):** Expand Section 4 to include interpretation of results, comparison with prior literature, limitations, and policy implications — covering the full scope of a Discussion section.
- **Option B:** If the authors prefer to keep a focused policy section, add a brief Discussion section before it (merging Discussion and Conclusion is also acceptable per AJARE guidelines).

A `<!-- NOTE FOR AUTHOR -->` comment is embedded in the file at this section.

---

### 6. Author Block — Flagged for Double-anonymous Review

**Before:** Author names and affiliations appeared in the manuscript body.

**After:** Author block is preserved in an HTML comment with explicit instructions to move it to a separate title page file. The block will not appear in the rendered submission.

*AJARE uses double-anonymous peer review. Author-identifying information must appear ONLY on the title page file, not in the main manuscript.*

---

### 7. DRAFT Sections Added

Three required sections were absent from the original manuscript and have been auto-drafted:

| Section | Content |
|---------|---------|
| **Data availability statement** | Template with three options (open repository / available on request / proprietary). Author selects appropriate option and fills in details. |
| **Funding** | Placeholder — author lists all funding sources and grant numbers. |
| **Conflict of interest** | Placeholder — author declares or states no conflict. |

All three sections are marked with `<!-- DRAFT: requires author review -->` / `<!-- END DRAFT -->`.

---

## Compliance Checklist

See `compliance_checklist.md` for the full PASS/WARN/FAIL breakdown.

Quick summary:
- **20 PASS** — section presence, abstract structure, headings, word count, references, draft markers
- **5 WARN** — Plain Language Summary (draft), Discussion scope, and three missing disclosures (data availability, funding, conflict of interest)
- **1 FAIL** — ORCID IDs (required for all authors; not present)

---

## Required Author Actions

The following items **must** be completed before submission:

### Critical (FAIL)
1. **ORCID IDs** — Add all four authors' ORCID IDs to the title page file.

### Required (WARN — blocks submission if left as DRAFT)
2. **Author block** — Remove the HTML-commented author block from `manuscript_formatted.md`. Create a separate title page file containing: title, authors, affiliations, ORCID IDs, acknowledgements, funding, data availability, and conflict of interest.
3. **Data availability statement** — Select one of the three template options and complete the required details.
4. **Funding statement** — List all funding sources with grant numbers in the Acknowledgements section (per AJARE guidelines).
5. **Conflict of interest** — Declare any conflicts or state "no conflict of interest."
6. **Discussion section** — Decide whether to expand Section 4 into a full Discussion or restructure (see Change #5 above).

### Optional / Encouraged
7. **Plain Language Summary** — Review and revise the auto-drafted text. Must be ≤200 words, no jargon. This is optional but encouraged by AJARE.
8. **Ethics/AI statement** — Add to Methods or Acknowledgements if AI tools were used for content generation.
9. **Figures** — The 8 figures (image1–image8) were not bundled with the pandoc-converted markdown. Upload the original figure files (TIFF, EPS, or PDF at highest resolution) as separate files at revision stage.
10. **Word count** — Final count ~7,361 words (estimated from markdown). Confirm in Word; AJARE limit is 6,000–10,000 words inclusive of abstract, references, notes, figures, and tables.

---

## Files Delivered

| File | Description |
|------|-------------|
| `outputs/ajare/manuscript_formatted.md` | Formatted manuscript (Markdown — source of truth for editing) |
| `outputs/ajare/manuscript_formatted.docx` | Formatted manuscript (Word — ready to open and finalize) |
| `outputs/ajare/compliance_checklist.md` | PASS/WARN/FAIL checklist for every AJARE requirement |
| `outputs/ajare/formatting_report.md` | This file — full change summary and required actions |
| `outputs/ajare/working.md` | Normalized source (pandoc output from original .docx, unformatted) |

---

## What Was NOT Changed

Per this tool's design principles, the following were **not** altered:

- All numerical results, statistical values, and figures
- All citations and reference entries (free format submission — typesetter handles style)
- Conclusions and interpretations
- Tables and their content
- Footnotes
- Scientific content of any kind

---

*Formatted by Manuscript Submission Formatting Agent (Claude Code) — 2026-02-24*
