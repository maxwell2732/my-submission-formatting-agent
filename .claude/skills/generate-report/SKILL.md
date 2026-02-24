# Skill: /generate-report

**Trigger phrases:** `/generate-report`, "generate formatting report", "summarize changes for [journal]", "what changes were made"

---

## Instructions

Generate a `formatting_report.md` that documents every change made between the original manuscript and the formatted output, with before/after examples.

### Arguments

```
/generate-report [journal-name]
```

- `[journal-name]`: Journal identifier (used to locate `outputs/[journal-name]/` files)

### Workflow

**Step 1: Verify files**

Check that these exist:
- `outputs/[journal-name]/working.md` (original ingest)
- `outputs/[journal-name]/manuscript_formatted.md` (formatted version)
- `guidelines/[journal-name].yml` (requirements)
- `outputs/[journal-name]/compliance_checklist.md` (if available)

**Step 2: Compare and document changes**

Read both `working.md` and `manuscript_formatted.md`. For each difference:

1. **Section reordering**: List sections moved, with before/after positions
   - Before: position N, After: position M
2. **Heading renames**: List all heading text changes
   - Before: "Study population and methods", After: "Methods"
3. **Abstract restructuring**: Note if abstract was restructured
   - Before: unstructured paragraph, After: structured with Background/Methods/Findings/Interpretation
4. **Auto-drafted sections**: List sections added by the formatter
   - Section name, word count, which source material was used
5. **Heading style changes**: Note if case was changed globally
   - "Applied sentence case to all H1/H2 headings (N headings changed)"

**Step 3: Include compliance summary**

If `compliance_checklist.md` exists, include a condensed version:
- PASS/WARN/FAIL counts
- FAIL items (if any)
- WARN items (if any)

**Step 4: Write the report**

Save to `outputs/[journal-name]/formatting_report.md` using this structure:

```markdown
# Formatting Report: [Journal Name]
**Date:** [YYYY-MM-DD]
**Source:** [original filename]
**Formatted:** manuscript_formatted.md / manuscript_formatted.docx

---

## Summary

| Category | Count |
|----------|-------|
| Sections reordered | N |
| Headings renamed | N |
| Heading style applied | N |
| Abstract restructured | Yes/No |
| Sections auto-drafted | N |

**Overall compliance:** PASS / WARN / FAIL (N PASS, N WARN, N FAIL)

---

## Changes Made

### 1. Section Order

Before → After:

| Before Position | Section | After Position |
|----------------|---------|----------------|
| 3 | Methods | 2 |
| 2 | Introduction | 1 |

### 2. Heading Renames

| Original Heading | New Heading | Reason |
|-----------------|-------------|--------|
| "Patients and Methods" | "Methods" | Journal style |

### 3. Heading Style

Applied [sentence case / title case] to all H1/H2 headings.
Changed: N headings.

Examples:
- "Study Design And Methods" → "Study design and methods"
- "Statistical Analysis" → "Statistical analysis"

### 4. Abstract Restructuring

Before: Unstructured paragraph (N words)
After: Structured with sections: Background / Methods / Findings / Interpretation

[Or: Abstract was already structured. Sections verified against requirements.]

### 5. Auto-Drafted Sections

The following sections were auto-drafted and require author review:

#### [Section Name]
- **Required by journal:** Yes (position N)
- **Source material:** Synthesized from Introduction (lines 45-67) and Discussion (lines 234-245)
- **Word count:** N words
- **Marked with:** `<!-- DRAFT: requires author review -->`

---

## Compliance Checklist Summary

| Check | Status | Notes |
|-------|--------|-------|
| All required sections present | PASS/WARN/FAIL | [notes] |
| Correct section order | PASS/WARN/FAIL | [notes] |
| Structured abstract | PASS/WARN/FAIL | [notes] |
| Word count | PASS/WARN (N words, limit N) | [notes] |
| Heading style | PASS/WARN/FAIL | [notes] |
| Data availability | PASS/WARN/FAIL | [notes] |
| Funding statement | PASS/WARN/FAIL | [notes] |
| Conflicts of interest | PASS/WARN/FAIL | [notes] |

Full checklist: `outputs/[journal]/compliance_checklist.md`

---

## Required Author Actions

Before submission, the author must:

1. **Review all DRAFT sections** — open `manuscript_formatted.md` and search for `<!-- DRAFT -->`. Each section needs author verification and editing.
2. [List any FAIL items from compliance checklist]
3. [List any WARN items the author should decide on]
4. [Note if word count is over limit and by how much]

---

## Files Delivered

- `outputs/[journal]/manuscript_formatted.md` — formatted markdown (edit-friendly)
- `outputs/[journal]/manuscript_formatted.docx` — formatted Word document (for submission)
- `outputs/[journal]/compliance_checklist.md` — detailed compliance results
- `outputs/[journal]/formatting_report.md` — this file

**Do not edit the original manuscript at:** `manuscripts/[filename]`
```

---

## Examples

```
/generate-report lancet-eb
```

```
/generate-report nejm
```

---

## Troubleshooting

- **working.md missing:** Ingest step was not run. Run `/format-manuscript` first, or run `python scripts/ingest.py` manually.
- **Cannot determine what changed:** If working.md and manuscript_formatted.md are identical, the manuscript may have already been compliant. Note this in the report.
