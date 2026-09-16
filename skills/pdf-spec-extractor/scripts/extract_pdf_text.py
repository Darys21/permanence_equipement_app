"""
extract_pdf_text.py
===================
Extrait texte brut depuis PDF spec PERMANENCE EQUIPEMENT.
Resultat ecrit UTF-8 dans fichier texte (pas print console, evite cp1252 Windows erreur).

Usage:
    python extract_pdf_text.py --input "Documentation/PERMANENCE EQUIPEMENT.pdf" --output script/pdf_output.txt
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("ERREUR: installer pypdf ou PyPDF2: pip install pypdf")
        sys.exit(1)


def extract(pdf: Path) -> str:
    reader = PdfReader(str(pdf))
    out: list[str] = []
    for i, page in enumerate(reader.pages, start=1):
        out.append(f"\n=== PAGE {i} ===\n")
        txt = page.extract_text() or ""
        out.append(txt)
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser("Extraire texte PDF")
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    if not args.input.exists():
        raise SystemExit(f"Fichier introuvable: {args.input}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    text = extract(args.input)
    args.output.write_text(text, encoding="utf-8")
    print(f"[OK] {args.output} ({len(text)} chars)")


if __name__ == "__main__":
    main()
