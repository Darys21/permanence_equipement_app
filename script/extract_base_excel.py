"""
extract_base_excel.py
=====================
Lit BASE/PERMANENCE EQUIPEMENT 2026 v4.xlsx, extrait sheets, valeurs uniques
colonne par colonne, compare choix backend Graph -> flag ecarts.
"""
from __future__ import annotations

import json
from pathlib import Path

import openpyxl

ROOT = Path(r"c:\Users\jyd.anguilet\Downloads\Joan - SETRAG\PERMANANCE EQUIPEMENT")
XLSX = ROOT / "BASE" / "PERMANENCE EQUIPEMENT 2026 v4.xlsx"
BACKEND_SCHEMAS = ROOT / "Backend" / "schemas_export"
OUT = ROOT / "Backend" / "BASE_vs_GRAPH_alignement.md"

wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
print(f"Sheets excel: {wb.sheetnames}")

# Valeurs choix Graph connues
graph_choix: dict[str, list[str]] = {}
for jp in BACKEND_SCHEMAS.glob("*.json"):
    obj = json.loads(jp.read_text(encoding="utf-8"))
    cols = obj["value"] if isinstance(obj, dict) and "value" in obj else obj
    for c in cols:
        if c.get("choice") and c["choice"].get("choices"):
            key = f"{jp.stem}.{c.get('name')}"
            graph_choix[key] = list(c["choice"]["choices"])
print(f"\nValeurs choix Graph export: {len(graph_choix)}")
for k, v in graph_choix.items():
    print(f"  {k}: {v}")

# Extraire sheets Excel -> 10 premières lignes, colonnes non vides
print("\n" + "=" * 90)
print("CONTENU EXCEL PAR SHEET (max 20 lignes, max 12 cols)")
print("=" * 90)
excel_summary_parts = [
    "# Alignement BASE Excel vs backend Graph export\n",
    f"Excel: `{XLSX.name}` - Sheets: {', '.join(wb.sheetnames)}\n",
    "\n## Valeurs Graph Choix backend\n",
]
for k, v in graph_choix.items():
    excel_summary_parts.append(f"- `{k}` : {' / '.join(v)}\n")
excel_summary_parts.append("\n## Extraction brute Sheets Excel\n")

for sn in wb.sheetnames:
    ws = wb[sn]
    excel_summary_parts.append(f"\n### Sheet: {sn}\n")
    excel_summary_parts.append("```\n")
    rows_printed = 0
    table_rows = []
    for row in ws.iter_rows(values_only=True, max_row=250):
        if all(c is None or str(c).strip() == "" for c in row):
            continue
        clean = tuple("" if c is None else str(c).strip() for c in row[:14])
        table_rows.append(clean)
        if rows_printed < 20:
            print(" | ".join(f"{x[:32]:<32}" for x in clean))
            excel_summary_parts.append(" | ".join(x for x in clean) + "\n")
            rows_printed += 1
    excel_summary_parts.append("```\n")
    print(f"... ({len(table_rows)} lignes non vides sheet {sn})")

wb.close()

OUT.write_text("".join(excel_summary_parts), encoding="utf-8")
print(f"\nRapport markdown ecrit: {OUT}")
