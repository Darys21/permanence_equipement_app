---
name: powerapps-backend-alignment
description: Audite et corrige les écarts entre les 4 YAML Power Apps (frontend) contre le schéma réel 6 listes SharePoint (backend). Compare 3 sources: PDF spec, Backend/contextBD.md, export Graph exporté par Graph API). Génére rapport JSON + correction automatique des renommages de colonnes les plus fréquents.
---

## But
Auditer la cohérence frontend ↔ backend. Vérifier TOUS les noms colonnes, types, Patch, lecture `.Value` (choix, filtres Poste=varQuart, colonnes audit Agent/Poste/DateSaisie.

## Quand déclencher
- Après modification d'un écran YAML
- Avant publication app Power Apps
- Après réception export réel backend Graph API
- Après changement PDF spec métier
- Sur question "est-ce que mes YAML est bien connecté aux listes SP?"

## Sources de vérité, par ordre de priorité
1. **Schema réel Graph API exporté par Graph (Backend/schemas_export/*.json + ALL_COLUMNS.yaml)
2. **Backend/contextBD.md** (documentation schéma consolidée humaine
3. **PERMANENCE EQUIPEMENT.pdf / script/pdf_output.txt (PDF spécification)

## Rapport d'audit
Le rapport est structuré en 6 sections par rapport aux 6 listes SP

### 1. Vérifications systématiques

#### A. Noms colonnes valides (ERREUR si référence à colonne inventée

Pour chaque fichier YAML Concept pages/, chaque `ThisItem.`, chaque colonne référence patch liste.

Listes: Ref_Cantons, Ref_Acteurs, Tx_Travaux, Tx_Feedbacks, Tx_incidents_Ruptures, Tx_LTV.

Champ inventé typique: `Titre` (devrait être Title), Date_travaux, DateTravaux, Heures_Degagement vs Heure_Degagement, AgentSaisie, Poste.Value vs Poste, Motifs vs Motif, Régime_travaux vs RegimeTravaux, Date_imposition vs Date_Imposition.

#### B. Type cohérent entre frontend ↔ backend
| Backend type | Frontend écriture | Frontend lecture |
| --- | --- | --- |
| Texte simple | `Champ: "value" simple string" | `ThisItem.Champ`
| Choix | `Champ: {Value: X.Selected.Value}` | `ThisItem.Champ.Value` |
| Nombre | `Champ: Value(Text)` | `ThisItem.Champ` |
| DateTime | `Champ: DateTimeValue(...) ou Now() / Today() | `Text(ThisItem.Champ, format)` |
| Personne/Grp | `Champ: {Claims, DisplayName, Email}` | `.DisplayName / .Email |
| Lookup SP natif | `Champ: {Id: Selected.ID, Value: Selected.Title}` | `.Value .Id` |

#### C. C. Filtrage session Poste=varQuart
- **TOUTES galleries + KPI CountRows **doivent** filtrer transactionnels sur Poste = varQuart + date du jour.

Exception: listes master (Ref_Cantons, Ref_Acteurs)

#### D. Audit colonnes systématiques Agent/Poste/DateSaisie
Tout Patch transactionnel contient:
```
Agent: User().FullName
Poste: varQuart
DateSaisie: Now()
```

Selon backend type: `Agent` texte simple. Si backend déclaré Person: `Agent: {Claims:...}`.

#### E. Navigation
Retirer toute référence à `*Ecran_backup` ou `Titre` dans Navigate(... backup`.

#### F. Patch Defaults(...) en création.
Jamais `Patch(Filter(...), Defaults(...)) invalide Power Fx.

#### G. ComboBox DisplayFields/SearchFields existent réellement.
Jamais `ComplianceAssetId` ou `Title` ou `Value` selon la source.

#### H. Guard clause choix backend valeur exacte
Valeurs` choix doivent correspondre choix backend exactes: Division1/2/3, non "Div 3" ; LTV Statut_LTV = Imposée (Active) / Supprimée (Levée) ; Incidents Etat En cours / Traitée / Consolidée.

## Utilisation
```
# Audit sans altération:
python skills/powerapps-backend-alignment/scripts/audit_frontend.py \
  --schemas "Backend/schemas_export/*.json" \
  --context "Backend/contextBD.md" \
  --yamls "Concept pages/**/*.yaml" \
  --report Backend/rapport_alignement.json

# Audit + correction automatique safe renommages
python skills/powerapps-backend-alignment/scripts/audit_frontend.py \
  --apply-safe-fixes \
  --schemas "Backend/schemas_export/*.json" \
  --yamls "Concept pages/**/*.yaml"
```

## Workflow global projet PERMANANCE EQUIPEMENT

1. Récupération schema réel (`sharepoint-graph-schema`)
2. Extrait PDF spec → colonnes reference
3. MAJ Backend/contextBD.md si divergence schéma
4. Audit frontend/backend via ce skill
5. Correction manuelle sur rapports divergents
6. Test import YAML dans Power Apps Studio
7. Publication + test métier
8. Clôture ticket.

## Rapport final
JSON structured:
{
  "audit_id": "...",
  "date": "...",
  "listes_verifiees": [...],
  "ecrans_yaml": [...],
  "erreurs": [
    {"file: "...", "severity": "BLOquant | WARN | INFO",
     "type": "COLUMN_NAME_INVALID | TYPE_MISMATCH | MISSING_AUDIT_COLUMN | NO_POSTE_FILTER | CHOICE_VALUE_MISSING | BACKUP_NAV | BAD_PATCH_SYNTAX",
     "details": "...", "line: "..." }
  ],
  "compteurs": {"total_checks": X, "erreurs": N, "warnings": M}
}
