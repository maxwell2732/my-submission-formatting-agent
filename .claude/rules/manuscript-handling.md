---
paths:
  - "manuscripts/**"
  - "outputs/**"
---

# Manuscript Handling Rules

## Ingest Pipeline

- **Always** convert source manuscripts to canonical markdown via `scripts/ingest.py` before editing.
  The canonical markdown in `outputs/[journal]/working.md` is the working copy.
- **Never** edit the original file in `manuscripts/`. That directory is read-only.
- For `.pdf` sources: treat as read-only reference. The ingest step reconstructs content via pandoc;
  verify reconstructed text against the PDF before proceeding.
- For `.tex` sources: use pandoc's LaTeX reader. Equations may need manual cleanup post-ingest;
  flag any `???` or `\begin{unknown}` remnants.
- For `.docx` sources: pandoc handles these cleanly. Check that tables and figures round-trip.

## Content Integrity

- **Never alter scientific content** — do not rephrase sentences, modify numbers, change citations,
  or reorder information within a section.
- Only permissible changes:
  1. Adding/removing/renaming section headings to match journal style
  2. Reordering top-level sections to match journal's required order
  3. Reformatting the abstract to match journal's abstract structure
  4. Auto-drafting missing required sections (MUST be marked `<!-- DRAFT -->`)
  5. Reformatting citation style (e.g., numbered → author-year)
- If in doubt whether a change touches scientific content, flag it in the formatting report
  with `[AUTHOR REVIEW REQUIRED]`.

## Draft Markers

Any auto-drafted content MUST be wrapped:
```
<!-- DRAFT: requires author review -->
[drafted content here]
<!-- END DRAFT -->
```

Never remove draft markers. Authors remove them after reviewing.

## Working with Outputs

- Work on `outputs/[journal]/working.md`, not the original manuscript.
- Always save both `.md` and `.docx` versions.
- `formatting_report.md` accompanies every formatted output.
