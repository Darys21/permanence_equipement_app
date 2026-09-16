---
name: pdf-spec-extractor
description: Extrait le texte et la structure des spécifications PDF (PERMANENCE EQUIPEMENT.pdf, process_developpement_app.pdf) pour nourrir LLM + aligner les YAML Power Apps et les schémas SharePoint. Génération des PDF de process/projet en retour.
---

## But
Transformer PDF spec métier brut en texte structuré + points clés exploitable par LLM/agents, et générer des PDF de process developpement projet uniforme.

## Quand déclencher
- Mise à jour de la spec `PERMANENCE EQUIPEMENT.pdf` (après modifications métier)
- Validation changements YAML vs PDF (colonnes / user stories / typage)
- Génération du PDF process de dev depuis documentation markdown
- Création `pdf_output.txt` version texte exploitable par recherche + agent LLM

## Prérequis Python
```
pip install PyPDF2 reportlab pypdf
```

## Workflow standard

### 1. Extraire texte PDF (scripts/extract_pdf_text.py)
```bash
python skills/pdf-spec-extractor/scripts/extract_pdf_text.py \
  --input "Documentation/PERMANENCE EQUIPEMENT.pdf" \
  --output script/pdf_output.txt
```

Sortie `pdf_output.txt` contient concaténation texte toutes pages.

### 2. Extraction ciblée colonnes (scripts/parse_spec_columns.py)
Parse la table des 6 listes depuis PDF texte. Génère JSON colonnes:
```
python skills/pdf-spec-extractor/scripts/parse_spec_columns.py \
  --input script/pdf_output.txt \
  --output Backend/schemas_from_pdf.json
```

Structure JSON de sortie:
```json
{
  "Tx_Travaux": [
    {"colonne": "Date_travaux", "type": "Date et heure", "obligatoire": "Oui"},
    {"colonne": "Heure_Demande", "type": "Date et heure", "obligatoire": "Non"}
  ]
}
```

### 3. Comparaison spec PDF vs Backend contextBD.md (scripts/diff_spec_vs_context.py)
```
python skills/pdf-spec-extractor/scripts/diff_spec_vs_context.py
```
Rapporte écarts entre:
- Colonnes PDF spec vs colonnes contextBD.md actuelles
- Noms colonnes YAML frontend vs spec PDF
- Types colonne Choix/Texte/Nombre divergents

### 4. Génération PDF process_developpement_app.pdf (scripts/generate_process_pdf.py)
Prend markdown process_developpement source, génère PDF uniforme:
```
python skills/pdf-spec-extractor/scripts/generate_process_pdf.py \
  --input Documentation/PROCESS_DEV.md \
  --output Documentation/process_developpement_app.pdf
```

## Format extraction et normalisation
- Encodage sortie: UTF-8 (jamais console print cp1252 → risque UnicodeEncodeError sur caractères ▼, accents français)
- Ordre pages: PDF pages indexées 0-based.
- Filtrage: en-têtes/pieds-page numériques supprimés par défaut.
- Tableaux: colonnes séparées par `|` (pipe) pour format Markdown-like dans txt.

## Interfaces avec autres skills
- `sharepoint-graph-schema` → comparaison spec PDF vs colonnes backend réel Graph exportées
- `powerapps-backend-alignment` → utilise parse_spec_columns.json pour audit frontend vs spec
- `powerapps-llm-yaml` → référence pdf_output.txt pour user stories US1.x, US2.x...

## Erreurs fréquentes
| Erreur | Cause | Solution |
| --- | --- | --- |
| UnicodeEncodeError: 'charmap' codec ... \u25bc | Print console Windows cp1252 | Toujours écrire fichier texte UTF-8, pas print. |
| Extraire texte vide ou partiel | PDF image (OCR non fait) | Convertir PDF avec couche texte d'abord. |
| Génération PDF police non latin | ReportLab defaut Helvetica | Ajouter police TTF support latin étendu. |
