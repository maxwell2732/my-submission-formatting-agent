#!/usr/bin/env python3
"""
Quality Scoring System for Academic Manuscripts and Course Materials

Calculates objective quality scores (0-100) based on defined rubrics.
Enforces quality gates: 80 (commit), 90 (PR), 95 (excellence).

Usage:
    # Manuscript compliance scoring
    python scripts/quality_score.py outputs/journal/manuscript_formatted.md --rubric manuscript
    python scripts/quality_score.py outputs/journal/manuscript_formatted.md --rubric manuscript --journal lancet-eb

    # Legacy course material scoring
    python scripts/quality_score.py Quarto/Lecture6_Topic.qmd
    python scripts/quality_score.py Slides/Lecture01_Topic.tex
    python scripts/quality_score.py scripts/R/Lecture06_simulations.R
"""

import sys
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re
import json

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# ==============================================================================
# SCORING RUBRIC (from .claude/rules/quality-gates.md)
# ==============================================================================

QUARTO_RUBRIC = {
    'critical': {
        'compilation_failure': {'points': 100, 'auto_fail': True},
        'equation_overflow': {'points': 20},
        'broken_citation': {'points': 15},
        'typo_in_equation': {'points': 10},
        'missing_plotly_chart': {'points': 10},
    },
    'major': {
        'text_overflow': {'points': 5},
        'tikz_label_overlap': {'points': 5},
        'notation_inconsistency': {'points': 3},
        'missing_box_separation': {'points': 2},
        'color_contrast_low': {'points': 3},
    },
    'minor': {
        'font_size_reduction': {'points': 1},
        'missing_forward_ref': {'points': 1},
        'missing_framing_sentence': {'points': 1},
    }
}

R_SCRIPT_RUBRIC = {
    'critical': {
        'syntax_error': {'points': 100, 'auto_fail': True},
        'hardcoded_path': {'points': 20},
        'missing_library': {'points': 10},
    },
    'major': {
        'missing_set_seed': {'points': 10},
        'missing_figure': {'points': 5},
        'missing_rds': {'points': 5},
    },
    'minor': {
        'style_violation': {'points': 1},
        'missing_roxygen': {'points': 1},
    }
}

BEAMER_RUBRIC = {
    'critical': {
        'compilation_failure': {'points': 100, 'auto_fail': True},
        'undefined_citation': {'points': 15},
        'overfull_hbox': {'points': 10},
    },
    'major': {
        'text_overflow': {'points': 5},
        'notation_inconsistency': {'points': 3},
    },
    'minor': {
        'font_size_reduction': {'points': 1},
    }
}

MANUSCRIPT_RUBRIC = {
    'critical': {
        'sections_out_of_order': {'points': 20},
        'abstract_missing_required_sections': {'points': 20},
        'missing_required_section': {'points': 15},    # per section
        'unclosed_draft_marker': {'points': 10},       # per instance
    },
    'major': {
        'word_count_over_limit': {'points': 10},
        'heading_style_noncompliant': {'points': 5},
        'special_requirement_missing': {'points': 5},  # per item
        'citation_format_inconsistency': {'points': 5},
    },
    'minor': {
        'heading_case_inconsistency': {'points': 2},
        'formatting_artifact': {'points': 1},
    }
}

THRESHOLDS = {
    'commit': 80,
    'pr': 90,
    'excellence': 95
}

# ==============================================================================
# ISSUE DETECTION (Lightweight checks - full agents run separately)
# ==============================================================================

