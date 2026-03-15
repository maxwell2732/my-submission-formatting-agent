#!/usr/bin/env python3
"""
Export formatted markdown to docx using pandoc + reference template.

Usage:
    python scripts/export_docx.py outputs/journal/manuscript_formatted.md outputs/journal/manuscript_formatted.docx
    python scripts/export_docx.py outputs/journal/working.md outputs/journal/manuscript_formatted.docx --reference templates/reference.docx
"""

import sys
import subprocess
import argparse
from pathlib import Path


DEFAULT_REFERENCE = Path('templates/reference.docx')


def export_docx(
    source: Path,
    output: Path,
    reference_doc: Path = DEFAULT_REFERENCE,
    mathml: bool = True,
) -> bool:
    """Convert markdown to docx using pandoc. Returns success bool."""
    if not source.exists():
        print(f"Error: Source file not found: {source}", file=sys.stderr)
        return False

    if not reference_doc.exists():
        print(f"Warning: Reference doc not found at {reference_doc}.", file=sys.stderr)
        print("To create a default reference: pandoc --print-default-data-file reference.docx > templates/reference.docx", file=sys.stderr)
        print("Proceeding without reference doc (pandoc default styles will be used).", file=sys.stderr)
        ref_args = []
    else:
        ref_args = ['--reference-doc', str(reference_doc)]

    # Create output directory if needed
    output.parent.mkdir(parents=True, exist_ok=True)

    # Use --mathml so LaTeX math converts to native OOXML equations in .docx
    math_args = ['--mathml'] if mathml else []

    cmd = [
        'pandoc',
        '--from', 'markdown',
        '--to', 'docx',
        *ref_args,
        *math_args,
        '--output', str(output),
        str(source),
    ]

    print(f"Exporting: {source}")
    print(f"Output: {output}")
    if ref_args:
        print(f"Reference: {reference_doc}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            print(f"Error: pandoc failed:\n{result.stderr or result.stdout}", file=sys.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("Error: pandoc timed out (>120s)", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("Error: pandoc not found. Install pandoc: https://pandoc.org/installing.html", file=sys.stderr)
        return False

    if output.exists():
        size_kb = output.stat().st_size / 1024
        print(f"Success: {output.name} ({size_kb:.1f} KB)")
        if mathml:
            print("MathML: enabled (LaTeX math → native OOXML equations)")
        if size_kb < 5:
            print("Warning: Output file is very small — check for conversion issues.", file=sys.stderr)
        return True
    else:
        print("Error: Output file was not created.", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert formatted markdown to docx via pandoc',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/export_docx.py outputs/lancet/manuscript_formatted.md outputs/lancet/manuscript_formatted.docx
  python scripts/export_docx.py outputs/nejm/working.md outputs/nejm/out.docx --reference templates/custom.docx

Setup (first time):
  pandoc --print-default-data-file reference.docx > templates/reference.docx

The reference.docx defines heading styles, fonts, and margins for the output.
Customize it in Word, then save to templates/reference.docx.
        """
    )
    parser.add_argument('source', type=Path, help='Input markdown file')
    parser.add_argument('output', type=Path, help='Output docx file')
    parser.add_argument(
        '--reference', type=Path, default=DEFAULT_REFERENCE,
        help=f'Reference docx template (default: {DEFAULT_REFERENCE})'
    )
    parser.add_argument(
        '--no-mathml', action='store_true', default=False,
        help='Disable MathML conversion (LaTeX math stays as images/text instead of native OOXML)'
    )

    args = parser.parse_args()
    success = export_docx(args.source, args.output, args.reference, mathml=not args.no_mathml)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
