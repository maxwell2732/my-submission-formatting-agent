# Manuscript Submission Formatting Agent

A structured Claude Code workflow to reformat research manuscripts for any journal's submission requirements — without altering scientific content.

**Last Updated:** 2026-03-15

---

## The problem

Every journal has different formatting requirements: structured abstracts, specific section ordering, heading styles, citation formats, word limits, required declarations. Reformatting a manuscript for a new journal — or after a rejection — is tedious, error-prone, and takes hours of work that adds zero scientific value.

## The solution

Give this agent your manuscript and a journal's author guidelines URL. It parses the requirements, restructures your paper to comply, auto-drafts any missing required sections (clearly marked for your review), and delivers a submission-ready `.docx` with a compliance report.

**What it never does:**
- Alter your scientific content (numbers, results, citations, conclusions)
- Silently add text — all auto-drafted sections are visibly marked `<!-- DRAFT: requires author review -->`
- Cut content to meet word limits — those are flagged as warnings for you to decide

> **Privacy:** `manuscripts/` and `outputs/` are gitignored. Your manuscripts never leave your machine or get pushed to GitHub.

---

## Quick start

### 1. Clone and open

```bash
git clone https://github.com/maxwell2732/my-submission-formatting-agent.git
cd my-submission-formatting-agent
claude
```

### 2. Set up a journal (one-time per journal)

```
/parse-guidelines ije https://academic.oup.com/ije/pages/general_instructions
```

This fetches the author guidelines and saves structured requirements to `guidelines/ije.yml`.

> **Tip:** If the journal's website blocks automated access (403 error), paste the guidelines text when prompted — the agent will extract requirements from the pasted content instead.

### 3. Format your manuscript

Drop your manuscript into `manuscripts/`, then:

```
/format-manuscript manuscripts/my_paper.docx ije
```

The agent will ingest your manuscript, analyse its structure, reformat it to comply with the journal's requirements, and deliver:

| Output file | What it is |
|-------------|-----------|
| `outputs/ije/manuscript_formatted.docx` | Submission-ready Word document |
| `outputs/ije/manuscript_formatted.md` | Markdown version (for version control and editing) |
| `outputs/ije/compliance_checklist.md` | PASS/WARN/FAIL for every journal requirement |
| `outputs/ije/formatting_report.md` | Summary of every change made + required author actions |

### 4. Review and submit

Open the formatting report, complete any DRAFT sections, address warnings, and submit.

---

## What it handles

The formatting pipeline (`/format-manuscript`) runs 11 steps automatically:

1. **Ingest** — converts .docx, .tex, or .pdf to normalised markdown via pandoc
2. **Analyse structure** — identifies sections, detects IMRaD structure, compares against journal requirements
3. **Reorder sections** — moves sections to match the journal's required order
4. **Rename headings** — applies the journal's heading naming convention and case style
5. **Restructure abstract** — converts to the journal's required structured format (e.g., Background/Methods/Results/Conclusions)
6. **Draft missing sections** — synthesises content for required sections that are absent (Key Messages, Declarations, etc.)
7. **Convert citations** — adjusts citation format (e.g., author-year to Vancouver superscript)
8. **Export** — produces `.docx` using a reference template and `.md` for version control
9. **Compliance check** — PASS/WARN/FAIL checklist for every journal requirement
10. **Quality score** — 0-100 compliance score (80 = acceptable, 90 = delivery-ready)
11. **Proofread** — grammar, typos, consistency, draft marker integrity

---

## Supported input formats

| Format | Quality | Notes |
|--------|---------|-------|
| `.tex` (LaTeX) | Best | Preserves structure, equations, citations |
| `.docx` (Word) | Good | Standard manuscript format |
| `.pdf` | Acceptable | Lossy conversion — review output carefully |

---

## Example: formatting for IJE

Here's what happens when formatting a ~10,000-word epidemiology manuscript for the International Journal of Epidemiology (3,000-word limit, structured abstract, Key Messages required):

**Structural changes made automatically:**
- Abstract restructured from 4-part to IJE's required 4-part format (Background/Methods/Results/Conclusions), trimmed to 250 words
- "Policy Background" section merged into Introduction
- "Data and Methods" + "Identification Strategy" merged into "Methods"
- "Main Results" + "Investigating the Mechanisms" reorganised into "Results"
- Section numbers stripped, sentence case applied to all headings
- Key Messages (3 bullets), Keywords, and 7 Declaration subsections auto-drafted

**Flagged for author action:**
- Word count 3,900 vs 3,000 limit (WARN — author decides what to cut)
- STROBE checklist required (observational study)
- 10 DRAFT placeholder sections to complete before submission

**Quality score: 90/100**

---

## All commands

