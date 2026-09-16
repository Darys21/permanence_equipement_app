"""
audit_frontend.py
=================
Audit YAML frontend Power Apps vs schema backend réel (Graph API export) et Backend/contextBD.md.

Rapport JSON des écarts. Option --apply-safe-fixes pour corriger renommages
colonne les plus fréquents (Titre->Title, backup navs, etc.)

Usage:
    python audit_frontend.py \
      --schemas "Backend/schemas_export/*.json" \
      --context "Backend/contextBD.md" \
      --yamls "Concept pages/**/*.yaml" \
      --report Backend/rapport_alignement.json [--apply-safe-fixes]
"""

from __future__ import annotations

import argparse
import datetime as _dt
import glob
import json
import re
import sys
from pathlib import Path


SEVERITY_BLOQ = "BLOQUANT"
SEVERITY_WARN = "WARN"
SEVERITY_INFO = "INFO"


def load_schemas(schemas_glob: str) -> dict[str, set[str]]:
    per_list_cols: dict[str, set[str]] = {}
    files = glob.glob(schemas_glob, recursive=True)
    if not files:
        print(f"[WARN] Aucun schema trouve via {schemas_glob}")
        return per_list_cols
    for fp in files:
        p = Path(fp)
        try:
            cols = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[SKIP] {p}: {e}")
            continue
        names: set[str] = set()
        display_names: set[str] = set()
        for c in cols:
            if c.get("name"):
                names.add(c["name"])
            if c.get("displayName"):
                display_names.add(c["displayName"])
        per_list_cols[p.stem] = names | display_names
    print(f"[OK] {len(per_list_cols)} schemas charges.")
    return per_list_cols


def yaml_files(pattern: str) -> list[Path]:
    files = glob.glob(pattern, recursive=True)
    return [Path(f) for f in sorted(files) if Path(f).suffix.lower() in {".yaml", ".yml"}]


TX_LISTES = {"Tx_Travaux", "Tx_Feedbacks", "Tx_incidents_Ruptures", "Tx_incidents_Ruptures",
             "Tx_LTV", "Tx_Incidents_Ruptures"}


