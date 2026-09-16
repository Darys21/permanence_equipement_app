# EXEMPLE source markdown pour générer PDF du processus de développement (avec generate_process_pdf.py).
# Copier ce fichier dans Documentation/PROCESS_DEV.md puis run generate_process_pdf.py.

# Processus de développement - Application Permanence Équipement

## 1. Objectif

Mettre à disposition des équipes opérationnelles une application Power Apps fiabilisant la collecte de données sur les chantiers, limitations de vitesse, incidents et feed-backs acteurs.

## 2. Cycle de vie d'une modification

1. Identification du besoin (backlog item)
2. Analyse impact frontend + backend
3. Extraction schema backend réel avec skill `sharepoint-graph-schema`
4. Mise à jour YAML écrans (skill `powerapps-llm-yaml`)
5. Audit alignement colonnes (skill `powerapps-backend-alignment`)
6. Publication Power Apps test
7. Validation utilisateur
8. Production

## 3. Règles de nommage

Chaque liste SharePoint transacationnelle contient 3 colonnes audit:
- `Agent`
- `Poste`
- `DateSaisie`

## 4. Contrôles obligatoires avant commit

1. Aucune référence à des écrans suffixés `_backup`
2. Pas de colonne `Titre` interne (toujours `Title`)
3. Tous les Patch() utilisent `Defaults()` en création
4. Toutes les galleries filtrent `Poste = varQuart`

---

## 5. Procédure rollback

- Revenir au commit précédent via Git
- Restaurer la version Power Apps "Publiée" dans Détails > Versions
- Contacter administrateur site SharePoint en cas de schéma rollback nécessaire