| Command | What it does |
|---------|-------------|
| `/parse-guidelines [name] [URL]` | Extract journal requirements → `guidelines/[name].yml` |
| `/format-manuscript [file] [journal]` | Full formatting pipeline |
| `/validate-compliance [file] [journal]` | Standalone compliance check on any formatted file |
| `/generate-report [journal]` | Generate formatting report with before/after diff |
| `/proofread [file]` | Grammar, typos, draft marker check |
| `/review-paper [file]` | Substantive manuscript review (argument, methods, referee objections) |
| `/validate-bib` | Cross-reference citations against bibliography |
| `/devils-advocate` | Challenge formatting decisions |
| `/commit [msg]` | Stage, commit, push |

---

## What's included

<details>
<summary><strong>7 agents, 11 skills, 10 rules, 4 hooks</strong> (click to expand)</summary>

### Agents (`.claude/agents/`)

| Agent | What it does |
|-------|-------------|
| `manuscript-analyzer` | Section inventory, IMRaD detection, gap analysis vs. journal requirements |
| `guidelines-extractor` | URL or pasted text → structured `guidelines/[journal].yml` |
| `section-drafter` | Synthesises missing required sections from existing manuscript content (always marks DRAFT) |
| `compliance-checker` | PASS/WARN/FAIL checklist for every journal requirement |
| `proofreader` | Grammar, typos, draft marker integrity, formatting artifacts |
| `verifier` | Checks output files exist, are valid, and quality score passes |
| `domain-reviewer` | **Template** — customise for your field's substance review |

### Rules (`.claude/rules/`)

**Always-on:**

| Rule | What it enforces |
|------|-----------------|
| `plan-first-workflow` | Plan mode for non-trivial tasks + context preservation |
| `orchestrator-protocol` | Contractor mode: implement → verify → review → fix → score |
| `session-logging` | Post-plan, incremental, and end-of-session logs |
| `meta-governance` | What belongs in the repo vs. gitignored |

**Path-scoped** (load only when working on matching files):

| Rule | Triggers on | What it enforces |
|------|------------|-----------------|
| `manuscript-handling` | `manuscripts/`, `outputs/` | Ingest pipeline, content integrity, draft markers |
| `journal-compliance` | `guidelines/`, `outputs/` | Section order, abstract structure, heading style |
| `output-generation` | `outputs/` | pandoc export, formatting report requirements |
| `quality-gates` | `outputs/` | 80/90/95 scoring thresholds, manuscript rubric |
| `proofreading-protocol` | `outputs/`, `manuscripts/` | Propose-first, then apply with approval |
| `pdf-processing` | `master_supporting_docs/` | Safe large PDF handling |

### Templates (`templates/`)

| Template | What it does |
|----------|-------------|
| `reference.docx` | Pandoc reference document for docx export |
| `journal-requirements.yml` | Annotated schema for journal YAML files |
| `formatting-report.md` | Report template for formatting outputs |
| `session-log.md` | Structured session logging format |
| `quality-report.md` | Merge-time quality report format |
| `requirements-spec.md` | MUST/SHOULD/MAY requirements framework |

</details>

---

## File layout

```
my-submission-formatting-agent/
├── manuscripts/          # Drop input manuscripts here (gitignored)
├── guidelines/           # Journal requirements YAML (one per journal)
├── outputs/              # Formatted outputs (gitignored)
│   └── [journal-name]/
│       ├── working.md                  # Normalised markdown (from ingest)
│       ├── manuscript_formatted.md     # Formatted output
│       ├── manuscript_formatted.docx   # Formatted Word document
│       ├── compliance_checklist.md     # PASS/WARN/FAIL per requirement
│       └── formatting_report.md        # Full change summary
├── scripts/
│   ├── ingest.py          # Manuscript → markdown (pandoc wrapper)
│   ├── export_docx.py     # Markdown → docx (pandoc wrapper)
│   └── quality_score.py   # Compliance scoring (--rubric manuscript)
├── templates/             # Reference docs and report templates
└── .claude/               # Rules, skills, agents, hooks
```

---

## Prerequisites

| Tool | Required for | Install |
|------|-------------|---------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) | Everything | `npm install -g @anthropic-ai/claude-code` |
| [pandoc](https://pandoc.org) | Ingest + export | [pandoc.org/installing.html](https://pandoc.org/installing.html) |
| Python 3.8+ | Quality scoring | [python.org](https://www.python.org/) |
| pyyaml | Guidelines-aware scoring | `pip install pyyaml` |

---

## Contributing

Issues and pull requests welcome. If you adapt this for a specific journal or discipline, consider sharing your `guidelines/*.yml` files back.

## License

MIT License. Use freely for research or any academic purpose.
