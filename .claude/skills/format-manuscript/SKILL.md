# Skill: /format-manuscript

**Trigger phrases:** `/format-manuscript`, "format my manuscript for [journal]", "prepare submission for [journal]", "reformat manuscript"

---

## Instructions

Full manuscript formatting pipeline: ingest → analyze → reformat → export → compliance check → report.

### Arguments

```
/format-manuscript [manuscript-file] [journal-name]
```

- `[manuscript-file]`: Path to manuscript in `manuscripts/` (supports .docx, .tex, .pdf)
- `[journal-name]`: Journal identifier matching a `guidelines/[journal-name].yml` file

### Prerequisites

Before running:
1. `manuscripts/[file]` must exist
2. `guidelines/[journal-name].yml` must exist — run `/parse-guidelines` first if not
3. `templates/reference.docx` must exist — create with `pandoc --print-default-data-file reference.docx > templates/reference.docx`

---

### Step-by-Step Workflow

**Step 1: Setup**

```bash
mkdir -p outputs/[journal-name]
```

Verify prerequisites. If `guidelines/[journal-name].yml` is missing, stop and tell user to run `/parse-guidelines` first.

**Step 2: Ingest**

```bash
python scripts/ingest.py manuscripts/[file] outputs/[journal-name]/working.md
```

Check output:
- If ingest fails: report the error, do not continue
- If `working.md` has `???` or leftover LaTeX commands: note these for cleanup

**Step 3: Analyze**

Launch `manuscript-analyzer` agent:
- Input: `outputs/[journal-name]/working.md` + `guidelines/[journal-name].yml`
- Output: `outputs/[journal-name]/section_inventory.md`

Review the inventory. Identify:
- Missing required sections (auto-draft candidates)
- Sections in wrong order (need reordering)
- Abstract requiring restructuring

**Step 4: Reformat**

Working on `outputs/[journal-name]/working.md`, apply changes IN ORDER:

4a. **Reorder sections**: Move sections to match journal's required order.
    - Do not edit section content, only move headings + their body text.

4b. **Rename headings**: Rename heading text to match journal style.
    - Apply sentence case / title case per `headings.style`.
    - Map manuscript's heading names to journal's required names.

4c. **Restructure abstract**: If journal requires structured abstract:
    - If abstract is present but unstructured: launch `section-drafter` to restructure it.
    - If abstract is present and structured: verify it matches required sections.

4d. **Auto-draft missing sections**: For each missing required section:
    - Launch `section-drafter` agent to generate draft content.
    - Each draft MUST be wrapped in `<!-- DRAFT: requires author review -->` markers.

**Step 5: Save formatted output**

Save the reformatted content as `outputs/[journal-name]/manuscript_formatted.md`.

**Step 6: Export to docx**

```bash
python scripts/export_docx.py outputs/[journal-name]/manuscript_formatted.md outputs/[journal-name]/manuscript_formatted.docx
```

Check that docx was created with non-zero size.

**Step 7: Compliance check**

Launch `compliance-checker` agent:
- Reads `outputs/[journal-name]/manuscript_formatted.md`
- Reads `guidelines/[journal-name].yml`
- Saves `outputs/[journal-name]/compliance_checklist.md`

**Step 8: Quality score**

```bash
python scripts/quality_score.py outputs/[journal-name]/manuscript_formatted.md --rubric manuscript
```

**Step 9: Proofread**

Launch `proofreader` agent on `outputs/[journal-name]/manuscript_formatted.md`.
Save report to `quality_reports/`.

**Step 10: Generate formatting report**

Write `outputs/[journal-name]/formatting_report.md` summarizing:
- All changes made (with before/after for section headings)
- Compliance checklist summary (PASS/WARN/FAIL counts)
- Draft sections requiring author review
- Required author actions
- Quality score

**Step 11: Present summary to user**

```
## Formatting Complete: [journal-name]

**Quality score:** N/100 ([status])

**Changes made:**
- Sections reordered: N
- Headings renamed: N
- Abstract restructured: Yes/No
- Sections auto-drafted: N

**Compliance:**
- PASS: N  WARN: N  FAIL: N

**Draft sections (require author review):**
- [list section names]

**Output files:**
- outputs/[journal]/manuscript_formatted.md
- outputs/[journal]/manuscript_formatted.docx
- outputs/[journal]/formatting_report.md

**Next steps:**
- Review draft sections (marked with <!-- DRAFT --> in the markdown)
- [List any FAIL items from compliance check]
- [Note if word count is over limit]
```

---

## Examples

```
/format-manuscript manuscripts/smith2024_diabetes.docx lancet-eb
```

```
/format-manuscript manuscripts/trial_results.tex nejm
```

---

## Troubleshooting

- **Ingest fails for .pdf:** PDF conversion via pandoc can be lossy. Try extracting text from PDF manually and saving as .txt in manuscripts/, then run again.
- **Pandoc not found:** Install pandoc — `pip install pandoc` or download from pandoc.org.
- **Missing reference.docx:** Run `pandoc --print-default-data-file reference.docx > templates/reference.docx`.
- **Section drafter produces poor drafts:** The source manuscript may lack sufficient content for those sections. Review draft carefully and add `[PLACEHOLDER]` markers for what authors need to fill in.
- **Quality score < 80:** Check the compliance checklist for FAIL items. Most common cause is missing required sections or wrong section order.
