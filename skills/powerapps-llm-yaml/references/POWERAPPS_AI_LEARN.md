# POWERAPPS AI LEARN - Connaissances Microsoft officielles consolidées

Source: Microsoft Learn Power Apps, SharePoint connector, Power Fx.
Projet: PERMANANCE EQUIPEMENT.

## 1. Connecteur SharePoint - Types colonne vs Power Fx

| Type SharePoint | Lecture Power Fx | Ecriture Patch Power Fx |
| --- | --- | --- |
| Texte simple | `ThisItem.TitreChamp` | `Champ: "valeur texte"` |
| Number / Nombre | `ThisItem.Nb` | `Champ: Value(TextInput.Text)` |
| DateHeure | `Text(ThisItem.Date, "dd/mm/yyyy hh:mm")` | `Champ: DateTimeValue(TextInput.Text)` ou `Today()` ou `Now()` |
| Choix single | `ThisItem.MonChoix.Value` | `MonChoix: {Value: "Ma Valeur"}` |
| Choix multi | `ForAll(ThisItem.MesChoix, Value)` | `MesChoix: ForAll(ComboBox.SelectedItems, {Value: Value})` |
| Personne / Groupe | `ThisItem.Agent.DisplayName`, `.Email`, `.Claims` | `Agent: {Claims:"i:0#.f|membership|...", Email, DisplayName, Department, JobTitle}` |
| Lookup SP natif | `ThisItem.Cant.LookupValue` | `Cant: {Id: NumericId, Value: "Label"}` |
| Hyperlink | `ThisItem.Url.Url` et `ThisItem.Url.Description` | `Url: {Url: "...", Description: "..."}` |
| Oui/Non boolean | `ThisItem.Actif` (bool) | `Actif: true` |

## 2. Règles de délégation SharePoint (évite les délégations warning 500-2000 items)
- Support délégué: `Filter`, `SortByColumns`, `StartsWith`, `=`, `<`, `>`, `And`, `Or`, `Search` sur colonnes indexées
- NON délègue PAS: `CountRows(Filter(...))` sur listes > seuil → use SharePoint views ou pre-filter sur index.
- NON délègue PAS: `DateValue(Text(...))` peut casser delegation → préférer bornes: `Date >= Today() && Date < DateAdd(Today(), 1, TimeUnit.Days)` pour day-filter.

## 3. Patch Defaults vs Base

Syntaxe création:
```powerfx
Patch(ListeSP, Defaults(ListeSP), {Champ: valeur})
```

Syntaxe mise à jour enregistrement existant:
```powerfx
Patch(ListeSP, LookUp(ListeSP, ID = varId), {Champ: nouvelleValeur})
```

ATTENTION: 1er argument Patch = toujours la liste SEUL. Jamais `Patch(Filter(...), Defaults(...), {...})` invalide.

## 4. Reset formulaire multi-étapes + variables globales

```powerfx
Set(varQuart, "P1")
Set(varOngletJournal, "Travaux")
Switch(varOngletJournal, "Travaux", Patch(...), "LTV", Patch(...), Patch(...))
Navigate(scrFeedback, ScreenTransition.Fade
Navigate retour: Navigate(JournalDeBord_1, ScreenTransition.Fade)
```

Vider formulaire: `Reset(TextInput1); Reset(ComboBox1); ResetForm(Form1)`

## 5. Choix cascade - SharePoint

### items: `Choices(Liste.Colonne)` donne options backend direct sans hardcoded.

Exemple cascade Division → Canton:
```powerfx
// Division ComboBox.Items: Choices(Ref_Cantons.Division)
// Canton ComboBox.Items: Filter(Ref_Cantons, Division.Value = DivisionCmb.Selected.Value)
```

## 6. Erreurs Power Fx fréquentes

| Symptôme | Cause | Correctif |
| --- | --- | --- |
| Nom colonne introuvable | casse/accent/espace trailing dans `Colonne ` vs `Colonne` | utiliser noms exacts Backend/contextBD.md + test dans studio Power Apps |
| Type incompatibilité Record vs Texte | `{Value:...}` obligatoire pour Choix | écrire selon type SP colonne |
| YamlInvalidSyntax PA1001 | `:` milieu formule scalaire `Text: =If(X=1,"ok","non": "bad"` | entourer formule multiligne `|-` YAML |
| Expected Boolean | `If(IsBlank(...), "Erreur", Patch(...))` OK | Attention type O/N on Radio Items = `Choices(Tx_Feedbacks.StatutContact)` au lieu `["OUI","NON"]` |

## 7. OnVisible patterns par écran

### PrisePoste_1:
```powerfx
Set(varQuart, "P1");
Refresh(Ref_Cantons);
Refresh(Ref_Acteurs);
Refresh(Tx_Travaux);
Refresh(Tx_LTV);
Refresh(Tx_incidents_Ruptures);
Refresh(Tx_Feedbacks);
```

### JournalDeBord_1:
```powerfx
Set(varOngletJournal, "Travaux");
Refresh(Ref_Cantons); Refresh(Tx_Travaux);
```

### scrFeedback:
```powerfx
If(!IsBlank(varFeedbackEvent), Reset(EventSelector))
```

### scrCloture_1:
```powerfx
Set(varEtapeCloture, 1);
Refresh(Tx_Travaux); Refresh(Tx_LTV); Refresh(Tx_incidents_Ruptures); Refresh(Tx_Feedbacks);
```
