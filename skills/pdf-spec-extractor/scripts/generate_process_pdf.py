"""
generate_process_pdf.py
=======================
Genere PDF process_developpement_app.pdf depuis markdown source.

Usage:
    python generate_process_pdf.py --input Documentation/process_dev_source.md --output Documentation/process_developpement_app.pdf

Dependances:
    pip install reportlab markdown
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer
except ImportError:
    print("ERREUR: pip install reportlab")
    sys.exit(1)


def md_to_story(md_text: str) -> list:
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], spaceAfter=10, fontSize=18)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], spaceAfter=8, fontSize=15)
    h3 = ParagraphStyle("H3", parent=styles["Heading3"], spaceAfter=6, fontSize=13)
    body = ParagraphStyle("Body", parent=styles["BodyText"], spaceAfter=6, fontSize=11, leading=16)
    bullet = ParagraphStyle("Bullet", parent=body, leftIndent=14, bulletIndent=4, spaceAfter=4)

    story: list = []
    lines = md_text.splitlines()
    code_buf: list[str] = []
    in_code = False
    for ln in lines:
        if in_code:
            if ln.startswith("```"):
                txt = "<br/>".join([re.sub(r" ", "&nbsp;", c) for c in code_buf])
                story.append(Paragraph(f"<code>{txt}</code>", body))
                code_buf = []
                in_code = False
            else:
                code_buf.append(ln)
            continue
        if ln.startswith("```"):
            in_code = True
            continue
        if not ln.strip():
            story.append(Spacer(1, 6))
            continue
        if ln.startswith("### "):
            story.append(Paragraph(ln[4:], h3))
        elif ln.startswith("## "):
            story.append(Paragraph(ln[3:], h2))
        elif ln.startswith("# "):
            story.append(Paragraph(ln[2:], h1))
        elif ln.startswith("---"):
            story.append(PageBreak())
        elif ln.lstrip().startswith(("- ", "* ")):
            txt = ln.lstrip()[2:]
            story.append(Paragraph(txt, bullet, bulletText="\u2022"))
        else:
            # inline bold **text** -> <b>
            txt = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", ln)
            txt = re.sub(r"`([^`]+)`", r"<code>\1</code>", txt)
            story.append(Paragraph(txt, body))
    return story


def main() -> None:
    ap = argparse.ArgumentParser("Markdown -> PDF process")
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    md = args.input.read_text(encoding="utf-8")
    story = md_to_story(md)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(args.output), pagesize=A4,
                            leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)
    doc.build(story)
    print(f"[OK] PDF genere: {args.output}")


if __name__ == "__main__":
    main()
