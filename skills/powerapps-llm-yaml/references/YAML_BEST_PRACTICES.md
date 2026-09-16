# YAML BEST PRACTICES - Power Apps Canvas

S'applique aux écrans YAML PERMANENCE EQUIPEMENT.
Format importable depuis ou exportable vers `PERMANENCE EQUIPEMENT.msapp`.

## 1. Structure fichier YAML

```yaml
Ecran1:
  Properties:
    Fill: =RGBA(255, 255, 255, 1)
    OnVisible: =Set(varX, 1); Refresh(Liste)
  Children:
    - RootContainer:
        Control: ScreenContainer@1.x.x
        Children:
          - ChildControl:
              Control: Classic/Button@2.2.0
              Properties:
                Text: =X
                OnSelect: =Navigate(Y, ScreenTransition.Fade)
              Children: []
```

## 2. Formules multilignes - OBLIGATOIRE bloc `|-`

Formule contenant `: ` (double-point espace), ou guillemets, ou plusieurs lignes → toujours YAML literal block `|-`:

MAUVAIS:
```yaml
Text: =If(Poste="P1", "06-14", "14-22")
```

BON:
```yaml
Text: |-
  =If(
      Poste="P1", "06-14",
      Poste="P2", "14-22",
      "22-06"
  )
```

Règle simple: SI formule contient `:` + espace OU plus de 160 caractères → `|-`.

## 3. Versions contrôles (minimiser surprises)

Respecter versions des YAMLs existants projet:
- ScreenContainer@1.4.0
- GroupContainer@1.5.0
- Classic/Button@2.2.0
- Label@2.5.1
- Gallery@2.15.0 Variant BrowseLayout_Vertical_TwoTextOneImageVariant_ver5.0
- Classic/ComboBox@2.4.0
- Classic/Radio@2.3.0
- Classic/Icon@2.5.0
- Classic/TextInput@2.2.0
- TextInput@2.3.0

## 4. Contrôles hauteurs fixes

NEVER mélanger `Height = Parent.Height` (responsive) sur des enfants dans `Variant: ManualLayout`. ManualLayout → coordonnées X/Y absolues et H/W fixes.

Vérifier débordements:
- FormPanel Height = 30 + max(Y + Height) des enfants
- Workspace Height = 30 + max(Y + Height) des panels
- Boutons finaux Y = Workspace Y + Workspace Height + 20 buffer

## 5. ComboBox Items / SearchFields / DisplayFields

Pour liste SharePoint backend source:
- `Items: Choices(Liste.Colonne)` SI type Choix; OU
- `Items: SortByColumns(Ref_Cantons, "Title", SortOrder.Ascending)` (lists)
- `DisplayFields: ["Title"]` ou `["Value"]`
- `SearchFields: ["Title"]` ou `["Value"]`

JAMAIS `DisplayFields: ["ComplianceAssetId"]` (colonne rare/absente).

## 6. Gallery Items - Filtres & tri

JAMAIS `Items: Tx_Travaux` brute. Toujours filtre session + tri:

```yaml
Items: |-
  =SortByColumns(
      Filter(Tx_Travaux, Poste = varQuart && DateTravaux = Today()),
      "Created",
      SortOrder.Descending
  )
TemplateSize: =72
```

Switch onglet 3 branches:
```yaml
Items: |-
  =Switch(
      varOngletJournal,
      "Travaux", SortByColumns(Filter(Tx_Travaux, Poste=varQuart && DateTravaux=Today()), "Created", SortOrder.Descending),
      "LTV", SortByColumns(Filter(Tx_LTV, Poste=varQuart && ...), "Created", SortOrder.Descending),
      "Incidents", SortByColumns(Filter(Tx_incidents_Ruptures, Poste=varQuart && ...), "Created", SortOrder.Descending)
  )
```

## 7. Patch & Refresh - Ordre

Patch liste → Refresh → Reset → Notify:

```yaml
OnSelect: |-
  =If(
      IsBlank(Champ),
      Notify("Erreur...", NotificationType.Error),
      Patch(Liste, Defaults(Liste), { Champ: Valeur });
      Refresh(Liste);
      Reset(Champ);
      Notify("OK", NotificationType.Success)
  )
```

## 8. Navigation - Vérifier écran existe

Bons noms ecrans projet:
- `PrisePoste_1`
- `JournalDeBord_1`
- `scrFeedback`
- `scrCloture_1`

JAMAIS suffixe `_backup`. JAMAIS `JournalDeBord_1_backup`.

## 9. Variables session partagées

Toujours Set() sur OnVisible AVANT Refresh. Nommage global stable:
- `varQuart` → "P1" | "P2" | "P3"
- `varOngletJournal` → "Travaux" | "LTV" | "Incidents"
- `varFeedbackEvent` → record from Gallery.Selected (Tx_Travaux row)
- `varEtapeCloture` → 1 | 2 | 3 | 4

## 10. Audit final YAML avant commit

Checklist:
- Blocs formule `:`-with-space tous en `|-` ?
- Tous les `ThisItem.` ont nom champ valide ? (jamais `ThisItem.` sans champ)
- `.Value` sur Choice en lecture, `{Value:}` en écriture ?
- Colonne Title/Titre cohérent avec Title ?
- Reset + Refresh après Patch ?
- Navigate cibles valides ?
- Pas de colonnes inventées (absentes Backend/contextBD.md) ?
- Galerie Items Filter Poste=varQuart + date condition ?
- H/W panel suffisant, aucun contrôle hors bords ?
