"""
parse_spec_columns.py
=====================
Depuis texte extrait pdf (pdf_output.txt), isole les tables 6 listes SP
et exporte JSON structuré colonne/type/obligatoire/choix si détectable.

Usage:
    python parse_spec_columns.py --input script/pdf_output.txt --output Backend/schemas_from_pdf.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


KNOWN_LISTS = [
    "Ref_Cantons",
    "Ref_Acteurs",
    "Tx_Travaux",
    "Tx_Feedbacks",
    "Tx_incidents_Ruptures",
    "Tx_Incidents_Ruptures",
    "Tx_LTV",
]


def normalize_list_name(name: str) -> str:
    for kn in KNOWN_LISTS:
        if name.lower().replace("_", "") == kn.lower().replace("_", ""):
            return kn
    return name


def extract_tables(text: str) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    lines = text.splitlines()
    current_list: str | None = None
    in_table = False
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        # Lignes contenant nom liste comme section
        for kn in KNOWN_LISTS:
            if re.search(rf"(^|[^A-Za-z_]){re.escape(kn)}([^A-Za-z_]|$)", line):
                current_list = kn
                in_table = True
                result.setdefault(current_list, [])
                break
        if current_list and in_table:
            # Ligne table format potentiel: NomColonne | Type | Oblig
            cols = [c.strip() for c in re.split(r"\s{2,}|\t|\|", line) if c.strip()]
            # Filtre lignes d'entete
            if cols and cols[0].lower() in {"colonne", "champ", "nom", "column"}:
                continue
            # Sinon considere 3 champs = ligne table colonne
            if current_list and len(cols) >= 2 and cols[0] not in KNOWN_LISTS:
                entry: dict[str, str] = {"colonne": cols[0]}
                if len(cols) >= 2:
                    entry["type"] = cols[1]
                if len(cols) >= 3:
                    entry["obligatoire"] = cols[2]
                if len(cols) >= 4:
                    entry["remarque"] = " ".join(cols[3:])
                result.setdefault(current_list, []).append(entry)
    return result


def main() -> None:
    ap = argparse.ArgumentParser("Parse texte PDF -> JSON colonnes")
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    text = args.input.read_text(encoding="utf-8")
    data = extract_tables(text)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    total = sum(len(v) for v in data.values())
    print(f"[OK] {len(data)} listes / {total} colonnes ecrites dans {args.output}")


if __name__ == "__main__":
    main()
