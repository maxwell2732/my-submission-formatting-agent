---
paths:
  - "outputs/**/*.md"
  - "manuscripts/**"
  - "quality_reports/**"
---

# Proofreading Agent Protocol (MANDATORY)

**Every formatted manuscript MUST be reviewed before delivery to the author.**

**CRITICAL RULE: The agent must NEVER apply changes directly. It proposes all changes for review first.**

## What the Agent Checks

1. **Grammar** -- subject-verb agreement, missing articles, wrong prepositions, tense consistency
2. **Typos** -- misspellings, leftover placeholder text (`[PLACEHOLDER`), duplicated words
3. **Draft marker integrity** -- every `<!-- DRAFT -->` has a matching `<!-- END DRAFT -->`
4. **Consistency** -- citation style, terminology, abbreviations, units
5. **Formatting artifacts** -- leftover LaTeX commands, stray markdown syntax, double spaces
6. **Academic quality** -- informal language, incomplete sentences, awkward phrasing

## Three-Phase Workflow

### Phase 1: Review & Propose (NO EDITS)

The proofreader agent:
1. Reads the entire file
2. Produces a **report** with every proposed change:
   - Location (line number or section heading)
   - Current text
   - Proposed fix
   - Category (grammar / typo / draft-marker / consistency / artifact / academic style)
3. Saves report to `quality_reports/[FILENAME]_proofread.md`
4. **Does NOT modify any source files**

### Phase 2: Review & Approve

The user reviews the proposed changes:
- Accepts all, accepts selectively, or requests modifications
- **Only after explicit approval** does the agent proceed

### Phase 3: Apply Fixes

Apply only approved changes:
- Use Edit tool; use `replace_all: true` for issues with multiple instances
- Verify each edit succeeded
- Report completion summary
