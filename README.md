# Manuscript Submission Formatting Agent

A Claude Code workflow for reformatting research manuscripts to meet journal author guidelines — without altering scientific content.

**Last Updated:** 2026-02-24

You provide a manuscript (.docx, .tex, or .pdf) and a journal's author guidelines URL. Claude parses the requirements, restructures the manuscript to comply, auto-drafts any missing required sections (marked as drafts for author review), and delivers a formatted `.docx` + `.md` with a full formatting report.

> **Privacy:** `manuscripts/` and `outputs/` are gitignored — your manuscripts and formatted files are never pushed to GitHub. They live only on your local machine.

---

## Quick Start

### 1. Clone & Open

```bash
git clone https://github.com/maxwell2732/my-submission-formatting-agent.git
cd my-submission-formatting-agent
claude
```

### 2. Set Up a Journal (one-time per journal)

```
/parse-guidelines ajare https://onlinelibrary.wiley.com/page/journal/14678489/homepage/forauthors.html
```

This fetches the author guidelines and saves structured requirements to `guidelines/ajare.yml`.

> **Tip:** If the journal's website blocks automated access (403), just paste the guidelines text when prompted — Claude will extract requirements from the pasted content instead.

### 3. Format a Manuscript

Drop your manuscript into `manuscripts/`, then:

```
/format-manuscript manuscripts/paper.docx ajare
```

Claude will ingest the manuscript, analyze its structure, reformat it to comply with the journal's requirements, and deliver:

- `outputs/ajare/manuscript_formatted.docx` — ready for submission
- `outputs/ajare/manuscript_formatted.md` — markdown version for editing
- `outputs/ajare/compliance_checklist.md` — PASS/WARN/FAIL for every requirement
- `outputs/ajare/formatting_report.md` — full summary of every change made

---

## What It Does

### Formatting pipeline (`/format-manuscript`)

1. **Ingest** — converts .docx/.tex/.pdf to normalized markdown via pandoc
2. **Analyze** — identifies all sections, detects IMRaD structure, compares against journal requirements
3. **Reorder** — moves sections to match the journal's required order
4. **Rename headings** — applies the journal's heading naming and case style
5. **Restructure abstract** — converts unstructured abstracts to the journal's required structured format
6. **Auto-draft missing sections** — synthesizes content from the manuscript for required sections that are absent (always marked `<!-- DRAFT: requires author review -->`)
7. **Export** — produces `.docx` using a reference template and `.md` for version control
8. **Compliance check** — PASS/WARN/FAIL checklist for every journal requirement
9. **Quality score** — 0–100 compliance score
10. **Proofread** — grammar, typos, draft marker integrity
11. **Report** — `formatting_report.md` with before/after summary and required author actions

### What it never does

- Alter scientific content (numbers, results, citations, conclusions)
- Silently add content — all auto-drafted sections are visibly marked as drafts
- Cut content to meet word limits — those are flagged as warnings for the author

---

## Skills

| Command | What It Does |
|---------|-------------|
| `/parse-guidelines [name] [URL]` | Extract journal requirements → `guidelines/[name].yml` |
| `/format-manuscript [file] [journal]` | Full formatting pipeline |
| `/validate-compliance [file] [journal]` | Standalone compliance check on any formatted file |
| `/generate-report [journal]` | Generate formatting report with before/after diff |
| `/proofread [file]` | Grammar, typos, draft marker check |
| `/review-paper [file]` | Substantive manuscript review (structure, methods, referee objections) |
| `/validate-bib` | Cross-reference citations |
| `/commit [msg]` | Stage, commit, push |

---

## What's Included

<details>
<summary><strong>7 agents, 11 skills, 10 rules, 4 hooks</strong> (click to expand)</summary>

### Agents (`.claude/agents/`)

| Agent | What It Does |
|-------|-------------|
| `manuscript-analyzer` | Section inventory, IMRaD detection, gap analysis vs. journal requirements |
| `guidelines-extractor` | URL or pasted text → structured `guidelines/[journal].yml` |
| `section-drafter` | Synthesizes missing required sections from existing manuscript content (always marks DRAFT) |
| `compliance-checker` | PASS/WARN/FAIL checklist for every journal requirement |
| `proofreader` | Grammar, typos, draft marker integrity, formatting artifacts |
| `verifier` | Checks output files exist, are valid, and quality score passes |
| `domain-reviewer` | **Template** — customize for your field's substance review |

