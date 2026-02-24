---
paths:
  - "outputs/**"
---

# Output Generation Rules

## docx Export

- **Always** use `templates/reference.docx` as the pandoc reference document:
  ```bash
  pandoc --from=markdown --to=docx --reference-doc=templates/reference.docx \
         input.md -o output.docx
  ```
- Heading styles must match the reference template's Heading 1/2/3 styles.
  Do not override heading styles inline.
- Figures referenced by relative path in markdown are embedded in docx by pandoc automatically.
  Verify figure paths are correct before export.

## Markdown Output

- Save both `.md` (for version control / diff) and `.docx` (for submission) in
  `outputs/[journal]/`.
- The `.md` file is the source of truth. The `.docx` is derived.
- Line length in output markdown: wrap at 100 characters for readability in diffs.

## Formatting Report

- Every formatted output MUST be accompanied by `outputs/[journal]/formatting_report.md`.
- Report uses `templates/formatting-report.md` as its template.
- Report includes:
  1. Summary of all changes made (section additions, reordering, heading renames)
  2. Compliance checklist (PASS/WARN/FAIL for each journal requirement)
  3. Draft sections requiring author review
  4. Items requiring author action (word count, reference style, etc.)
- Reports are for the author — write clearly, not for Claude.

## Output Directory Structure

```
outputs/[journal]/
├── working.md                  # Normalized source (from ingest)
├── manuscript_formatted.md     # Final formatted markdown
├── manuscript_formatted.docx   # Final formatted docx
└── formatting_report.md        # Change summary + compliance checklist
```

## Naming Conventions

- Journal name in directory: lowercase, hyphenated (e.g., `lancet-eb`, `nejm`, `plos-one`)
- Do not use spaces or uppercase in directory names.

## Verification Before Delivery

Before marking a formatted output complete:
1. Confirm `outputs/[journal]/manuscript_formatted.docx` exists and has non-zero size
2. Confirm `outputs/[journal]/formatting_report.md` exists
3. Confirm no orphaned `<!-- DRAFT -->` markers are unclosed
4. Confirm quality score >= 80 via `python scripts/quality_score.py`
