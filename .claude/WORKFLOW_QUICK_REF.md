# Workflow Quick Reference — Manuscript Submission Formatting Agent

**Model:** Contractor (you direct, Claude orchestrates)

---

## The Loop

```
Your instruction
    ↓
[PLAN] (if multi-file or unclear) → Show plan → Your approval
    ↓
[EXECUTE] Ingest → Analyze → Reformat → Export → Compliance check → Report
    ↓
[REPORT] Summary + output files + required author actions
    ↓
Repeat
```

---

## Core Workflow (Start Here)

```bash
# Step 1: Parse journal guidelines (one-time per journal)
/parse-guidelines [journal-name] [URL]

# Step 2: Format the manuscript
/format-manuscript manuscripts/paper.docx [journal-name]

# Step 3: Review draft sections, then validate
/validate-compliance outputs/[journal]/manuscript_formatted.md [journal-name]
```

---

## I Ask You When

- **Design forks:** "Manuscript has two Results sections — merge or keep?"
- **Content ambiguity:** "Cannot determine which paragraph maps to 'Background' — clarify?"
- **Scope question:** "Also proofread while formatting, or just format?"
- **Missing data:** "Cannot auto-draft Data Availability — do you have a repository URL?"

---

## I Just Execute When

- Formatting is rules-based (section reorder, heading rename, heading case)
- Ingest / export commands
- Compliance checking (mechanical against guidelines YAML)
- Auto-drafting from existing content (always marked DRAFT)
- Proofreading (report only, no edits)

---

## Quality Gates (No Exceptions)

| Score | Action |
|-------|--------|
| >= 80 | Ready to commit / deliver |
| < 80  | Fix blocking compliance issues first |

---

## Non-Negotiables

- **Never alter scientific content** — only formatting, structure, headings
- **Draft markers always used** — `<!-- DRAFT -->` on all auto-generated content
- **manuscripts/ is read-only** — always work in outputs/
- **Both .md and .docx delivered** — never just one format

---

## Preferences

<!-- Fill in as you discover your working style -->

**Reporting:** Concise bullet summary + full compliance checklist in separate file
**Draft sections:** Always mark, never silently insert
**Session logs:** Always (post-plan, incremental, end-of-session)
**Word count:** Flag WARN but never cut content automatically

---

## Exploration Mode

For testing or experimenting with new journals, use the **Fast-Track** workflow:
- Work in `explorations/` folder
- 60/100 quality threshold (vs. 80/100 for production)
- No plan needed — just a value check
- See `.claude/rules/exploration-fast-track.md`

---

## Key File Locations

| What | Where |
|------|-------|
| Input manuscripts | `manuscripts/` (read-only) |
| Journal guidelines | `guidelines/[journal].yml` |
| Working copy | `outputs/[journal]/working.md` |
| Formatted output | `outputs/[journal]/manuscript_formatted.md/.docx` |
| Compliance report | `outputs/[journal]/compliance_checklist.md` |
| Formatting report | `outputs/[journal]/formatting_report.md` |
| Reference template | `templates/reference.docx` |
| Guidelines schema | `templates/journal-requirements.yml` |

---

## Next Step

You provide task → I plan (if needed) → Your approval → Execute → Done.