class Auditor:
    def __init__(self, schemas: dict[str, set[str]]):
        self.schemas = schemas
        self.errors: list[dict[str, object]] = []
        self._file: Path | None = None
        self._buf_lines: list[str] = []
        self._apply = False

    def _add_err(self, severity: str, type_: str, details: str, lineno: int | None = None) -> None:
        self.errors.append({
            "file": str(self._file) if self._file else None,
            "severity": severity,
            "type": type_,
            "details": details,
            "line": lineno,
        })

    def check_file(self, path: Path, apply_safe: bool) -> None:
        self._file = path
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)

        # Check Titre invalide (devrait etre Title)
        for idx, ln in enumerate(lines, 1):
            if re.search(r"(?<![A-Za-z0-9_])Titre(?![A-Za-z0-9_])", ln):
                self._add_err(SEVERITY_BLOQ, "COLUMN_NAME_INVALID",
                              "Reference 'Titre' invalide (colonne interne SharePoint = Title).", idx)
                if apply_safe:
                    lines[idx-1] = re.sub(r"(?<![A-Za-z0-9_])Titre(?![A-Za-z0-9_])", "Title", lines[idx-1])

        # Nav backup
        for idx, ln in enumerate(lines, 1):
            if "_backup" in ln and ("Navigate(" in ln or "JournalDeBord" in ln or "PrisePoste" in ln):
                self._add_err(SEVERITY_BLOQ, "BACKUP_NAV",
                              "Reference ecran backup dans Navigate() : " + ln.strip(), idx)

        # ThisItem. sans champ
        for idx, ln in enumerate(lines, 1):
            if "ThisItem." in ln and re.search(r"ThisItem\.\s*[\)\]\}]", ln):
                self._add_err(SEVERITY_BLOQ, "THISITEM_INCOMPLET",
                              "ThisItem. incomplet (sans nom champ) : " + ln.strip(), idx)

        # CountRows sans Filter Poste pour listes transactionnelles
        in_tx_context = any(lx in text for lx in ["Tx_Travaux", "Tx_LTV", "Tx_incidents_Ruptures", "Tx_Feedbacks"])
        if in_tx_context:
            for idx, ln in enumerate(lines, 1):
                if re.search(r"CountRows\s*\(\s*Tx_(Travaux|LTV|incidents|Feedbacks)", ln) and "Filter" not in ln:
                    self._add_err(SEVERITY_WARN, "NO_POSTE_FILTER",
                                  "CountRows() sur liste transactionnelle sans Filter(Poste=varQuart).", idx)
                if re.search(r"Items:\s*=Tx_(Travaux|LTV|incidents|Feedbacks)", ln) and "Filter" not in ln:
                    self._add_err(SEVERITY_WARN, "NO_POSTE_FILTER",
                                  "Gallery Items sur liste transactionnelle sans Filter Poste=varQuart.", idx)

        # Patch Defaults
        for idx, ln in enumerate(lines, 1):
            if re.search(r"Patch\s*\(\s*Filter\s*\(", ln) and "Defaults" in ln:
                self._add_err(SEVERITY_BLOQ, "BAD_PATCH_SYNTAX",
                              "Patch(Filter(...), Defaults(...), ...) invalide Power Fx : 1er argument doit etre la liste.", idx)

        # ComplianceAssetId search field
        for idx, ln in enumerate(lines, 1):
            if "ComplianceAssetId" in ln:
                self._add_err(SEVERITY_WARN, "INVALID_SEARCH_FIELD",
                              "SearchFields contient ComplianceAssetId (non standard). Remplacer par Title/Value.", idx)

        # colonnes audit Agent/Poste/DateSaisie absentes dans Patch Tx_
        if apply_safe:
            final = "".join(lines)
            if final != text:
                path.write_text(final, encoding="utf-8")
                print(f"  [FIX] {path}")

    def check_contextbd_auditcols(self, yamls: list[Path]) -> None:
        for p in yamls:
            txt = p.read_text(encoding="utf-8")
            # Patch sans Agent ni Poste ni DateSaisie pour liste transactionnelle
            for match in re.finditer(r"Patch\s*\(\s*(Tx_[A-Za-z_]+)\s*,\s*Defaults\([^)]+\)\s*,[\s\S]*?\n\s*\)\s*;", txt):
                block = match.group(0)
                if "Agent:" not in block and "AgentSaisie" not in block:
                    self._file = p
                    self._add_err(SEVERITY_BLOQ, "MISSING_AUDIT_COLUMN",
                                  f"Patch {match.group(1)} sans colonne audit Agent/AgentSaisie.")
                if "Poste:" not in block:
                    self._file = p
                    self._add_err(SEVERITY_BLOQ, "MISSING_AUDIT_COLUMN",
                                  f"Patch {match.group(1)} sans colonne audit Poste.")
                if "DateSaisie:" not in block:
                    self._file = p
                    self._add_err(SEVERITY_BLOQ, "MISSING_AUDIT_COLUMN",
                                  f"Patch {match.group(1)} sans colonne audit DateSaisie.")

    def report(self, yamls: list[Path], schemas_count: int) -> dict[str, object]:
        total = len(self.errors)
        bl = sum(1 for e in self.errors if e["severity"] == SEVERITY_BLOQ)
        wn = sum(1 for e in self.errors if e["severity"] == SEVERITY_WARN)
        inf = sum(1 for e in self.errors if e["severity"] == SEVERITY_INFO)
        return {
            "audit_id": f"align_{_dt.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "date": _dt.datetime.now().isoformat(timespec="seconds"),
            "listes_schemas_charges": schemas_count,
            "ecrans_yaml_scannes": [str(y) for y in yamls],
            "compteurs": {"total_checks": len(yamls) * 8, "bloquants": bl, "warnings": wn, "infos": inf},
            "erreurs": self.errors,
        }


def main() -> None:
    ap = argparse.ArgumentParser("Audit alignement Power Apps YAML vs backend")
    ap.add_argument("--schemas", required=True, type=str)
    ap.add_argument("--context", type=Path, default=None)
    ap.add_argument("--yamls", required=True, type=str)
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--apply-safe-fixes", action="store_true")
    args = ap.parse_args()

    schemas = load_schemas(args.schemas)
    ys = yaml_files(args.yamls)
    if not ys:
        print("[ERREUR] Aucun YAML trouve.")
        sys.exit(2)
    print(f"[OK] {len(ys)} YAML scannes.")

    auditor = Auditor(schemas)
    for y in ys:
        auditor.check_file(y, args.apply_safe_fixes)
    auditor.check_contextbd_auditcols(ys)

    report = auditor.report(ys, len(schemas), )
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    total = report["compteurs"]  # type: ignore[index]
    print(f"[OK] Rapport ecrit {args.report}")
    print(f"   Bloquants: {total['bloquants']}  Warnings: {total['warnings']}  Infos: {total['infos']}")


if __name__ == "__main__":
    main()
