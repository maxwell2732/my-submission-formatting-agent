# Session Log: Manuscript Submission Formatting Agent Setup

**Date:** 2026-02-24
**Goal:** Repurpose academic workflow template repo into a manuscript submission formatting agent
**Status:** COMPLETE

---

## What Was Done

Implemented the full setup plan for the manuscript submission formatting agent. Transformed a Beamer/Quarto slide development repo into a manuscript formatting pipeline.

### Phase 1: Configuration Updates
- Updated `CLAUDE.md` — replaced slide-centric content with manuscript workflow context
- Filled all `[BRACKETED PLACEHOLDERS]` with meaningful defaults

### Phase 2: Removed Irrelevant Infrastructure
- Deleted 9 slide/R/TikZ-specific rules
- Deleted 7 slide-specific agents (beamer-translator, quarto-critic, quarto-fixer, slide-auditor, pedagogy-reviewer, tikz-reviewer, r-reviewer)
- Deleted 11 slide/R/TikZ-specific skill directories
- Removed `Slides/`, `Quarto/`, `Preambles/` directories

### Phase 3: New Directory Structure
- Created `manuscripts/` (read-only input store)
- Created `guidelines/` (journal requirements YAML)
- Created `outputs/` (formatted output per journal)

### Phase 4: New Rules
- `.claude/rules/manuscript-handling.md` — ingest pipeline + content integrity rules
- `.claude/rules/journal-compliance.md` — section order, abstract structure, heading style
- `.claude/rules/output-generation.md` — pandoc export, formatting report requirements
- Updated `.claude/rules/quality-gates.md` — manuscript compliance rubric

### Phase 5: New Agents
- `manuscript-analyzer.md` — section inventory, IMRaD detection, gap analysis
- `guidelines-extractor.md` — URL/text → structured YAML
- `section-drafter.md` — synthesize missing sections from existing content (always DRAFT)
- `compliance-checker.md` — systematic PASS/WARN/FAIL compliance checklist
- Updated `proofreader.md` — adapted for manuscripts (draft marker integrity, formatting artifacts)
- Updated `verifier.md` — adapted for docx/md output verification

### Phase 6: New Skills
- `parse-guidelines/` — extracts journal requirements from URL or pasted text
- `format-manuscript/` — full pipeline orchestrator (11-step workflow)
- `validate-compliance/` — standalone compliance check
- `generate-report/` — formatting_report.md with before/after diff
- Updated `proofread/` and `review-paper/` for manuscript context

### Phase 7: Scripts
- `scripts/ingest.py` — pandoc wrapper for .docx/.tex/.pdf → markdown
- `scripts/export_docx.py` — pandoc wrapper for markdown → docx with reference template
- Updated `scripts/quality_score.py` — added `ManuscriptScorer` class + `--rubric manuscript` flag

### Phase 8: Templates
- `templates/reference.docx` — pandoc default reference document (created via pandoc)
- `templates/journal-requirements.yml` — annotated schema template for journal YAML files
- `templates/formatting-report.md` — report template for formatting outputs
- Updated `.claude/WORKFLOW_QUICK_REF.md` — manuscript workflow context
- Updated `MEMORY.md` — [LEARN] entries for manuscript agent patterns

---

## Key Decisions

1. **manuscripts/ is read-only** — protects originals; work always happens on outputs/ copies
2. **Draft markers mandatory** — no auto-drafted content without `<!-- DRAFT -->` wrapper
3. **Word count = WARN not FAIL** — authors decide what to cut, tool never deletes content
4. **Both .md and .docx always delivered** — .md for version control/editing, .docx for submission
5. **guidelines.yml is single source of truth** — all compliance checks read from this file

---

## Verification Remaining

End-to-end verification (run when pandoc + sample manuscript available):
1. `python scripts/ingest.py manuscripts/sample.docx outputs/test/working.md`
2. `python scripts/export_docx.py outputs/test/working.md outputs/test/out.docx`
3. `/parse-guidelines [name] [URL]`
4. `/format-manuscript manuscripts/sample.docx [journal]`
5. `python scripts/quality_score.py outputs/test/working.md --rubric manuscript`

---

## Open Questions

- None. Setup complete. Ready for first real manuscript.

---

## Next Steps for User

1. Run `/parse-guidelines [journal-name] [URL]` to set up your first journal
2. Drop a manuscript into `manuscripts/`
3. Run `/format-manuscript manuscripts/[file] [journal-name]`

---
**Context compaction () at 21:36**
Check git log and quality_reports/plans/ for current state.
