# SKILLS PROJET - PERMANANCE EQUIPEMENT

Ensemble des compétences réutilisables du dépôt. Structure inspirée du
modèle: `skills/<nom-skill>/SKILL.md`, `references/`, `assets|scripts|examples/`.

## Arborescence

```
skills/
├── README.md                                 (ce fichier)
│
├── powerapps-llm-yaml/                       (Skill 1: Génération/correction YAML Power Apps Canvas)
│   ├── SKILL.md
│   ├── references/
│   │   ├── POWERAPPS_AI_LEARN.md             (types SharePoint ↔ Power Fx, délégation, Patch, Navigate, Refresh)
│   │   └── YAML_BEST_PRACTICES.md            (règles syntaxe YAML, versions contrôles, cascade, audit final)
│   └── assets/
│       └── example.pa.yaml                   (canevas minimal: Header, Division→Canton cascade, SaveButton Patch Defaults)
│
├── sharepoint-graph-schema/                  (Skill 2: Récupération schema backend réel 6 listes)
│   ├── SKILL.md
│   ├── references/
│   │   ├── GRAPH_API_SHAREPOINT.md           (endpoints, headers, columnType map, permissions)
│   │   └── env.example                       (template .env à copier racine: TENANT_ID, CLIENT_ID, mode auth)
│   ├── scripts/
│   │   ├── fetch_sharepoint_schema.py        (device code ou client-credentials MSAL → export JSON + ALL_COLUMNS.yaml)
│   │   └── align_frontend_yaml.py            (remap frontend → noms backend reels; output .aligned.yaml)
│   └── assets/
│
├── pdf-spec-extractor/                       (Skill 3: Extraire PDF spec + generer PDF process)
│   ├── SKILL.md
│   ├── references/
│   │   └── PDF_EXTRACTION.md                 (PyPDF2 / reportlab tips, pipelines, encode UTF-8)
│   ├── scripts/
│   │   ├── extract_pdf_text.py               (PERMANENCE EQUIPEMENT.pdf → script/pdf_output.txt)
│   │   ├── parse_spec_columns.py             (pdf_output.txt → JSON colonnes 6 listes)
│   │   └── generate_process_pdf.py           (PROCESS_DEV.md → Documentation/process_developpement_app.pdf)
│   └── examples/
│       └── PROCESS_DEV.example.md            (markdown source exemple)
│
└── powerapps-backend-alignment/              (Skill 4: Audit alignement 4 YAML vs 6 listes)
    ├── SKILL.md
    ├── references/
    │   └── AUDIT_FRONTBACK.md                (8 types vérifications systématiques, cas typiques)
    ├── scripts/
    │   └── audit_frontend.py                 (scan YAML → JSON rapport, option --apply-safe-fixes)
    └── examples/
        └── rapport_alignement.example.md     (exemple rapport typique)
```

## Skill existant déjà dans repo (non dans skills/)

```
.agents/skills/caveman/                        (.agents/skills/ natif TRAE, pas skills/)
    SKILL.md + README.md                       (style réponse caveman)
```

---

## Workflow complet bout en bout

1. **Phase 1 - Extraire PDF spec métier**
   ```
   python skills/pdf-spec-extractor/scripts/extract_pdf_text.py \
     --input "Documentation/PERMANENCE EQUIPEMENT.pdf" --output script/pdf_output.txt
   python skills/pdf-spec-extractor/scripts/parse_spec_columns.py \
     --input script/pdf_output.txt --output Backend/schemas_from_pdf.json
   ```

2. **Phase 2 - Récupérer schéma backend réel SharePoint**
   - Copier `skills/sharepoint-graph-schema/references/env.example` → racine `.env`, renseigner TENANT_ID/CLIENT_ID
   - Exécuter:
   ```
   python skills/sharepoint-graph-schema/scripts/fetch_sharepoint_schema.py
   ```
   - Résultat dans `Backend/schemas_export/` (1 JSON par liste + ALL_COLUMNS.yaml)

3. **Phase 3 - MAJ Backend/contextBD.md**
   - Comparer ALL_COLUMNS.yaml exporté vs `Backend/contextBD.md`. Mettre à jour les types.
   - S'assurer: colonnes audit Agent/Poste/DateSaisie présentes; types Choix vs Texte corrects; CantonID type Lookup ou Nombre.

4. **Phase 4 - Générer / Modifier écrans Power Apps YAML**
   - Utiliser canevas `skills/powerapps-llm-yaml/assets/example.pa.yaml`
   - Respecter `SKILL.md` skill powerapps-llm-yaml (Choix .Value / {Value:}, cascade, Defaults Patch, Reset Refresh Notify)

5. **Phase 5 - Audit alignement Frontend / Backend**
   ```
   python skills/powerapps-backend-alignment/scripts/audit_frontend.py \
     --schemas "Backend/schemas_export/*.json" \
     --context "Backend/contextBD.md" \
     --yamls "Concept pages/**/*.yaml" \
     --report Backend/rapport_alignement.json [--apply-safe-fixes]
   ```

6. **Si écarts renommages colonnes**
   ```
   python skills/sharepoint-graph-schema/scripts/align_frontend_yaml.py \
     --schemas Backend/schemas_export/*.json \
     --input "Concept pages/Ecran 2 Journal de bord/dashboard.yaml" \
     --output "Concept pages/Ecran 2 Journal de bord/dashboard.aligned.yaml"
   ```
   puis comparer et remplacer si ok.

7. **Publication + documentation**
   - Générer PDF process mis à jour:
   ```
   python skills/pdf-spec-extractor/scripts/generate_process_pdf.py \
     --input Documentation/PROCESS_DEV.md --output Documentation/process_developpement_app.pdf
   ```

---

## Quick: Prérequis tous skills
```
pip install msal requests PyYAML python-dotenv rich pypdf reportlab markdown
```
