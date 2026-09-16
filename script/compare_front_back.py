"""
compare_front_back.py
=====================
Scan 4 YAML Power Apps frontend pour divergences vs backend reel Graph.
Genere rapport JSON + resume console.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"c:\Users\jyd.anguilet\Downloads\Joan - SETRAG\PERMANANCE EQUIPEMENT")
YAMLS_DIR = ROOT / "Concept pages"

# Règles de divergence critiques (motif regex -> explication correctif)
RULES = [
    # COLONNES Tx_Travaux
    (r"\bDateTravaux\b",         "DateTravaux -> Datetravaux (nom interne SP = Datetravaux un mot t minuscule)", "DATETRAVAUX_NOM"),
    (r"\bHeure_Autorisee\b",     "Heure_Autorisee -> Heures_Autorisee (PLURIEL interne!)", "HEURE_AUT_PLURIEL"),
    (r"\bHeure_Degagement\b",    "Heure_Degagement -> Heures_Degagement (PLURIEL interne!)", "HEURE_DEG_PLURIEL"),
    (r"\bHeure_Voie_Retablie\b", "Heure_Voie_Retablie -> Heures_Voie_Retablie (PLURIEL interne!)", "HEURE_VR_PLURIEL"),
    (r"\bMotif_Engagement_Tardif\b(?!s)", "Motif_Engagement_Tardif -> Motifs_Engagement_Tardif (PLURIEL Motifs_)", "MOTIFS_ENG_PLURIEL"),
    (r"\bRegimeTravaux\b",       "RegimeTravaux -> R_x00e9_gimetravaux (unicode é interne)", "REGIME_UNICODE"),
    (r"\bRégime_travaux\b",      "Régime_travaux -> R_x00e9_gimetravaux (unicode é interne)", "REGIME_UNICODE2"),
    # INCIDENTS
    (r"\bHeure_Debut\b(?!_x00e9)", "Heure_Début texte direct -> Heure_D_x00e9_but (é interne)", "INCIDENT_HEURE_DEBUT"),
    (r"\bCantonID\b(?![0_])",    "CantonID sur Incidents/LTV -> CantonID0 (Incidents Lookup) ou CantonID_ (LTV Lookup) sur bonnes listes. CantonID Nombre seulement OK sur Tx_Travaux.", "CANTON_FK_TYPE"),
    (r"[ ']CantonID[ ']",        "Vérifier sur quelle liste (Tx_Travaux:Nombre OK; Incidents:CantonID0 Lookup; LTV:CantonID_ Lookup)", "CANTON_CTX_CHECK"),
    # LTV
    (r"\bActeurID\b(?!0)",       "ActeurID sur LTV -> ActeurID0 Lookup suffix 0; ActeurID Nombre OK seulement sur Tx_Travaux", "ACTEUR_LTV_LOOKUP"),
    (r"\bDate_Imposition\b",     "Date_Imposition I MAJ -> Date_imposition i minuscule backend", "IMPOSITION_CASSE"),
    (r'Imposée \(Active\)',      '"Imposée (Active)" -> backend reel = "Imposée" SANS parentheses', "STATUT_LTV_IMPOSEE"),
    (r'Supprimée \(Levée\)',     '"Supprimée (Levée)" -> backend reel = "Supprimée" SANS parentheses', "STATUT_LTV_SUPPRIMEE"),
    # FEEDBACKS
    (r"StatutContact\s*:\s*\{\s*Value\s*:", "StatutContact {Value: ...} CHOIX -> StatutContact BOOLEAN backend reel (=true/false)", "STATUTCONTACT_BOOLEAN"),
    (r"MoyenCom.*Sur place",      "MoyenCom 'Sur place' existe PAS backend. Retirer; backend: Whatsapp, Telephone, Thuraya, Thuraya + Telephone", "MOYENCOM_SURPLACE"),
    (r"MoyenCom.*WhatsApp.*Phone", "MoyenCom valeurs 'WhatsApp'/'Phone' -> backend reel: Whatsapp (min a)/Telephone (fr)", "MOYENCOM_VALEURS"),
    # POSTE colonne type CHOIX partout - TEXTE errone
    (r"Poste\s*:\s*varQuart(?!\s*[,}])",  "Poste = varQuart TEXTE -> Poste colonne CHOIX! → Poste: {Value: varQuart}", "POSTE_CHOIX_WRITE"),
    (r"Filter\([^,]+,\s*Poste\s*=\s*varQuart",  "Filter Poste = varQuart sans .Value → Poste est CHOIX! Poste.Value = varQuart", "POSTE_CHOIX_FILTER"),
    (r"ThisItem\.Poste\s*[,\)\]]|[^.]Poste\s*[<>=]", "Reference Poste sans .Value (lecture) → Poste est CHOIX! ThisItem.Poste.Value", "POSTE_CHOIX_READ"),
    # AGENT colonne - texte errone
    (r"Agent\s*:\s*User\(\)\.FullName", "Agent texte plein -> AgentSaisie colonne PERSONNE! record Claims format", "AGENT_SAISIE_CLAIMS"),
    (r"ThisItem\.Agent\b",        "ThisItem.Agent texte -> ThisItem.AgentSaisie.DisplayName colonne Personne", "AGENT_SAISIE_READ"),
    # REF CANTONS PK Debut
    (r"PK_Debut",                 "Ref_Cantons -> PK_d_x00e9_but nom interne (é encode)", "REF_CANTON_PK_E"),
]

YAMLS_DIR = ROOT / "Frontend"
YAMLS_DIR2 = ROOT / "Concept pages"
REPORTS: list[dict] = []
total = 0
yamls = list(YAMLS_DIR.rglob("*.yaml")) + list(YAMLS_DIR.rglob("*.yml"))
yamls += list(YAMLS_DIR2.rglob("*.yaml")) + list(YAMLS_DIR2.rglob("*.yml"))
# unique paths
seen: set[Path] = set()
yamls_uniq: list[Path] = []
for y in yamls:
    if y in seen:
        continue
    seen.add(y)
    yamls_uniq.append(y)
yamls = yamls_uniq
print(f"Scan {len(yamls)} YAML frontend...")
for y in yamls:
    text = y.read_text(encoding="utf-8")
    for pattern, msg, code in RULES:
        for m in re.finditer(pattern, text):
            lineno = text.count("\n", 0, m.start()) + 1
            total += 1
            REPORTS.append({
                "file": str(y.relative_to(ROOT)),
                "line": lineno,
                "code": code,
                "match": m.group(0)[:80],
                "recommendation": msg,
            })

REPORTS.sort(key=lambda r: (r["file"], r["line"]))
out = ROOT / "Backend" / "rapport_divergences_front_back.json"
out.write_text(json.dumps({
    "generated_at": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
    "yamls_scanned": [str(y.relative_to(ROOT)) for y in yamls],
    "total_divergences": total,
    "details": REPORTS,
}, indent=2, ensure_ascii=False), encoding="utf-8")

# Resume console par fichier
from collections import defaultdict
per_file: dict[str, int] = defaultdict(int)
per_code: dict[str, int] = defaultdict(int)
for r in REPORTS:
    per_file[r["file"]] += 1
    per_code[r["code"]] += 1

print()
print("=" * 80)
print(f"TOTAL DIVERGENCES DETECTEES: {total}")
print("=" * 80)
print("\nPar fichier YAML:")
for f, c in sorted(per_file.items(), key=lambda x: -x[1]):
    print(f"  {c:3d}  {f}")
print("\nTop types divergence:")
for c, n in sorted(per_code.items(), key=lambda x: -x[1])[:10]:
    print(f"  {n:3d}  {c}")
print(f"\nRapport detail JSON: {out}")
