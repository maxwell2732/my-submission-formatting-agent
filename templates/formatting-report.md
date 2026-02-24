# Formatting Report: [Journal Name]

**Date:** [YYYY-MM-DD]
**Source manuscript:** `manuscripts/[filename]`
**Journal guidelines:** `guidelines/[journal-name].yml`
**Formatted output:** `outputs/[journal-name]/manuscript_formatted.md` + `.docx`

---

## Summary

| Category | Count |
|----------|-------|
| Sections reordered | N |
| Headings renamed | N |
| Heading style applied | N headings changed |
| Abstract restructured | Yes / No |
| Sections auto-drafted | N |
| **Overall compliance** | PASS / WARN / FAIL |

---

## Changes Made

### 1. Section Order

The following sections were moved to match the journal's required order:

| Section | Original Position | New Position |
|---------|-----------------|--------------|
| [section name] | [N] | [M] |

*No sections reordered.* (if applicable)

---

### 2. Heading Renames

| Original Heading | New Heading | Reason |
|-----------------|-------------|--------|
| "[original]" | "[new]" | Match journal required section name |

*No headings renamed.* (if applicable)

---

### 3. Heading Style

Applied **[sentence case / title case]** to all H1/H2 headings per journal requirements.

Changed: N headings.

Examples:
- "[Original Heading Text]" → "[Reformatted heading text]"

*No heading style changes needed.* (if applicable)

---

### 4. Abstract Restructuring

**Before:** Unstructured paragraph (N words)

**After:** Structured with required sections:
- **[Section 1]:** [first sentence of that section]
- **[Section 2]:** [first sentence of that section]
- ...

*Abstract was already correctly structured.* (if applicable)

---

### 5. Auto-Drafted Sections

The following sections were auto-drafted because the original manuscript did not contain them. **These require author review before submission.**

#### [Section Name]
- **Required by journal:** Yes (position N in required order)
- **Source material used:** [e.g., "Synthesized from Introduction paragraphs 2-3 and Discussion paragraph 5"]
- **Word count:** N words
- **Marked with:** `<!-- DRAFT: requires author review -->`
- **What author should do:** [specific instructions]

*No sections were auto-drafted.* (if applicable)

---

## Compliance Checklist

| Requirement | Status | Notes |
|-------------|--------|-------|
| All required sections present | PASS / WARN / FAIL | [notes] |
| Correct section order | PASS / WARN / FAIL | [notes] |
| Structured abstract | PASS / WARN / FAIL | [notes] |
| Word count | PASS / WARN ([N] words, limit [M]) | [notes] |
| Heading style | PASS / WARN / FAIL | [notes] |
| Data availability statement | PASS / WARN / FAIL | [notes] |
| Funding statement | PASS / WARN / FAIL | [notes] |
| Conflicts of interest | PASS / WARN / FAIL | [notes] |
| [Other special requirements] | PASS / WARN / FAIL | [notes] |

Full checklist: `outputs/[journal-name]/compliance_checklist.md`

**Quality score:** N/100 ([PASS / WARN / BLOCKED])

---

## Required Author Actions

Before submitting, the author must complete these steps:

- [ ] **Review all DRAFT sections** — open `manuscript_formatted.md` and search for `<!-- DRAFT -->`. Edit each section to confirm or replace the auto-drafted content.
- [ ] [Other action from FAIL compliance items]
- [ ] [Action if word count over limit]
- [ ] [Action if reference style needs conversion]
- [ ] Verify figure files are in correct format ([format]) and resolution ([DPI])

---

## Files Delivered

| File | Description |
|------|-------------|
| `outputs/[journal]/manuscript_formatted.md` | Formatted markdown (edit-friendly, version control) |
| `outputs/[journal]/manuscript_formatted.docx` | Formatted Word document (for submission) |
| `outputs/[journal]/compliance_checklist.md` | Detailed compliance results |
| `outputs/[journal]/formatting_report.md` | This file |

**The original manuscript has NOT been modified:** `manuscripts/[filename]`

---

## Notes

[Any additional observations, limitations of the automatic formatting, or items the formatter was uncertain about.]
