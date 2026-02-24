# Skill: /validate-compliance

**Trigger phrases:** `/validate-compliance`, "check compliance", "verify compliance for [journal]", "does this meet [journal] requirements"

---

## Instructions

Standalone compliance check on an already-formatted manuscript. Useful for iterative refinement after manual edits.

### Arguments

```
/validate-compliance [output-file] [journal-name]
```

- `[output-file]`: Path to the formatted markdown file (e.g., `outputs/lancet-eb/manuscript_formatted.md`)
- `[journal-name]`: Journal identifier matching a `guidelines/[journal-name].yml` file

### Workflow

**Step 1: Verify files exist**

- Check `[output-file]` exists
- Check `guidelines/[journal-name].yml` exists
- If either is missing: stop and tell the user what's needed

**Step 2: Launch compliance-checker agent**

Pass both files to the `compliance-checker` agent.
Agent saves `outputs/[journal-name]/compliance_checklist.md` and returns a summary.

**Step 3: Run quality score**

```bash
python scripts/quality_score.py [output-file] --rubric manuscript
```

**Step 4: Present results**

Display the compliance summary:
- Overall status (PASS / WARN / FAIL)
- PASS / WARN / FAIL counts
- Any FAIL items (these must be fixed before submission)
- Quality score
- Recommended next steps

---

## Examples

```
/validate-compliance outputs/lancet-eb/manuscript_formatted.md lancet-eb
```

```
/validate-compliance outputs/nejm/draft_v2.md nejm
```

---

## Troubleshooting

- **FAIL on section order:** The formatter may need to be re-run, or you can manually move sections in the markdown.
- **WARN on word count:** This is informational only — the author decides whether to trim content.
- **FAIL on special requirements:** Check if the manuscript has a data availability statement, funding statement, or conflicts of interest section. Add if missing.