### Skills (`.claude/skills/`)

| Skill | What It Does |
|-------|-------------|
| `/parse-guidelines` | Extract requirements from journal guidelines URL or pasted text |
| `/format-manuscript` | Full 11-step formatting pipeline |
| `/validate-compliance` | Standalone compliance check |
| `/generate-report` | Formatting report with before/after diff |
| `/proofread` | Launch proofreader on a manuscript file |
| `/review-paper` | Full manuscript review (argument, methods, referee objections) |
| `/validate-bib` | Cross-reference citations against bibliography |
| `/devils-advocate` | Challenge formatting decisions |
| `/commit` | Stage, commit, push |
| `/lit-review` | Literature search and synthesis |
| `/research-ideation` | Research questions and empirical strategies |

### Rules (`.claude/rules/`)

**Always-on:**

| Rule | What It Enforces |
|------|-----------------|
| `plan-first-workflow` | Plan mode for non-trivial tasks + context preservation |
| `orchestrator-protocol` | Contractor mode: implement → verify → review → fix → score |
| `session-logging` | Post-plan, incremental, and end-of-session logs |
| `meta-governance` | What belongs in the repo vs. gitignored |

**Path-scoped** (load only when working on matching files):

| Rule | Triggers On | What It Enforces |
|------|------------|-----------------|
| `manuscript-handling` | `manuscripts/`, `outputs/` | Ingest pipeline, content integrity, draft markers |
| `journal-compliance` | `guidelines/`, `outputs/` | Section order, abstract structure, heading style |
| `output-generation` | `outputs/` | pandoc export, formatting report requirements |
| `quality-gates` | `outputs/` | 80/90/95 scoring thresholds, manuscript rubric |
| `proofreading-protocol` | `outputs/`, `manuscripts/` | Propose-first, then apply with approval |
| `pdf-processing` | `master_supporting_docs/` | Safe large PDF handling |

### Templates (`templates/`)

| Template | What It Does |
|----------|-------------|
| `journal-requirements.yml` | Annotated schema for journal YAML files (copy to `guidelines/`) |
| `formatting-report.md` | Report template for formatting outputs |
| `reference.docx` | Pandoc reference document for docx export |
| `session-log.md` | Structured session logging format |
| `quality-report.md` | Merge-time quality report format |
| `requirements-spec.md` | MUST/SHOULD/MAY requirements framework |
| `constitutional-governance.md` | Non-negotiable principles vs. preferences template |
| `skill-template.md` | Skill creation template |

</details>

---

## Prerequisites

| Tool | Required For | Install |
|------|-------------|---------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) | Everything | `npm install -g @anthropic-ai/claude-code` |
| [pandoc](https://pandoc.org) | Ingest + export | [pandoc.org/installing.html](https://pandoc.org/installing.html) |
| [gh CLI](https://cli.github.com/) | PR workflow | `brew install gh` / [cli.github.com](https://cli.github.com/) |
| Python 3.8+ | Quality scoring | [python.org](https://www.python.org/) |
| pyyaml (optional) | Guidelines-aware scoring | `pip install pyyaml` |

---

## File Layout

```
my-submission-formatting-agent/
├── manuscripts/          # Drop input manuscripts here (read-only)
├── guidelines/           # Journal requirements YAML (one file per journal)
├── outputs/              # Formatted outputs
│   └── [journal-name]/
│       ├── working.md                  # Normalized markdown (from ingest)
│       ├── manuscript_formatted.md     # Formatted output
│       ├── manuscript_formatted.docx   # Formatted Word document
│       ├── compliance_checklist.md     # PASS/WARN/FAIL per requirement
│       └── formatting_report.md        # Full change summary
├── scripts/
│   ├── ingest.py          # Manuscript → markdown (pandoc wrapper)
│   ├── export_docx.py     # Markdown → docx (pandoc wrapper)
│   └── quality_score.py   # Compliance scoring (--rubric manuscript)
├── templates/
│   ├── reference.docx              # Pandoc docx reference template
│   └── journal-requirements.yml   # Schema template for new journals
└── .claude/               # Rules, skills, agents, hooks
```

---

## License

MIT License. Use freely for research or any academic purpose.
