#!/usr/bin/env python3
"""
Manuscript Ingest: Convert input manuscript to normalized markdown.

Supports .docx, .tex, .pdf input formats via pandoc.

Usage:
    python scripts/ingest.py manuscripts/paper.docx outputs/journal/working.md
    python scripts/ingest.py manuscripts/paper.tex  outputs/journal/working.md
    python scripts/ingest.py manuscripts/paper.pdf  outputs/journal/working.md
"""

import sys
import subprocess
import argparse
from pathlib import Path
from typing import Optional


PANDOC_FROM_MAP = {
    '.docx': 'docx',
    '.tex': 'latex',
    '.pdf': 'pdf',
    '.txt': 'markdown',
    '.md': 'markdown',
}

PANDOC_MARKDOWN_OPTIONS = [
    '--wrap=none',               # No hard line wrapping
    '--markdown-headings=atx',   # Use # headings (ATX style)
    '--reference-links',         # Collect links at bottom
    '--strip-comments',          # Remove HTML comments from source
]


def run_pandoc(source: Path, output: Path, from_format: str, bibliography: Optional[Path] = None) -> tuple[bool, str]:
    """Run pandoc conversion. Returns (success, error_message)."""
    bib_args = ['--bibliography', str(bibliography)] if bibliography else []

    cmd = [
        'pandoc',
        '--from', from_format,
        '--to', 'markdown',
        *PANDOC_MARKDOWN_OPTIONS,
        *bib_args,
        '--output', str(output),
        str(source),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            return False, result.stderr or result.stdout
        return True, ''
    except subprocess.TimeoutExpired:
        return False, 'pandoc timed out (>120s)'
    except FileNotFoundError:
        return False, 'pandoc not found. Install pandoc: https://pandoc.org/installing.html'


def post_process_markdown(content: str, source_format: str) -> tuple[str, list[str]]:
    """Clean up common pandoc conversion artifacts. Returns (cleaned_content, warnings)."""
    warnings = []
    lines = content.split('\n')
    cleaned = []

    for line in lines:
        # Flag potential pandoc conversion artifacts
        if '???' in line:
            warnings.append(f"Possible conversion artifact (???): {line[:80]}")
        if r'\begin{' in line or r'\end{' in line:
            warnings.append(f"Leftover LaTeX environment: {line[:80]}")

        # Remove excessive blank lines (max 2 consecutive)
        cleaned.append(line)

    # Normalize multiple blank lines to at most 2
    result_lines = []
    blank_count = 0
    for line in cleaned:
        if line.strip() == '':
            blank_count += 1
            if blank_count <= 2:
                result_lines.append(line)
        else:
            blank_count = 0
            result_lines.append(line)

    return '\n'.join(result_lines), warnings


def ingest(source_path: Path, output_path: Path, bibliography: Optional[Path] = None) -> bool:
    """Ingest a manuscript file and convert to normalized markdown."""
    if not source_path.exists():
        print(f"Error: Source file not found: {source_path}", file=sys.stderr)
        return False

    suffix = source_path.suffix.lower()
    from_format = PANDOC_FROM_MAP.get(suffix)
    if from_format is None:
        print(f"Error: Unsupported format '{suffix}'.", file=sys.stderr)
        print(f"Supported formats: {', '.join(PANDOC_FROM_MAP.keys())}", file=sys.stderr)
        return False

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Ingesting: {source_path}")
    print(f"Format: {suffix} → markdown")
    print(f"Output: {output_path}")

    if suffix == '.pdf':
        print("Note: PDF conversion may lose some formatting. Review output carefully.")

    if bibliography:
        if not bibliography.exists():
            print(f"Warning: Bibliography file not found: {bibliography}", file=sys.stderr)
        else:
            print(f"Bibliography: {bibliography}")

    # Run pandoc
    success, error = run_pandoc(source_path, output_path, from_format, bibliography=bibliography)
    if not success:
        print(f"Error: pandoc failed:\n{error}", file=sys.stderr)
        return False

    # Post-process
    content = output_path.read_text(encoding='utf-8')
    cleaned, warnings = post_process_markdown(content, from_format)
    output_path.write_text(cleaned, encoding='utf-8')

    # Report
    line_count = len(cleaned.split('\n'))
    word_count = len(cleaned.split())
    print(f"Success: {line_count} lines, ~{word_count} words")

    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings[:10]:
            print(f"  - {w}")
        if len(warnings) > 10:
            print(f"  ... and {len(warnings) - 10} more. Review output file.")
        print("\nReview these artifacts before formatting.")

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Convert manuscript to normalized markdown via pandoc',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/ingest.py manuscripts/paper.docx outputs/lancet/working.md
  python scripts/ingest.py manuscripts/paper.tex  outputs/nejm/working.md
  python scripts/ingest.py manuscripts/paper.pdf  outputs/plos/working.md

Supported input formats:
  .docx   Word document (best conversion quality)
  .tex    LaTeX source
  .pdf    PDF (lossy; review output carefully)
  .txt    Plain text
  .md     Markdown (pass-through normalization)

Output:
  Normalized markdown in outputs/[journal]/working.md
        """
    )
    parser.add_argument('source', type=Path, help='Input manuscript file')
    parser.add_argument('output', type=Path, help='Output markdown file')
    parser.add_argument(
        '--bibliography', type=Path, default=None,
        help='Path to .bib file (overrides any bibliography referenced in the source)'
    )

    args = parser.parse_args()
    success = ingest(args.source, args.output, bibliography=args.bibliography)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
