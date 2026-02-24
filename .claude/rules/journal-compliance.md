---
paths:
  - "guidelines/**"
  - "outputs/**"
---

# Journal Compliance Rules

## Requirements Loading

- **Always** load `guidelines/[journal].yml` before beginning any formatting work.
  If the file doesn't exist, run `/parse-guidelines` first.
- Validate the YAML is well-formed before using it. Missing required fields are a blocking error.

## Section Order

- Section order in the formatted manuscript **must exactly match** the journal's `sections_required`
  list in order.
- If the manuscript has sections not in the journal's list: keep them, but note them in the
  formatting report as `[UNRECOGNIZED SECTION — author should verify]`.

## Abstract Structure

- Abstract structure is a **hard requirement**. The abstract must have exactly the headings listed
  in `abstract.structure`, in order.
- If the original abstract is unstructured: reconstruct it by assigning sentences/paragraphs to
  the required sections. Each section header should be bolded: **Background**, **Methods**, etc.
- If a required abstract section has no clear corresponding content: draft a placeholder and mark
  `<!-- DRAFT -->`.

## Word Limits

- Word limits are **soft warnings** (not hard blocks).
- If total word count exceeds `word_limit.total`: flag in compliance report as WARN, not FAIL.
- If abstract word count exceeds `abstract.word_limit`: flag as WARN.
- Never delete content to meet word limits. Authors decide what to cut.

## Auto-Drafted Sections

- When a journal requires a section that the manuscript lacks, auto-draft it from existing content.
- Priority order for source material: methods section, discussion section, conclusions section.
- Never invent data or results. Synthesize only from text already in the manuscript.
- Mark every auto-drafted section with `<!-- DRAFT: requires author review -->`.

## Heading Style

- Apply `headings.style` uniformly:
  - `"sentence case"`: Only first word and proper nouns capitalized (e.g., "Study design and participants")
  - `"title case"`: All major words capitalized (e.g., "Study Design and Participants")
- Apply to all section and subsection headings.

## Reference Format

- Reference format (`references.style`) is noted in the compliance report.
- Automatic conversion of reference formats is not attempted (too error-prone).
- Flag in report: "Reference style should be [style]. Manual conversion may be needed."

## Special Requirements

- For each item in `special_requirements`: check if it exists in the manuscript.
  Report PASS / WARN / FAIL with location if found.
