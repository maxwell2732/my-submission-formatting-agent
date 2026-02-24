---
name: review-paper
description: Comprehensive manuscript review covering argument structure, methodology, citation completeness, writing quality, and potential referee objections. Works with .docx, .tex, .pdf, and .md manuscripts.
disable-model-invocation: true
argument-hint: "[paper filename in manuscripts/ or master_supporting_docs/, or full path]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Manuscript Review

Produce a thorough, constructive review of an academic manuscript — the kind of report a top-journal referee would write.

**Input:** `$ARGUMENTS` — path to a paper (.docx, .tex, .pdf, .md), or a filename in `manuscripts/` or `master_supporting_docs/`.

---

## Steps

1. **Locate and read the manuscript.** Check:
   - Direct path from `$ARGUMENTS`
   - `manuscripts/$ARGUMENTS`
   - `master_supporting_docs/supporting_papers/$ARGUMENTS`
   - `outputs/` for formatted versions
   - Glob for partial matches

2. **Read the full paper** end-to-end. For long documents, read in sections.

3. **Evaluate across 6 dimensions** (see below).

4. **Generate 3-5 "referee objections"** — the tough questions a top referee would ask.

5. **Produce the review report.**

6. **Save to** `quality_reports/paper_review_[sanitized_name].md`

---

## Review Dimensions

### 1. Argument Structure
- Is the research question clearly stated?
- Does the introduction motivate the question effectively?
- Is the logical flow sound (question → method → results → conclusion)?
- Are the conclusions supported by the evidence?
- Are limitations acknowledged?

### 2. Study Design and Methods
- Is the study design appropriate for the research question?
- Are key methodological assumptions stated explicitly?
- Are there threats to validity (confounding, bias, measurement error)?
- Are statistical methods appropriate?
- Is sample size / power discussed?

### 3. Results and Interpretation
- Are results clearly reported with appropriate statistics?
- Are figures and tables well-designed and self-contained?
- Is interpretation appropriate (not over-claiming)?
- Are negative or null results handled appropriately?

### 4. Literature Positioning
- Are the key papers cited?
- Is prior work characterized accurately?
- Is the contribution clearly differentiated from existing work?
- Any missing citations that a referee would flag?

### 5. Writing Quality
- Clarity and concision
- Academic tone
- Consistent terminology throughout
- Abstract effectively summarizes the paper
- Tables and figures have clear labels, notes, sources

### 6. Formatting and Presentation
- Is the paper the right length for the contribution?
- Is notation / terminology consistent throughout?
- Are there any typos, grammatical errors, or formatting issues?
- Are headings appropriate for the journal type?

---

## Output Format

```markdown
# Manuscript Review: [Paper Title]

**Date:** [YYYY-MM-DD]
**Reviewer:** review-paper skill
**File:** [path to manuscript]

## Summary Assessment

**Overall recommendation:** [Strong Accept / Accept / Revise & Resubmit / Reject]

[2-3 paragraph summary: main contribution, strengths, and key concerns]

## Strengths

1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

## Major Concerns

### MC1: [Title]
- **Dimension:** [Argument / Methods / Results / Literature / Writing / Presentation]
- **Issue:** [Specific description]
- **Suggestion:** [How to address it]
- **Location:** [Section/page if applicable]

[Repeat for each major concern]

## Minor Concerns

### mc1: [Title]
- **Issue:** [Description]
- **Suggestion:** [Fix]

[Repeat]

## Referee Objections

These are the tough questions a top referee would likely raise:

### RO1: [Question]
**Why it matters:** [Why this could be fatal]
**How to address it:** [Suggested response or additional analysis]

[Repeat for 3-5 objections]

## Specific Comments

[Section-by-section comments, if any]

## Summary Ratings

| Dimension | Rating (1-5) |
|-----------|-------------|
| Argument Structure | [N] |
| Study Design / Methods | [N] |
| Results / Interpretation | [N] |
| Literature | [N] |
| Writing | [N] |
| Presentation | [N] |
| **Overall** | **[N]** |
```

---

## Principles

- **Be constructive.** Every criticism should come with a suggestion.
- **Be specific.** Reference exact sections, tables, figures.
- **Distinguish fatal flaws from minor issues.** Not everything is equally important.
- **Acknowledge what's done well.** Good research deserves recognition.
- **Do NOT fabricate details.** If you can't read a section clearly, say so.
- **Do NOT alter scientific content.** This is a review, not an edit.
