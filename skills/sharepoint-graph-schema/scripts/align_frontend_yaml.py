# align_frontend_yaml.py
# Utilise schemas JSON exportes par fetch_sharepoint_schema.py pour transformer
# les references de colonnes frontend YAML Power Apps vers le nom reel backend.
#
# Usage:
#   python align_frontend_yaml.py --schemas Backend/schemas_export/*.json \
#       --input "Concept pages/Ecran 2 Journal de bord/dashboard.yaml" \
#       --output "Concept pages/Ecran 2 Journal de bord/dashboard.aligned.yaml"
#
# Ce script est un utilitaire du skill `sharepoint-graph-schema`.
# Il NE MODIFIE PAS l'original ; il ecrit dans --output. A review avant remplacement.

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def load_schemas(paths: list[Path]) -> dict[str, dict[str, str]]:
    """Pour chaque liste, construit mapping displayName -> name interne backend."""
    mapping: dict[str, dict[str, str]] = {}
    for p in paths:
        try:
            cols = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[SKIP] JSON invalide {p}: {e}")
            continue
        name_map: dict[str, str] = {}
        for c in cols:
            dn = c.get("displayName") or c.get("name")
            nm = c.get("name")
            if dn and nm:
                name_map[dn] = nm
                name_map[nm] = nm
        mapping[p.stem] = name_map
    return mapping


def remap(text: str, per_list_mapping: dict[str, dict[str, str]]) -> tuple[str, int]:
    """
    Remplace dans le texte toutes les occurrences displayName connus par le
    backend name si different. On ne remplace que les identifiants Power Fx
    (mots entiers, suffixe .Value garde).
    """
    flat: dict[str, str] = {}
    for mp in per_list_mapping.values():
        flat.update(mp)
    seen = set()
    new_text = text
    count = 0
    sorted_keys = sorted(flat.keys(), key=len, reverse=True)
    for k in sorted_keys:
        v = flat[k]
        if k == v or not k.strip():
            continue
        pattern = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(k) + r"(?![A-Za-z0-9_])")
        new_text, n = pattern.subn(v, new_text)
        if n:
            seen.add((k, v))
            count += n
    for (k, v) in seen:
        print(f"  [REMAP] '{k}' -> '{v}'")
    return new_text, count


def main() -> None:
    ap = argparse.ArgumentParser("Aligner frontend YAML sur noms colonnes backend reels")
    ap.add_argument("--schemas", nargs="+", required=True, type=Path)
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input not found: {args.input}")

    mapping = load_schemas([p for p in args.schemas if p.exists()])
    src = args.input.read_text(encoding="utf-8")
    new_src, n = remap(src, mapping)
    args.output.write_text(new_src, encoding="utf-8")
    print(f"\n[DONE] {n} substitutions ecrites dans {args.output}.")


if __name__ == "__main__":
    main()
