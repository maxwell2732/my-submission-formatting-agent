# CLAUDE.MD -- Manuscript Submission Formatting Agent

**Project:** Manuscript Submission Formatting Agent
**Institution:** [YOUR INSTITUTION]
**Branch:** main

---

## Core Principles

- **Plan first** -- enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** -- run ingest + export and confirm outputs at end of every task
- **Never alter scientific content** -- reformat only; flag any content-touching changes for author review
- **Draft markers required** -- auto-drafted sections MUST be tagged `<!-- DRAFT: requires author review -->`
- **Quality gates** -- nothing ships below 80/100
- **[LEARN] tags** -- when corrected, save `[LEARN:category] wrong → right` to MEMORY.md

---

## Folder Structure

```
my-submission-formatting-agent/
├── CLAUDE.md                    # This file
├── .claude/                     # Rules, skills, agents, hooks
├── Bibliography_base.bib        # Centralized bibliography
├── Figures/                     # Figures and diagrams
├── manuscripts/                 # Input manuscripts (read-only originals)
├── guidelines/                  # Parsed journal requirements (.yml)
├── outputs/                     # Formatted outputs per journal
│   └── [journal-name]/
│       ├── working.md           # Normalized markdown (working copy)
│       ├── manuscript_formatted.docx
│       ├── manuscript_formatted.md
│       └── formatting_report.md
├── docs/                        # GitHub Pages
├── scripts/                     # ingest.py, export_docx.py, quality_score.py
├── quality_reports/             # Plans, session logs, merge reports
├── explorations/                # Research sandbox
├── templates/                   # reference.docx, journal-requirements.yml, etc.
└── master_supporting_docs/      # Reference papers
```

---

## Commands

```bash
# Ingest manuscript → normalized markdown
python scripts/ingest.py manuscripts/paper.docx outputs/journal/working.md
python scripts/ingest.py manuscripts/paper.tex  outputs/journal/working.md
python scripts/ingest.py manuscripts/paper.pdf  outputs/journal/working.md

# Export markdown → formatted docx
python scripts/export_docx.py outputs/journal/working.md outputs/journal/manuscript_formatted.docx

# Compliance quality score
python scripts/quality_score.py outputs/journal/manuscript_formatted.md --rubric manuscript

# Generate reference.docx template (run once to set up)
pandoc --print-default-data-file reference.docx > templates/reference.docx
```

---

## Quality Thresholds

| Score | Gate | Meaning |
|-------|------|---------|
| 80 | Commit | Good enough to save |
| 90 | PR | Ready for delivery |
| 95 | Excellence | Aspirational |

---

## Skills Quick Reference

| Command | What It Does |
|---------|-------------|
| `/parse-guidelines [name] [URL]` | Extract journal requirements → guidelines/[name].yml |
| `/format-manuscript [file] [journal]` | Full formatting pipeline (ingest → reformat → export) |
| `/validate-compliance [file] [journal]` | Standalone compliance check on formatted output |
| `/generate-report [journal]` | Generate formatting_report.md with before/after diff |
| `/proofread [file]` | Grammar/typo/consistency review |
| `/review-paper [file]` | Substantive manuscript review |
| `/commit [msg]` | Stage, commit, push |
| `/lit-review [topic]` | Literature search + synthesis |
| `/research-ideation [topic]` | Research questions + strategies |
| `/interview-me [topic]` | Interactive research interview |
| `/validate-bib` | Cross-reference citations |
| `/devils-advocate` | Challenge formatting decisions |

---

## Journal Requirements YAML Schema

Key fields in `guidelines/[journal].yml`:

| Field | Description |
|-------|-------------|
| `journal` | Journal name |
| `sections_required` | Ordered list with name, level, position, word_limit |
| `abstract.structure` | Required abstract sections in order |
| `headings.style` | "sentence case" or "title case" |
| `word_limit.total` | Total word limit |
| `references.style` | "Vancouver", "APA", "AMA", etc. |
| `special_requirements` | List of additional requirements |

---

## Current Project State

| Journal | Guidelines | Sample Output | Notes |
|---------|-----------|---------------|-------|
| [journal-name] | `guidelines/[name].yml` | `outputs/[name]/` | [Brief description] |