class IssueDetector:
    """Detect common issues for quality scoring."""

    @staticmethod
    def check_quarto_compilation(filepath: Path) -> Tuple[bool, str]:
        """Check if Quarto file compiles successfully."""
        try:
            result = subprocess.run(
                ['quarto', 'render', str(filepath), '--to', 'html'],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=filepath.parent
            )
            if result.returncode != 0:
                return False, result.stderr
            return True, ""
        except subprocess.TimeoutExpired:
            return False, "Compilation timeout (>2min)"
        except FileNotFoundError:
            return False, "Quarto not installed"

    @staticmethod
    def check_equation_overflow(content: str) -> List[int]:
        """Detect displayed equations with single lines likely to overflow.

        Flags equations only when a SINGLE LINE within a math block exceeds
        120 characters. Multi-line equations properly broken across lines
        are not flagged even if the total block is long.

        Checks:
        - $$ ... $$ blocks (Quarto/LaTeX)
        - \\begin{equation} ... \\end{equation} blocks
        - \\begin{align} ... \\end{align} blocks
        - \\begin{gather} ... \\end{gather} blocks
        """
        overflows = []
        lines = content.split('\n')
        in_math = False
        math_start = 0
        math_delim = None  # Track which delimiter opened the block

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Check for $$ delimiter (toggle)
            if '$$' in stripped and math_delim != 'env':
                if not in_math:
                    in_math = True
                    math_start = i
                    math_delim = '$$'
                    # Handle single-line $$ ... $$ (both delimiters on same line)
                    if stripped.count('$$') >= 2:
                        inner = stripped.split('$$')[1]
                        if len(inner.strip()) > 120:
                            overflows.append(i)
                        in_math = False
                        math_delim = None
                    continue
                else:
                    in_math = False
                    math_delim = None
                    continue

            # Check for \begin{equation/align/gather/...}
            env_begin = re.match(
                r'\\begin\{(equation|align|gather|multline|eqnarray)\*?\}', stripped
            )
            if env_begin and not in_math:
                in_math = True
                math_start = i
                math_delim = 'env'
                continue

            # Check for \end{equation/align/gather/...}
            if re.match(r'\\end\{(equation|align|gather|multline|eqnarray)\*?\}', stripped):
                in_math = False
                math_delim = None
                continue

            # Inside a math block: check individual line length
            if in_math:
                # Strip LaTeX comments before measuring
                code_part = line.split('%')[0] if '%' in line else line
                if len(code_part.strip()) > 120:
                    overflows.append(i)

        return overflows

    @staticmethod
    def check_broken_citations(content: str, bib_file: Path) -> List[str]:
        """Check for LaTeX citation keys not in bibliography.

        Matches \\cite{}, \\citep{}, \\citet{}, \\citeauthor{}, \\citeyear{}, etc.
        """
        cite_pattern = r'\\cite[a-z]*\{([^}]+)\}'
        cited_keys = set()
        for match in re.finditer(cite_pattern, content):
            keys = match.group(1).split(',')
            cited_keys.update(k.strip() for k in keys)

        if not bib_file.exists():
            return list(cited_keys)

        bib_content = bib_file.read_text(encoding='utf-8')
        bib_keys = set(re.findall(r'@\w+\{([^,]+),', bib_content))

        broken = cited_keys - bib_keys
        return list(broken)

    @staticmethod
    def check_plotly_widgets(html_file: Path, expected: int = None) -> Tuple[int, bool]:
        """Check if plotly charts rendered in HTML."""
        if not html_file.exists():
            return 0, False

        html_content = html_file.read_text(encoding='utf-8')
        actual_count = html_content.count('htmlwidget')

        if expected is None:
            return actual_count, True

        return actual_count, (actual_count >= expected)

    @staticmethod
    def check_r_syntax(filepath: Path) -> Tuple[bool, str]:
        """Check R script for syntax errors."""
        try:
            result = subprocess.run(
                ['Rscript', '-e', f'parse("{filepath}")'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                return False, result.stderr
            return True, ""
        except subprocess.TimeoutExpired:
            return False, "Syntax check timeout"
        except FileNotFoundError:
            return False, "Rscript not installed"

    @staticmethod
    def check_hardcoded_paths(content: str) -> List[int]:
        """Detect absolute paths in R scripts."""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            if re.search(r'["\'][/\\]|["\'][A-Za-z]:[/\\]', line):
                if not re.search(r'http:|https:|file://|/tmp/', line):
                    issues.append(i)

        return issues

    @staticmethod
    def check_latex_syntax(content: str) -> List[Dict]:
        """Check for common LaTeX syntax issues without compiling.

        Looks for:
        - Unmatched braces
        - Unclosed environments
        - Common typos in commands
        """
        issues = []
        lines = content.split('\n')

        # Track open environments
        env_stack = []
        for i, line in enumerate(lines, 1):
            # Skip comments
            stripped = line.split('%')[0] if '%' in line else line

            # Check for \begin{env}
            for match in re.finditer(r'\\begin\{(\w+)\}', stripped):
                env_stack.append((match.group(1), i))

            # Check for \end{env}
            for match in re.finditer(r'\\end\{(\w+)\}', stripped):
                env_name = match.group(1)
                if env_stack and env_stack[-1][0] == env_name:
                    env_stack.pop()
                elif env_stack:
                    issues.append({
                        'line': i,
                        'description': f'Mismatched environment: \\end{{{env_name}}} '
                                       f'but expected \\end{{{env_stack[-1][0]}}} '
                                       f'(opened at line {env_stack[-1][1]})',
                    })
                else:
                    issues.append({
                        'line': i,
                        'description': f'\\end{{{env_name}}} without matching \\begin',
                    })

        # Report unclosed environments
        for env_name, line_num in env_stack:
            issues.append({
                'line': line_num,
                'description': f'Unclosed environment: \\begin{{{env_name}}} never closed',
            })

        return issues

    @staticmethod
    def check_overfull_hbox_risk(content: str) -> List[int]:
        """Detect lines in LaTeX source likely to cause overfull hbox.

        Checks for very long lines inside text and math environments
        that are likely to overflow the slide width.
        """
        issues = []
        lines = content.split('\n')
        in_frame = False

        for i, line in enumerate(lines, 1):
            stripped = line.split('%')[0] if '%' in line else line

            # Track frame environments for context
            if r'\begin{frame}' in stripped:
                in_frame = True
            elif r'\end{frame}' in stripped:
                in_frame = False

            # Flag very long content lines inside frames
            # Strip leading whitespace and LaTeX commands for length check
            if in_frame and len(stripped.strip()) > 120:
                # Skip lines that are just comments or common long commands
                if stripped.strip().startswith('%'):
                    continue
                # Skip includegraphics, input, and similar path-based commands
                if re.match(r'\s*\\(includegraphics|input|bibliography|usepackage)', stripped):
                    continue
                issues.append(i)

        return issues

    @staticmethod
    def check_quarto_citations(content: str, bib_file: Path) -> List[str]:
        """Check Quarto-style citation keys against bibliography.

        Supports patterns: @key, [@key], [@key1; @key2]
        """
        cited_keys = set()

        # Pattern 1: [@key] or [@key1; @key2; ...]
        bracket_pattern = r'\[([^\]]*@[^\]]+)\]'
        for match in re.finditer(bracket_pattern, content):
            inner = match.group(1)
            # Extract individual @key references from within brackets
            for key_match in re.finditer(r'@([\w:.#$%&\-+?<>~/]+)', inner):
                cited_keys.add(key_match.group(1))

        # Pattern 2: standalone @key (not inside brackets, not email addresses)
        # Match @key that is preceded by start-of-line or whitespace or punctuation
        # but NOT preceded by characters that indicate an email address
        standalone_pattern = r'(?<![.\w])@([\w:.#$%&\-+?<>~/]+)'
        for match in re.finditer(standalone_pattern, content):
            key = match.group(1)
            # Skip if it looks like a Quarto directive or special syntax
            if key.startswith('{') or key in ('fig', 'tbl', 'sec', 'eq', 'lst'):
                continue
            cited_keys.add(key)

        if not cited_keys:
            return []

        if not bib_file.exists():
            return list(cited_keys)

        bib_content = bib_file.read_text(encoding='utf-8')
        bib_keys = set(re.findall(r'@\w+\{([^,]+),', bib_content))

        broken = cited_keys - bib_keys
        return list(broken)

# ==============================================================================
# MANUSCRIPT COMPLIANCE SCORER
# ==============================================================================

class ManuscriptScorer:
    """Score manuscript compliance against journal requirements."""

    def __init__(self, filepath: Path, journal: Optional[str] = None, verbose: bool = False):
        self.filepath = filepath
        self.journal = journal
        self.verbose = verbose
        self.score = 100
        self.issues = {'critical': [], 'major': [], 'minor': []}
        self.auto_fail = False
        self.guidelines = self._load_guidelines()

    def _load_guidelines(self) -> Optional[Dict]:
        """Load journal guidelines YAML if available."""
        if not self.journal:
            return None
        if not YAML_AVAILABLE:
            return None
        yml_path = Path('guidelines') / f'{self.journal}.yml'
        if not yml_path.exists():
            return None
        try:
            with open(yml_path, encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception:
            return None

    def _count_words(self, content: str) -> int:
        """Count words in markdown, roughly excluding YAML front matter."""
        lines = content.split('\n')
        # Strip YAML front matter
        if lines and lines[0].strip() == '---':
            end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == '---'), None)
            if end:
                lines = lines[end + 1:]
        text = '\n'.join(lines)
        # Remove markdown headings, links, inline code
        text = re.sub(r'#{1,6}\s+', '', text)
        text = re.sub(r'`[^`]+`', '', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
        return len(text.split())

    def _get_headings(self, content: str) -> List[Dict]:
        """Extract all markdown headings with level, text, and line number."""
        headings = []
        for i, line in enumerate(content.split('\n'), 1):
            m = re.match(r'^(#{1,6})\s+(.+)', line)
            if m:
                headings.append({
                    'level': len(m.group(1)),
                    'text': m.group(2).strip(),
                    'line': i,
                })
        return headings

    def _check_draft_markers(self, content: str) -> Tuple[int, int]:
        """Count open and close draft markers. Returns (open_count, close_count)."""
        open_count = len(re.findall(r'<!--\s*DRAFT', content, re.IGNORECASE))
        close_count = len(re.findall(r'<!--\s*END DRAFT', content, re.IGNORECASE))
        return open_count, close_count

    def _check_section_order(self, headings: List[Dict]) -> bool:
        """Check if H1 sections are in the order required by guidelines."""
        if not self.guidelines:
            return True
        required = self.guidelines.get('sections_required', [])
        if not required:
            return True
        # Get manuscript H1 headings
        h1_texts = [h['text'].lower() for h in headings if h['level'] == 1]
        required_names = [r['name'].lower() for r in required if r.get('required', True)]
        # Check that required sections appear in the right relative order
        last_pos = -1
        for req in required_names:
            matches = [i for i, t in enumerate(h1_texts) if req in t or t in req]
            if matches:
                pos = matches[0]
                if pos < last_pos:
                    return False
                last_pos = pos
        return True

    def _find_missing_sections(self, headings: List[Dict]) -> List[str]:
        """Return list of required sections missing from the manuscript."""
        if not self.guidelines:
            return []
        required = self.guidelines.get('sections_required', [])
        all_heading_texts = [h['text'].lower() for h in headings]
        missing = []
        for r in required:
            if not r.get('required', True):
                continue
            # Skip level-0 sections (title, affiliations, keywords) — not headings
            if r.get('level', 1) == 0:
                continue
            name = r['name'].lower()
            # Check if the section notes say "do NOT include" heading (e.g., PNAS Introduction)
            notes = (r.get('notes') or '').lower()
            if 'do not include' in notes and 'heading' in notes:
                continue
            found = any(name in t or t in name for t in all_heading_texts)
            if not found:
                missing.append(r['name'])
        return missing

    def _check_heading_style(self, headings: List[Dict]) -> List[str]:
        """Return list of non-compliant headings per guidelines style."""
        if not self.guidelines:
            return []
        style_raw = self.guidelines.get('headings', {}).get('style', '') or ''
        style = style_raw.lower()
        if not style:
            return []
        noncompliant = []
        for h in headings:
            text = h['text']
            if style == 'sentence case':
                # First word should be capitalized, rest (except proper nouns) lowercase
                words = text.split()
                if len(words) > 1:
                    # Check if any word after position 0 is incorrectly capitalized
                    # (heuristic: flag if >1 subsequent word is Title-cased and not a known proper noun)
                    titled_after_first = sum(
                        1 for w in words[1:]
                        if w and w[0].isupper() and w.lower() not in ('a', 'an', 'the', 'and', 'or')
                    )
                    if titled_after_first >= 2:
                        noncompliant.append(text)
            elif style == 'title case':
                minor_words = {'a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor',
                               'on', 'at', 'to', 'by', 'in', 'of', 'up', 'as'}
                words = text.split()
                for j, w in enumerate(words):
                    clean = re.sub(r'[^a-zA-Z]', '', w)
                    if j > 0 and clean.lower() in minor_words:
                        continue
                    if clean and not clean[0].isupper():
                        noncompliant.append(text)
                        break
        return noncompliant

    def score_manuscript(self) -> Dict:
        """Score manuscript compliance."""
        content = self.filepath.read_text(encoding='utf-8')
        headings = self._get_headings(content)

        # 1. Draft markers
        open_m, close_m = self._check_draft_markers(content)
        unclosed = open_m - close_m
        if unclosed > 0:
            for _ in range(unclosed):
                self.issues['critical'].append({
                    'type': 'unclosed_draft_marker',
                    'description': 'Unclosed <!-- DRAFT --> marker',
                    'details': 'Every <!-- DRAFT --> must have a matching <!-- END DRAFT -->',
                    'points': MANUSCRIPT_RUBRIC['critical']['unclosed_draft_marker']['points']
                })
                self.score -= MANUSCRIPT_RUBRIC['critical']['unclosed_draft_marker']['points']
        elif open_m > 0:
            # Paired draft markers: warn (expected during iteration)
            self.issues['minor'].append({
                'type': 'draft_markers_present',
                'description': f'{open_m} DRAFT section(s) require author review',
                'details': 'Search for <!-- DRAFT --> in the output file',
                'points': 0
            })

        # 2. Missing required sections (only if guidelines loaded)
        missing = self._find_missing_sections(headings)
        for section in missing:
            pts = MANUSCRIPT_RUBRIC['critical']['missing_required_section']['points']
            self.issues['critical'].append({
                'type': 'missing_required_section',
                'description': f'Missing required section: {section}',
                'details': 'Journal requires this section. Add or auto-draft it.',
                'points': pts
            })
            self.score -= pts

        # 3. Section order
        if not self._check_section_order(headings):
            pts = MANUSCRIPT_RUBRIC['critical']['sections_out_of_order']['points']
            self.issues['critical'].append({
                'type': 'sections_out_of_order',
                'description': 'Sections not in journal-required order',
                'details': f"Check guidelines/{self.journal}.yml sections_required for correct order",
                'points': pts
            })
            self.score -= pts

        # 4. Heading style
        noncompliant_headings = self._check_heading_style(headings)
        if len(noncompliant_headings) >= 3:
            pts = MANUSCRIPT_RUBRIC['major']['heading_style_noncompliant']['points']
            self.issues['major'].append({
                'type': 'heading_style_noncompliant',
                'description': f'{len(noncompliant_headings)} headings not in required style',
                'details': f"Required: {self.guidelines.get('headings', {}).get('style', 'unknown')}. "
                           f"Examples: {noncompliant_headings[:2]}",
                'points': pts
            })
            self.score -= pts
        elif len(noncompliant_headings) > 0:
            pts = MANUSCRIPT_RUBRIC['minor']['heading_case_inconsistency']['points']
            self.issues['minor'].append({
                'type': 'heading_case_inconsistency',
                'description': f'{len(noncompliant_headings)} headings with minor style issue',
                'details': f"Examples: {noncompliant_headings[:2]}",
                'points': pts * len(noncompliant_headings)
            })
            self.score -= pts * len(noncompliant_headings)

        # 5. Word count (if guidelines specify)
        if self.guidelines:
            total_limit = (self.guidelines.get('word_limit') or {}).get('total')
            if total_limit:
                word_count = self._count_words(content)
                if word_count > total_limit * 1.10:
                    pts = MANUSCRIPT_RUBRIC['major']['word_count_over_limit']['points']
                    over_pct = int((word_count - total_limit) / total_limit * 100)
                    self.issues['major'].append({
                        'type': 'word_count_over_limit',
                        'description': f'Word count {word_count} exceeds limit {total_limit} (+{over_pct}%)',
                        'details': 'Author should trim content before submission',
                        'points': pts
                    })
                    self.score -= pts

        # 6. Formatting artifacts
        artifacts = re.findall(r'\\[a-zA-Z]+\{', content)
        if len(artifacts) > 5:
            pts = MANUSCRIPT_RUBRIC['minor']['formatting_artifact']['points']
            self.issues['minor'].append({
                'type': 'formatting_artifact',
                'description': f'{len(artifacts)} possible LaTeX remnants in output',
                'details': f"Examples: {list(set(artifacts))[:3]}",
                'points': pts
            })
            self.score -= pts

        self.score = max(0, self.score)
        return self._generate_report()

    def _generate_report(self) -> Dict:
        """Generate quality score report."""
        if self.auto_fail:
            status = 'FAIL'
        elif self.score >= THRESHOLDS['excellence']:
            status = 'EXCELLENCE'
        elif self.score >= THRESHOLDS['pr']:
            status = 'PR_READY'
        elif self.score >= THRESHOLDS['commit']:
            status = 'COMMIT_READY'
        else:
            status = 'BLOCKED'

        counts = {k: len(v) for k, v in self.issues.items()}
        counts['total'] = sum(counts.values())

        return {
            'filepath': str(self.filepath),
            'score': self.score,
            'status': status,
            'auto_fail': self.auto_fail,
            'rubric': 'manuscript',
            'journal': self.journal,
            'issues': {**self.issues, 'counts': counts},
            'thresholds': THRESHOLDS,
        }

    def print_report(self, summary_only: bool = False) -> None:
        """Print formatted compliance report."""
        report = self._generate_report()
        print(f"\n# Manuscript Compliance Score: {self.filepath.name}\n")

        status_label = {
            'EXCELLENCE': '[EXCELLENCE]', 'PR_READY': '[PASS]',
            'COMMIT_READY': '[PASS]', 'BLOCKED': '[BLOCKED]', 'FAIL': '[FAIL]'
        }
        print(f"## Overall Score: {report['score']}/100 {status_label.get(report['status'], '')}")
        if self.journal:
            print(f"**Journal:** {self.journal}")
        if not self.guidelines and self.journal:
            print(f"**Note:** guidelines/{self.journal}.yml not found — only generic checks run")
        elif not self.journal:
            print("**Note:** No journal specified — only generic checks run (use --journal [name])")

        if summary_only:
            counts = report['issues']['counts']
            print(f"\n**Total issues:** {counts['total']} "
                  f"({counts['critical']} critical, {counts['major']} major, {counts['minor']} minor)")
            return

        for severity in ('critical', 'major'):
            issues = report['issues'][severity]
            label = 'MUST FIX' if severity == 'critical' else 'SHOULD FIX'
            print(f"\n## {severity.title()} Issues ({label}): {len(issues)}")
            if not issues:
                print("None")
            for i, issue in enumerate(issues, 1):
                pts = f" (-{issue['points']} points)" if issue.get('points') else ""
                print(f"{i}. **{issue['description']}**{pts}")
                print(f"   - {issue['details']}")

        if self.verbose:
            issues = report['issues']['minor']
            print(f"\n## Minor Issues: {len(issues)}")
            for i, issue in enumerate(issues, 1):
                print(f"{i}. {issue['description']}")

        if report['status'] == 'BLOCKED':
            print(f"\n## Action Required")
            print(f"Score {report['score']}/100 is below commit threshold ({THRESHOLDS['commit']}).")
            print("Fix critical issues above and re-run.")
        elif report['status'] == 'COMMIT_READY':
            gap = THRESHOLDS['pr'] - report['score']
            print(f"\n**Status:** Ready to commit. Need +{gap} points for PR/delivery threshold.")


# ==============================================================================
# QUALITY SCORER
# ==============================================================================

class QualityScorer:
    """Calculate quality scores for course materials."""

    def __init__(self, filepath: Path, verbose: bool = False):
        self.filepath = filepath
        self.verbose = verbose
        self.score = 100
        self.issues = {
            'critical': [],
            'major': [],
            'minor': []
        }
        self.auto_fail = False

    def score_quarto(self) -> Dict:
        """Score Quarto lecture slides."""
        content = self.filepath.read_text(encoding='utf-8')

        # Check compilation
        compiles, error = IssueDetector.check_quarto_compilation(self.filepath)
        if not compiles:
            self.auto_fail = True
            self.issues['critical'].append({
                'type': 'compilation_failure',
                'description': 'Quarto compilation failed',
                'details': error[:200],
                'points': 100
            })
            self.score = 0
            return self._generate_report()

        # Check equation overflow (heuristic)
        equation_overflows = IssueDetector.check_equation_overflow(content)
        for line in equation_overflows:
            self.issues['critical'].append({
                'type': 'equation_overflow',
                'description': f'Potential equation overflow at line {line}',
                'details': 'Single equation line >120 chars may overflow slide',
                'points': 20
            })
            self.score -= 20

        # Check broken citations (LaTeX-style \cite patterns)
        bib_file = self.filepath.parent.parent / 'Bibliography_base.bib'
        broken_citations = IssueDetector.check_broken_citations(content, bib_file)

        # Also check Quarto-style @key citations
        quarto_broken = IssueDetector.check_quarto_citations(content, bib_file)
        # Merge both sets, avoiding duplicates
        all_broken = set(broken_citations) | set(quarto_broken)
        for key in all_broken:
            self.issues['critical'].append({
                'type': 'broken_citation',
                'description': f'Citation key not in bibliography: {key}',
                'details': 'Add to Bibliography_base.bib or fix key',
                'points': 15
            })
            self.score -= 15

        # Check plotly widgets (if HTML exists)
        html_file = self.filepath.parent.parent / 'docs' / 'slides' / self.filepath.with_suffix('.html').name
        if html_file.exists():
            widget_count, _ = IssueDetector.check_plotly_widgets(html_file)
            expected_plotly = content.count('plotly::plot_ly')
            if expected_plotly > 0 and widget_count < expected_plotly:
                missing = expected_plotly - widget_count
                self.issues['critical'].append({
                    'type': 'missing_plotly_chart',
                    'description': f'{missing} plotly chart(s) failed to render',
                    'details': f'Expected {expected_plotly}, found {widget_count}',
                    'points': 10 * missing
                })
                self.score -= 10 * missing

        self.score = max(0, self.score)
        return self._generate_report()

    def score_r_script(self) -> Dict:
        """Score R script quality."""
        content = self.filepath.read_text(encoding='utf-8')

        # Check syntax
        is_valid, error = IssueDetector.check_r_syntax(self.filepath)
        if not is_valid:
            self.auto_fail = True
            self.issues['critical'].append({
                'type': 'syntax_error',
                'description': 'R syntax error',
                'details': error[:200],
                'points': 100
            })
            self.score = 0
            return self._generate_report()

        # Check hardcoded paths
        path_issues = IssueDetector.check_hardcoded_paths(content)
        for line in path_issues:
            self.issues['critical'].append({
                'type': 'hardcoded_path',
                'description': f'Hardcoded absolute path at line {line}',
                'details': 'Use relative paths or here::here()',
                'points': 20
            })
            self.score -= 20

        # Check for set.seed() if randomness detected
        has_random = any(fn in content for fn in ['rnorm', 'runif', 'sample', 'rbinom', 'rnbinom'])
        has_seed = 'set.seed' in content
        if has_random and not has_seed:
            self.issues['major'].append({
                'type': 'missing_set_seed',
                'description': 'Missing set.seed() for reproducibility',
                'details': 'Add set.seed(YYYYMMDD) after library() calls',
                'points': 10
            })
            self.score -= 10

        self.score = max(0, self.score)
        return self._generate_report()

    def score_beamer(self) -> Dict:
        """Score Beamer/LaTeX lecture slides."""
        content = self.filepath.read_text(encoding='utf-8')

        # Check for LaTeX syntax issues (without compiling)
        syntax_issues = IssueDetector.check_latex_syntax(content)
        if syntax_issues:
            # Mismatched environments are treated as compilation risk
            for issue in syntax_issues:
                self.issues['critical'].append({
                    'type': 'compilation_failure',
                    'description': f'LaTeX syntax issue at line {issue["line"]}',
                    'details': issue['description'],
                    'points': 100
                })
            self.auto_fail = True
            self.score = 0
            return self._generate_report()

        # Check for undefined/broken citations (\cite, \citep, \citet patterns)
        bib_file = self.filepath.parent.parent / 'Bibliography_base.bib'
        if not bib_file.exists():
            # Also check same directory
            bib_file = self.filepath.parent / 'Bibliography_base.bib'
        broken_citations = IssueDetector.check_broken_citations(content, bib_file)
        for key in broken_citations:
            self.issues['critical'].append({
                'type': 'undefined_citation',
                'description': f'Citation key not in bibliography: {key}',
                'details': 'Add to Bibliography_base.bib or fix key',
                'points': 15
            })
            self.score -= 15

        # Check for lines likely to cause overfull hbox
        overfull_lines = IssueDetector.check_overfull_hbox_risk(content)
        for line in overfull_lines:
            self.issues['critical'].append({
                'type': 'overfull_hbox',
                'description': f'Potential overfull hbox at line {line}',
                'details': 'Line >120 chars inside frame may overflow slide width',
                'points': 10
            })
            self.score -= 10

        # Check equation overflow (same heuristic as Quarto)
        equation_overflows = IssueDetector.check_equation_overflow(content)
        for line_num in equation_overflows:
            self.issues['critical'].append({
                'type': 'overfull_hbox',
                'description': f'Potential equation overflow at line {line_num}',
                'details': 'Single equation line >120 chars likely to overflow',
                'points': 10
            })
            self.score -= 10

        self.score = max(0, self.score)
        return self._generate_report()

    def _generate_report(self) -> Dict:
        """Generate quality score report."""
        if self.auto_fail:
            status = 'FAIL'
            threshold = 'None (auto-fail)'
        elif self.score >= THRESHOLDS['excellence']:
            status = 'EXCELLENCE'
            threshold = 'excellence'
        elif self.score >= THRESHOLDS['pr']:
            status = 'PR_READY'
            threshold = 'pr'
        elif self.score >= THRESHOLDS['commit']:
            status = 'COMMIT_READY'
            threshold = 'commit'
        else:
            status = 'BLOCKED'
            threshold = 'None (below commit)'

        critical_count = len(self.issues['critical'])
        major_count = len(self.issues['major'])
        minor_count = len(self.issues['minor'])
        total_count = critical_count + major_count + minor_count

        return {
            'filepath': str(self.filepath),
            'score': self.score,
            'status': status,
            'threshold': threshold,
            'auto_fail': self.auto_fail,
            'issues': {
                'critical': self.issues['critical'],
                'major': self.issues['major'],
                'minor': self.issues['minor'],
                'counts': {
                    'critical': critical_count,
                    'major': major_count,
                    'minor': minor_count,
                    'total': total_count
                }
            },
            'thresholds': THRESHOLDS
        }

    def print_report(self, summary_only: bool = False) -> None:
        """Print formatted quality report."""
        report = self._generate_report()

        print(f"\n# Quality Score: {self.filepath.name}\n")

        status_emoji = {
            'EXCELLENCE': '[EXCELLENCE]',
            'PR_READY': '[PASS]',
            'COMMIT_READY': '[PASS]',
            'BLOCKED': '[BLOCKED]',
            'FAIL': '[FAIL]'
        }

        print(f"## Overall Score: {report['score']}/100 {status_emoji.get(report['status'], '')}")

        if report['status'] == 'BLOCKED':
            print(f"\n**Status:** BLOCKED - Cannot commit (score < {THRESHOLDS['commit']})")
        elif report['status'] == 'COMMIT_READY':
            print(f"\n**Status:** Ready for commit (score >= {THRESHOLDS['commit']})")
            gap_to_pr = THRESHOLDS['pr'] - report['score']
            print(f"**Next milestone:** PR threshold ({THRESHOLDS['pr']}+)")
            print(f"**Gap analysis:** Need +{gap_to_pr} points to reach PR quality")
        elif report['status'] == 'PR_READY':
            print(f"\n**Status:** Ready for PR (score >= {THRESHOLDS['pr']})")
            gap_to_excellence = THRESHOLDS['excellence'] - report['score']
            if gap_to_excellence > 0:
                print(f"**Next milestone:** Excellence ({THRESHOLDS['excellence']})")
                print(f"**Gap analysis:** +{gap_to_excellence} points to excellence")
        elif report['status'] == 'EXCELLENCE':
            print(f"\n**Status:** Excellence achieved! (score >= {THRESHOLDS['excellence']})")
        elif report['status'] == 'FAIL':
            print(f"\n**Status:** Auto-fail (compilation/syntax error)")

        if summary_only:
            print(f"\n**Total issues:** {report['issues']['counts']['total']} "
                  f"({report['issues']['counts']['critical']} critical, "
                  f"{report['issues']['counts']['major']} major, "
                  f"{report['issues']['counts']['minor']} minor)")
            return

        # Detailed issues
        print(f"\n## Critical Issues (MUST FIX): {report['issues']['counts']['critical']}")
        if report['issues']['counts']['critical'] == 0:
            print("No critical issues - safe to commit\n")
        else:
            for i, issue in enumerate(report['issues']['critical'], 1):
                print(f"{i}. **{issue['description']}** (-{issue['points']} points)")
                print(f"   - {issue['details']}\n")

        if report['issues']['counts']['major'] > 0:
            print(f"## Major Issues (SHOULD FIX): {report['issues']['counts']['major']}")
            for i, issue in enumerate(report['issues']['major'], 1):
                print(f"{i}. **{issue['description']}** (-{issue['points']} points)")
                print(f"   - {issue['details']}\n")

        if report['issues']['counts']['minor'] > 0 and self.verbose:
            print(f"## Minor Issues (NICE-TO-HAVE): {report['issues']['counts']['minor']}")
            for i, issue in enumerate(report['issues']['minor'], 1):
                print(f"{i}. {issue['description']} (-{issue['points']} points)\n")

        # Recommendations
        if report['status'] == 'BLOCKED':
            print("## Recommended Actions")
            print("1. Fix all critical issues above")
            print(f"2. Re-run quality score (target: >={THRESHOLDS['commit']})")
            print("3. Commit after reaching threshold\n")
        elif report['status'] == 'COMMIT_READY' and report['score'] < THRESHOLDS['pr']:
            print("## Recommended Actions to Reach PR Threshold")
            points_needed = THRESHOLDS['pr'] - report['score']
            print(f"Need +{points_needed} points to reach {THRESHOLDS['pr']}/100")
            if report['issues']['counts']['major'] > 0:
                print("Fix major issues listed above to improve score")
            print(f"\n**Estimated time:** 10-20 minutes\n")

# ==============================================================================
# CLI INTERFACE
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Calculate quality scores for manuscripts and course materials',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Score manuscript compliance (recommended)
  python scripts/quality_score.py outputs/lancet/manuscript_formatted.md --rubric manuscript
  python scripts/quality_score.py outputs/lancet/manuscript_formatted.md --rubric manuscript --journal lancet-eb

  # Legacy: Score Quarto/Beamer/R files
  python scripts/quality_score.py Quarto/Lecture6_Topic.qmd
  python scripts/quality_score.py Slides/Lecture01_Topic.tex
  python scripts/quality_score.py scripts/R/Lecture06_simulations.R

  # Summary only
  python scripts/quality_score.py outputs/lancet/manuscript.md --rubric manuscript --summary

  # JSON output
  python scripts/quality_score.py outputs/lancet/manuscript.md --rubric manuscript --json

Quality Thresholds:
  80/100 = Commit threshold
  90/100 = PR / delivery threshold
  95/100 = Excellence (aspirational)

Exit Codes:
  0 = Score >= 80 (commit allowed)
  1 = Score < 80 (commit blocked)
  2 = Auto-fail (compilation/syntax error)
        """
    )

    parser.add_argument('filepaths', type=Path, nargs='+', help='Path(s) to file(s) to score')
    parser.add_argument('--rubric', choices=['manuscript', 'auto'], default='auto',
                        help='Scoring rubric: "manuscript" for compliance scoring, "auto" to detect from extension')
    parser.add_argument('--journal', type=str, default=None,
                        help='Journal name (loads guidelines/[journal].yml for compliance checks)')
    parser.add_argument('--summary', action='store_true', help='Show summary only')
    parser.add_argument('--verbose', action='store_true', help='Show all issues including minor')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    results = []
    exit_code = 0

    for filepath in args.filepaths:
        if not filepath.exists():
            print(f"Error: File not found: {filepath}")
            exit_code = 1
            continue

        try:
            # Determine rubric
            use_manuscript = (
                args.rubric == 'manuscript' or
                (args.rubric == 'auto' and filepath.suffix == '.md' and
                 str(filepath).startswith('outputs'))
            )

            if use_manuscript:
                scorer = ManuscriptScorer(filepath, journal=args.journal, verbose=args.verbose)
                report = scorer.score_manuscript()
                if not args.json:
                    scorer.print_report(summary_only=args.summary)
            else:
                scorer = QualityScorer(filepath, verbose=args.verbose)
                if filepath.suffix == '.qmd':
                    report = scorer.score_quarto()
                elif filepath.suffix == '.R':
                    report = scorer.score_r_script()
                elif filepath.suffix == '.tex':
                    report = scorer.score_beamer()
                elif filepath.suffix == '.md':
                    # Plain markdown without --rubric manuscript: use manuscript scorer
                    ms = ManuscriptScorer(filepath, journal=args.journal, verbose=args.verbose)
                    report = ms.score_manuscript()
                    if not args.json:
                        ms.print_report(summary_only=args.summary)
                    results.append(report)
                    if report['score'] < THRESHOLDS['commit']:
                        exit_code = max(exit_code, 1)
                    continue
                else:
                    print(f"Error: Unsupported file type: {filepath.suffix}")
                    print("Use --rubric manuscript for .md files")
                    continue

                if not args.json:
                    scorer.print_report(summary_only=args.summary)

            results.append(report)

            if report.get('auto_fail'):
                exit_code = max(exit_code, 2)
            elif report['score'] < THRESHOLDS['commit']:
                exit_code = max(exit_code, 1)

        except Exception as e:
            print(f"Error scoring {filepath}: {e}")
            import traceback
            traceback.print_exc()
            exit_code = 1

    if args.json:
        print(json.dumps(results, indent=2))

    sys.exit(exit_code)

if __name__ == '__main__':
    main()
