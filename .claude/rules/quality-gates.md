---
paths:
  - "outputs/**"
  - "guidelines/**"
---

# Quality Gates & Scoring Rubrics

## Thresholds

- **80/100 = Commit** -- good enough to save
- **90/100 = PR** -- ready for delivery to author
- **95/100 = Excellence** -- aspirational

## Manuscript Compliance Rubric (.md output)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Missing required section (journal mandates it) | -15 per section |
| Critical | Sections out of journal-required order | -20 |
| Critical | Abstract missing required structured sections | -20 |
| Critical | Unclosed `<!-- DRAFT -->` marker | -10 per instance |
| Major | Word count exceeds limit (>10% over) | -10 |
| Major | Heading style non-compliant (wrong case) | -5 per heading level |
| Major | Special requirement missing (e.g., data availability statement) | -5 per item |
| Major | Citation format inconsistency | -5 |
| Minor | Minor heading case inconsistency | -2 |
| Minor | Trailing whitespace / formatting artifacts | -1 per instance |

## Scoring Interpretation

- **Score 95-100:** Excellence — all requirements met, no warnings
- **Score 90-94:** PR-ready — minor issues only, safe to deliver
- **Score 80-89:** Commit — some warnings, author should review before submission
- **Score < 80:** Blocked — critical compliance issues must be resolved

## Enforcement

- **Score < 80:** Block commit. List blocking issues.
- **Score < 90:** Allow commit, warn. List recommendations.
- User can override with justification (e.g., "author will fix word count manually").

## Quality Reports

Generated **only at merge time**. Use `templates/quality-report.md` for format.
Save to `quality_reports/merges/YYYY-MM-DD_[branch-name].md`.

## Exploration Threshold

Work in `explorations/` uses a relaxed threshold: 60/100.
See `.claude/rules/exploration-fast-track.md`.
