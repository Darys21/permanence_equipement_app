# REFERENCES - Audit Colonnes Frontend vs Backend

## Liste des 6 listes

- 2 master data: Ref_Cantons, Ref_Acteurs
- 4 transactionnelles: Tx_Travaux, Tx_Feedbacks, Tx_incidents_Ruptures, Tx_LTV

## Colonnes audit transactionnels systématiques (doivent apparaitre dans chaque Patch)
- `Agent`: User().FullName (ou type Person record Claims/DisplayName/Email selon backend)
- `Poste`: varQuart ("P1"/"P2"/"P3")
- `DateSaisie`: Now()

## Tests types classiques d'erreur frontend

### 1. Erreurs nom colonne
- `Titre` doit toujours être corrigé en `Title`
- `Date_travaux` : vérifier backend, peut-être `DateTravaux`
- `Régime_travaux` accent vs `RegimeTravaux`
- `Heure_demande` vs `Heure_Demande` (casse)
- `Heures_Autorisee` pluriel vs `Heure_Autorisee` singulier
- `Motifs_Engagement_Tardif` vs `Motif_Engagement_Tardif`

### 2. Fausses lecture choix .Value sur Texte
- Si colonne Poste backend = Texte, ERREUR: `Poste.Value = varQuart`
- Si colonne Poste backend = Choix, ERREUR: `Poste = varQuart` (sans Value record)
- Si CantonID backend type lookup natif → `{Id, Value}` attendu, pas simple entier
- Si CantonID backend type nombre → simple entier attendu

### 3. Navigation backup
- JournalDeBord_1_backup → corrigé JournalDeBord_1
- PrisePoste_2 → PrisePoste_1
- Toute Nav cible doit exister dans fichiers YAMLs projet

### 4. Patch syntaxe invalide
- `Patch(Filter(Tx_X, Poste = varQuart), Defaults(Tx_X), {})` → invalide.
- Premier argument Patch = liste seule (ou LookUp record existant pour Update).
- `Patch(Tx_X, Defaults(Tx_X), {...})` SEUL correct en création.

### 5. Écran OnVisible minimum recommandé
`Set(var..., val) ; Refresh(Ref_Cantons) ; Refresh(Tx_Travaux) ; ...`
Pas de Refresh → galleries avec données périmées.

### 6. Galleries sans filtre session (fuite de données postes adjacents)
- `Items: Tx_Travaux` → interdit sans `Filter(Poste = varQuart && Date condition)`
- `CountRows(Tx_X)` → KPI comptage TOTAL hors quart.

### 7. ComboBox champs non existants
Items: Listes existantes.
SearchFields / DisplayFields: colonnes réellement présentes.
Jamais `ComplianceAssetId` (non standard).

### 8. Valeurs Choix inventées
Exemple: `Statut_LTV = {Value: "Active"}` invalide si backend propose `{Value: "Imposée (Active)"}`.
Vérifier 100% de correspondance valeurs string exactes.

## Mapping liste front → backend colonnes typical

### Ecran 1 PrisePoste → listes:
Tx_Travaux (Filtre: IsBlank(Heure_Degagement) = chantiers en cours)
Tx_LTV: Statut_LTV.Value = "Imposée (Active)" = LTV encore actives
Ref_Cantons (lookup nom canton)

### Ecran 2 Journal → listes:
Toutes les 6 listes (2 master lookup + 4 transactionnelles en lecture/écriture)
Master cascades: Division → Canton → ID.

### Ecran 3 Feedback → listes:
Tx_Travaux (sélection événement à pointer)
Tx_Feedbacks (écriture + historique feedback)

### Ecran 4 Clôture → listes:
4 KPIs: Tx_Travaux, Tx_LTV, Tx_incidents_Ruptures, Tx_Feedbacks
Plus galleries détail.
