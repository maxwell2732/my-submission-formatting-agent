---
name: proofread
description: Run the proofreading protocol on manuscript files. Checks grammar, typos, draft marker integrity, consistency, and academic writing quality. Produces a report without editing files.
disable-model-invocation: true
argument-hint: "[filename or path to manuscript .md/.docx/.tex]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Proofread Manuscript

Run the proofreading protocol on a manuscript file. Produces a report of all issues found WITHOUT editing any source files.

## Steps

1. **Identify the file to review:**
   - If `$ARGUMENTS` is a specific filename: review that file
   - Look in `outputs/`, `manuscripts/`, or use the exact path given

2. **Launch the proofreader agent** which checks for:

   **GRAMMAR:** Subject-verb agreement, articles (a/an/the), prepositions, tense consistency
   **TYPOS:** Misspellings, leftover placeholder text, duplicated words
   **DRAFT MARKERS:** Check that every `<!-- DRAFT -->` has a matching `<!-- END DRAFT -->`
   **CONSISTENCY:** Citation format, terminology, abbreviations, units
   **FORMATTING ARTIFACTS:** Leftover LaTeX commands, stray markdown syntax, double spaces
   **ACADEMIC STYLE:** Informal language, incomplete sentences, awkward constructions

3. **Produce a detailed report** for each file listing every finding with:
   - Location (line number or section heading)
   - Current text (what's wrong)
   - Proposed fix (what it should be)
   - Category and severity

4. **Save the report** to `quality_reports/[FILENAME]_proofread.md`

5. **IMPORTANT: Do NOT edit any source files.**
   Only produce the report. Fixes are applied separately after user review.

6. **Present summary** to the user:
   - Total issues found
   - Breakdown by category
   - Draft marker status
   - Most critical issues highlighted
