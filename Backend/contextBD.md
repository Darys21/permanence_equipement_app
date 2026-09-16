# Schéma backend PERMANANCE EQUIPEMENT - 6 listes SharePoint (Source: Graph API EXPORT REEL 2026-09-08)

Source autoritaire: exports Graph API dans `Backend/schemas_export/*.json`.
Ce document = vérité pour colonnes internes, types, relations, patch frontend YAML.
Valeurs `name` (nom interne SharePoint) = ceux à utiliser DANS LES YAML Power Apps (jamais displayName pour `ThisItem.<name>` ou `Patch(..., { name: value })`).

---

## 0. Schéma relationnel entité-relation (ER) / relations 1-N

```mermaid
erDiagram
    Ref_Cantons {
        number PK_d_but PK
        number PK_fin
        choice Division
        text Title "Nom canton affiche"
    }
    Ref_Acteurs {
        text Title "Nom / Prenom acteur"
        text Fonction
    }
    Tx_Travaux {
        datetime Datetravaux "Date travaux (Name interne: Datetravaux)"
        number CantonID FK
        choice R_gimetravaux "Regime_travaux interne url encode"
        number ActeurID FK
        datetime Heure_demande
        datetime Heure_Fin_Prevue
        datetime Heures_Autorisee "PLURIEL interne"
        datetime Heure_engagement
        datetime Heures_Degagement "PLURIEL interne"
        datetime Heures_Voie_Retablie "PLURIEL interne"
        text Motif_Engagement
        text Motifs_Engagement_Tardif "PLURIEL interne"
        text Motif_Degagement_Tardif
        number PK_Debut
        number PK_Fin
        choice Poste "CHOIX P1|P2|P3"
        person AgentSaisie
        datetime DateSaisie
    }
    Tx_Feedbacks {
        number TravailID FK "1 Tx_Travaux -> N Feedbacks"
        datetime HeureContact
        choice MoyenCom
        boolean StatutContact
        text Commentaire
        choice Poste
        person AgentSaisie
        datetime DateSaisie
    }
    Tx_incidents_Ruptures {
        datetime DateIncident
        lookup CantonID0 FK "CANTON LOOKUP NATIF SharePoint -> Ref_Cantons Title"
        text PK
        choice Localisation_Type
        datetime Heure_D_but
        datetime Heure_Fin
        choice Etat
        text Commentaires
        choice Poste
        person AgentSaisie
        datetime DateSaisie
    }
    Tx_LTV {
        text Motif_Ralentissement
        lookup CantonID_ FK "LOOKUP NATIF Ref_Cantons Title"
        number PK_Debut
        number PK_Fin
        number Taux
        lookup ActeurID0 FK "LOOKUP NATIF Ref_Acteurs ID"
        choice Statut_LTV "CHOIX Imposée|Supprimée"
        datetime Date_imposition
        datetime Date_Suppression
        choice Poste
        person AgentSaisie
        datetime DateSaisie
    }

    Ref_Cantons ||--o{ Tx_Travaux : "CantonID Nombre simple"
    Ref_Acteurs ||--o{ Tx_Travaux : "ActeurID Nombre simple"
    Tx_Travaux ||--o{ Tx_Feedbacks : "TravailID Nombre simple"
    Ref_Cantons ||--o{ Tx_incidents_Ruptures : "CantonID0 Lookup natif"
    Ref_Cantons ||--o{ Tx_LTV : "CantonID_ Lookup natif"
    Ref_Acteurs ||--o{ Tx_LTV : "ActeurID0 Lookup natif"
```

---

## 1. Ref_Cantons (master data - divisions cantons / PK géographiques)

| Nom interne (`name`) | Affichage | Type SP | Oblig | Détails |
|---|---|---|---|---|
| `Title` | Titre / Nom canton | Texte 255 | Non | Libellé canton affiché Power Apps (LookUp par ID) |
| `Division` | Division | **Choix** | **OUI** | **Valeurs: Division 1, Division 2, Division 3** |
| `PK_d_x00e9_but` | PK_Debut | Nombre | **OUI** | Unicode encode é = `d_x00e9_but`. Utiliser **seulement `PK_d_x00e9_but` en code Power Apps** |
| `PK_fin` | PK_Fin | Nombre | **OUI** | PK fin canton |

**Note front-end:** En lecture Power Apps, `ThisItem.PK_d_x00e9_but` renvoie la valeur numérique. Patch création: `Patch(Ref_Cantons, Defaults(Ref_Cantons), { Title: ..., Division: {Value: "Division 1"}, PK_d_x00e9_but: 123, PK_fin: 456 })`.

---

## 2. Ref_Acteurs (master data - acteurs terrain)

| Nom interne | Affichage | Type SP | Oblig | Détails |
|---|---|---|---|---|
| `Title` | Titre / Nom | Texte 255 | Non | Nom/prénom acteur |
| `Fonction` | Fonction | Texte 255 | **OUI** | Rôle acteur (ex: Responsable maintenance, Conducteur travaux, ...) |

---

## 3. Tx_Travaux (transactionnel - chantiers & interventions)

### Liste 26 colonnes. Règles type colonne POWER APPS 100%:

| Nom interne (`name`) | Affichage | Type SharePoint | Obligatoire | Syntaxe lecture Power Apps / Valeurs | Syntaxe écriture Patch() |
|---|---|---|---|---|---|
| `Title` | Titre chantier | Texte | **OUI** | `ThisItem.Title` | `Title: "Chantier - " & Text(Now(),"yyyymmdd-hhmm")` |
| `Datetravaux` | Date_travaux | **DateTime** standard dateTime | **OUI** default Today() | `Text(ThisItem.Datetravaux, "dd/mm/yyyy")` | `Datetravaux: Today()` |
| `CantonID` | CantonID (trailing espace display: `"CantonID "`) | **Number** simple | **OUI** | `LookUp(Ref_Cantons, ID = ThisItem.CantonID).Title` | `CantonID: CantonInput.Selected.ID` |
| `R_x00e9_gimetravaux` | Regime_travaux | **Choix** dropdown | Non | `ThisItem.R_x00e9_gimetravaux.Value` | `R_x00e9_gimetravaux: {Value: RegimeInput.Selected.Value}` |
| `ActeurID` | ActeurID | **Number** simple | Non | `LookUp(Ref_Acteurs, ID = ThisItem.ActeurID).Title` | `ActeurID: ActorInput.Selected.ID` |
| `Heure_demande` | Heure_demande | DateTime | Non | `Text(ThisItem.Heure_demande, "hh:mm")` | `Heure_demande: IfError(DateTimeValue(RequestInput.Text), Blank())` |
| `Heure_Fin_Prevue` | Heure_Fin_Prevue | DateTime | Non | même format | `Heure_Fin_Prevue: IfError(DateTimeValue(...), Blank())` |
| `Heures_Autorisee` | Heures_Autorisee | **DateTime PLURIEL** | Non | **ATTENTION `Heures_` pluriel interne** | `Heures_Autorisee: IfError(DateTimeValue(...), Blank())` |
| `Heure_engagement` | Heure_engagement | DateTime | Non | singulier | `Heure_engagement: DateTimeValue(...)` |
| `Heures_Degagement` | Heures_Degagement | DateTime PLURIEL | Non | **ATTENTION pluriel interne Heures_D** | `Heures_Degagement: IfError(...)` |
| `Heures_Voie_Retablie` | Heures_Voie_Retablie | DateTime PLURIEL | Non | **pluriel interne** | `Heures_Voie_Retablie: IfError(...)` |
| `Motif_Engagement` | Motif_Engagement | Texte 255 | Non | direct | `Motif_Engagement: TextInput.Text` |
| `Motifs_Engagement_Tardif` | Motifs_Engagement_Tardif | Texte 255 | Non | **ATTENTION Motifs pluriel interne** | `Motifs_Engagement_Tardif: TextInput.Text` |
| `Motif_Degagement_Tardif` | Motif_Degagement_Tardif | Texte 255 | Non | singulier Motif | `Motif_Degagement_Tardif: TextInput.Text` |
| `PK_Debut` | PK_Debut | Nombre | Non | numeric | `PK_Debut: IfError(Value(PKDebutInput.Text), Blank())` |
| `PK_Fin` | PK_Fin | Nombre | Non | numeric | `PK_Fin: IfError(Value(PKFinInput.Text), Blank())` |
| `Poste` | Poste | **CHOIX** OUI | **OUI** | `ThisItem.Poste.Value`  **IMPORTANT: PAS Texte!** | `Poste: {Value: varQuart}` |
| `AgentSaisie` | AgentSaisie | **PERSONNE/GROUPE (peopleOnly)** | **OUI** | `ThisItem.AgentSaisie.DisplayName` `.Email` | `AgentSaisie: {Claims:"i:0#.f|membership|" & Lower(User().Email), Email:User().Email, DisplayName:User().FullName, Department:"", JobTitle:"", Picture:""}` |
| `DateSaisie` | DateSaisie | DateTime | **OUI** | direct | `DateSaisie: Now()` |

### Valeurs Regime_travaux exactes backend:
`TSDL | VI | DIG | CAT A | CAT B | CAT C | CAT D | ATTACHEMENT`

### Ordre temporel à valider US2.3 (Power Fx guard):
```powerfx
If(
    DateTimeValue(RequestInput.Text) > DateTimeValue(AuthInput.Text)
    || DateTimeValue(AuthInput.Text) > DateTimeValue(EngagInput.Text),
    Notify("Ordre temporel invalide: Demande ≤ Autorisee ≤ Engagement", NotificationType.Error),
    Patch(...)
)
```

---

## 4. Tx_Feedbacks (transactionnel - suivi contact acteur après intervention)

| Nom interne | Affichage | Type SP | Oblig | Syntaxe |
|---|---|---|---|---|
| `Title` | Titre | Texte | Non | `Title: "Feedback #" & Text(Now(), "hhmmss")` |
| `TravailID` | TravailID | **Number FK** | **OUI** | `TravailID: varFeedbackEvent.ID` (clé primaire Tx_Travaux) |
| `HeureContact` | HeureContact | DateTime | **OUI** | `HeureContact: Now()` ou DateTimeValue |
| `MoyenCom` | MoyenCom | **Choix** | **OUI** | Valeurs backend: `Whatsapp | Telephone | Thuraya | Thuraya + Telephone`. Patch: `MoyenCom: {Value: Moyen.Selected.Value}` |
| `StatutContact` | StatutContact | **BOOLEAN (pas Choix!)** | Non | Default `true`. Patch: `StatutContact: (ContactStatusRadio.Selected.Value = "OUI")` |
| `Commentaire` | Commentaire | Texte multiligne | Non | `Commentaire: TextInput.Text` |
| `Poste` | Poste | **CHOIX** P1/P2/P3 | **OUI** | **Pas Texte!** `Poste: {Value: varQuart}` |
| `AgentSaisie` | AgentSaisie | **PERSONNE** | **OUI** | record Claims format identique Tx_Travaux |
| `DateSaisie` | DateSaisie | DateTime | Non | `DateSaisie: Now()` |
| `NumeroContact` | NumeroContact | Number | Non | (colonne additionnelle, peut rester vierge) |
| `PK` | PK | Texte 255 | Non | (info rapporteur; pas FK) |

**Alerte divergence front historique!** Ancien YAML: `StatutContact = {Value: ContactStatus.Selected.Value}` → FAUX. StatutContact = Boolean backend réel. Ecrire comparaison = true/false.

---

## 5. Tx_incidents_Ruptures (transactionnel - incidents voie / ruptures géométrie)

| Nom interne | Affichage | Type SP | Oblig | Détails / Syntaxe |
|---|---|---|---|---|
| `Title` | Titre | Texte | Non | `Title: "INCIDENT - " & Text(Now(),"ddmm-hhmm")` |
| `DateIncident` | DateIncident | DateTime dateOnly | Non | `DateIncident: Today()` |
| `PK` | PK | Texte 255 | Non | texte libre PK repérage |
| `Localisation_Type` | Localisation_Type | **Choix** | Non | Valeurs: `Pleinne barre/FD | Pleinne barre/FG | Voie directe en garre` |
| `Heure_D_x00e9_but` | Heure_Début | DateTime | Non | **Nom interne avec é encodé `D_x00e9_but`!** `Heure_D_x00e9_but: DateTimeValue(...)` |
| `Heure_Fin` | Heure_Fin | DateTime | Non | simple |
| `Etat` | Etat | **Choix** | Non | **Tri: 1. Consolidée 2. Traitée 3. En cours** |
| `Commentaires` | Commentaires | Texte 255 | Non | simple |
| `CantonID0` | CantonID | **LOOKUP NATIF SharePoint → Ref_Cantons Title** | Non | **ATTENTION NOM INTERNE CantonID0** (pas CantonID). Lecture: `ThisItem.CantonID0.Value`. Patch: `CantonID0: {Id: CantonInput.Selected.ID, Value: CantonInput.Selected.Title}` |
| `Poste` | Poste | CHOIX P1/P2/P3 | Non | **Choix**. `Poste: {Value: varQuart}` |
| `AgentSaisie` | AgentSaisie | PERSONNE | Non | record Claims comme Tx_Travaux |
| `DateSaisie` | DateSaisie | DateTime | Non | `Now()` |

---

## 6. Tx_LTV (transactionnel - limitations temporaires vitesse)

| Nom interne | Affichage | Type SP | Oblig | Syntaxe Patch / Lecture |
|---|---|---|---|---|
| `Title` | Titre | Texte | Non | string |
| `Motif_Ralentissement` | Motif_Ralentissement | Texte 255 | Non | string |
| `PK_Debut` | PK_Debut | Nombre | Non | numeric |
| `PK_Fin` | PK_Fin | Nombre | Non | numeric |
| `Taux` | Taux (km/h) | Nombre | Non | numeric (ex: 30, 60, 80) |
| `Statut_LTV` | Statut_LTV | **Choix** | Non | **Valeurs backend: Imposée / Supprimée (SANS suffixe!).** `ThisItem.Statut_LTV.Value`. Patch: `Statut_LTV: {Value: "Imposée"}` |
| `Date_imposition` | Date_imposition | DateTime | Non | minuscule `i` |
| `Date_Suppression` | Date_Suppression | DateTime | Non | S majuscule |
| `CantonID_` | CantonID | **LOOKUP NATIF → Ref_Cantons Title** | Non | **Nom interne underscore suffix `CantonID_`!** Patch: `CantonID_: {Id: CantonInput.Selected.ID, Value: CantonInput.Selected.Title}` |
| `ActeurID0` | ActeurID | **LOOKUP NATIF → Ref_Acteurs ID** | Non | **Nom interne suffix zéro `ActeurID0`!** Patch: `ActeurID0: {Id: ActorInput.Selected.ID, Value: ActorInput.Selected.Title}` |
| `Poste` | Poste | CHOIX P1/P2/P3 | Non | **Choix** `Poste: {Value: varQuart}` |
| `AgentSaisie` | AgentSaisie | PERSONNE | Non | Claims record |
| `DateSaisie` | DateSaisie | DateTime | Non | `Now()` |

**Alerte historique front!**
Anciens YAML utilisaient `Statut_LTV.Value = "Imposée (Active)"`. Backend réel: `"Imposée"` SANS parenthèses. → Corriger filtre gallery LTV actif: `Filter(Tx_LTV, Statut_LTV.Value = "Imposée")`.

---

## 7. Navigation & variables session partagées entre 4 écrans Power Apps

```mermaid
flowchart LR
    A[PrisePoste_1  -->|Set varQuart P1|P2|P3| B]
    A -->|OnSelect bouton Commencer quart| B(JournalDeBord_1)
    B -->|Set varOngletJournal Travaux|LTV|Incidents| B
    B -->|Clic icône message ligne Travaux + Set varFeedbackEvent| C(scrFeedback)
    B -->|OnSelect 'Feedback history' onglet| C
    B -->|OnSelect 'Clôturer quart'| D(scrCloture_1)
    C -->|Back Navigate| B
    D -->|Validation etape 4 + Navigate final| A
```

### Variables globales session et périmètre:

| Nom variable | Valeurs possibles | Écran défini | Utilisé dans |
|---|---|---|---|
| `varQuart` | `"P1" \| "P2" \| "P3"` | PrisePoste_1 (bouton SelectP1 etc.) | **TOUS 4 écrans**, filtre galleries Poste.Value = varQuart, colonne audit Poste {Value: varQuart} |
| `varOngletJournal` | `"Travaux" \| "LTV" \| "Incidents"` | JournalDeBord_1 (Onglet TabOnSelect) | Journal FormPanel visible branches, Switch SaveButton Patch 3 branches, Switch EventsGallery Items 3 listes, Switch EventCount CountRows 3 KPIs |
| `varFeedbackEvent` | Record complet ligne Tx_Travaux | JournalDeBord_1 Icon.OnSelect scrFeedback target | scrFeedback Default EventSelector ComboBox, lblEventCtxt Titre/Date canton, TravailID Patch Feedbacks = `varFeedbackEvent.ID` |
| `varEtapeCloture` | `1 \| 2 \| 3 \| 4` | scrCloture_1 OnVisible et Buttons étape 1-2-3-4 | SummaryPanel.Visible, ClosurePanel.Visible |

### Comportement filtres galleries obligatoires
Toutes galleries transactionnelles ET CountRows KPI doivent filtrer:
1. Filtre session quart:
```powerfx
// Poste est CHOIX dans TOUTES listes transactionnelles: donc .Value obligatoire!
Filter(Tx_Travaux, Poste.Value = varQuart && Datetravaux = Today())
Filter(Tx_LTV, Poste.Value = varQuart && Statut_LTV.Value = "Imposée")
Filter(Tx_incidents_Ruptures, Poste.Value = varQuart && DateIncident = Today())
Filter(Tx_Feedbacks, Poste.Value = varQuart && TravailID = varFeedbackEvent.ID)
```
2. Pas `.Value` → erreur runtime Power Apps incompatible type record vs texte.

### Patch minimaliste transaction - syntaxe colonne audit PERSONNE
**OBLIGATOIRE pour AgentSaisie (type personOrGroup backend):**
```powerfx
AgentSaisie: {
    Claims: "i:0#.f|membership|" & Lower(User().Email),
    Email: User().Email,
    DisplayName: User().FullName,
    Department: "",
    JobTitle: "",
    Picture: ""
}
```
Poste + Audit 3 colonnes (si rattachée à la création objet transactionnel) toujours ensemble:
```powerfx
{
    ... champs metier ...,
    Poste: {Value: varQuart},
    AgentSaisie: {Claims:"i:0#.f|membership|" & Lower(User().Email), Email:User().Email, DisplayName:User().FullName, Department:"", JobTitle:"", Picture:""},
    DateSaisie: Now()
}
```

---

## 8. Comparatif divergence critiques - Frontend (YAML historique) VERSUS Backend réel Graph

| Concept | Valeur historique YAML hypothèse | **Backend réel export Graph** | Correctif à appliquer |
|---|---|---|---|
| `DateTravaux` (sans underscore) Tx_Travaux | `DateTravaux: Today()` | **`Datetravaux` (un mot, t minuscule, pas underscore)** | Remplacer `DateTravaux` → `Datetravaux` dans toutes références |
| CantonID Incidents | `CantonID: Selected.ID` (number) | **`CantonID0` Lookup natif {Id,Value}** | `CantonID0: {Id: Selected.ID, Value: Selected.Title}` |
| CantonID LTV | `CantonID: Selected.ID` (number) | **`CantonID_` Lookup natif {Id,Value} suffix _** | `CantonID_: {Id: Selected.ID, Value: Selected.Title}` |
| ActeurID LTV | `ActeurID: Selected.ID` (number) | **`ActeurID0` Lookup natif {Id,Value} suffix 0** | `ActeurID0: {Id: Selected.ID, Value: Selected.Title}` |
| Poste colonne type | `Poste = varQuart` (texte) | **`Poste` = CHOIX P1/P2/P3 dans TOUTES listes!** | `Poste: {Value: varQuart}` en écriture; `.Value` en lecture/gallery/Filter |
| AgentSaisie colonne type | `Agent: User().FullName` (texte) | **`AgentSaisie` type PERSONNE claims record** | Écrire record Claims format i:0#.f|membership + DisplayName/Email |
| Heure autorisée colonne | `Heure_Autorisee` singulier | **`Heures_Autorisee` PLURIEL** | Corriger Heure_ → Heures_ (A, D, V) |
| Heure dégagement colonne | `Heure_Degagement` singulier | **`Heures_Degagement` PLURIEL** | Heures_Degagement partout |
| Heure voie rétablie | `Heure_Voie_Retablie` singulier | **`Heures_Voie_Retablie` PLURIEL** | Heures_Voie_Retablie partout |
| Motif engagement tardif Tx_Travaux | `Motif_Engagement_Tardif` singulier | **`Motifs_Engagement_Tardif` PLURIEL** | Motifs_ avec s |
| Régime travaux colonne | `RegimeTravaux` ou `Régime_travaux` (accent) | **`R_x00e9_gimetravaux`** (é unicode interne) | Référencer `R_x00e9_gimetravaux` .Value en lecture |
| StatutContact Tx_Feedbacks type | `{Value: "OUI"}` (Choix) | **BOOLEAN** type 0/1 true/false! | `StatutContact: (RadioSelected = "OUI")` booléen |
| Statut_LTV LTV | `"Imposée (Active)"` / `"Supprimée (Levée)"` | **Valeurs simples: `Imposée` / `Supprimée`** | Filtrer galleries `.Value = "Imposée"` et patch `{Value: "Imposée"}` |
| Heure début Incidents | `Heure_Debut` (é) | **`Heure_D_x00e9_but` (é encodé)** | `Heure_D_x00e9_but` nom interne partout |
| PK début Ref_Cantons | `PK_Debut` | **`PK_d_x00e9_but`** é minuscule encodé | `PK_d_x00e9_but` en code Power Apps |
| Date imposition LTV | `Date_Imposition` I majuscule | **`Date_imposition` i minuscule** | Corriger casse i |
| Localisation Incidents Etat defaut | `"En cours" / "Traitée" / "Consolidée"` alpha | **Ordre backend stocké: Consolidée, Traitée, En cours** (tri default liste non alphabétique) | Conserver ordre UI user friendly mais backend enregistre choice value exacte string |
| MoyenCom Feedback Valeurs | `WhatsApp / Phone / Thuraya / Sur place` | **Backend réel: Whatsapp \| Telephone \| Thuraya \| Thuraya + Telephone** | Items ComboBox = Choices(Tx_Feedbacks.MoyenCom) ; retirer "Sur place" non référencé backend |

---

## 9. Exemples Patch complet 100% conforme backend réel Graph

### Exemple A. Patch Tx_Travaux (chantier)
```powerfx
Patch(
    Tx_Travaux,
    Defaults(Tx_Travaux),
    {
        Title: "Chantier - " & Text(Now(), "yyyymmdd-hhmm"),
        Datetravaux: Today(),
        CantonID: CantonInput_1.Selected.ID,
        R_x00e9_gimetravaux: {Value: RegimeInput_1.Selected.Value},
        ActeurID: ActorInput_1.Selected.ID,
        Heure_demande: IfError(DateTimeValue(RequestInput_1.Text), Blank()),
        Heure_Fin_Prevue: IfError(DateTimeValue(FinPrevueInput_1.Text), Blank()),
        Heures_Autorisee: IfError(DateTimeValue(AuthorizationInput_1.Text), Blank()),
        Heure_engagement: IfError(DateTimeValue(EngagementInput_1.Text), Blank()),
        Heures_Degagement: IfError(DateTimeValue(DegagementInput_1.Text), Blank()),
        Heures_Voie_Retablie: IfError(DateTimeValue(VoieRetablieInput_1.Text), Blank()),
        PK_Debut: IfError(Value(PKDebutInput_1.Text), Blank()),
        PK_Fin: IfError(Value(PKFinInput_1.Text), Blank()),
        Motif_Engagement: MotifEngagementInput_1.Text,
        Motifs_Engagement_Tardif: MotifEngTardifInput_1.Text,
        Motif_Degagement_Tardif: MotifDegTardifInput_1.Text,
        Poste: {Value: varQuart},
        AgentSaisie: {Claims:"i:0#.f|membership|" & Lower(User().Email), Email:User().Email, DisplayName:User().FullName, Department:"", JobTitle:"", Picture:""},
        DateSaisie: Now()
    }
);
Refresh(Tx_Travaux);
```

### Exemple B. Patch Tx_LTV (limitation)
```powerfx
Patch(
    Tx_LTV,
    Defaults(Tx_LTV),
    {
        Title: "LTV-" & Text(Now(), "yyyymmddhhmm"),
        Motif_Ralentissement: MotifRalInput.Text,
        PK_Debut: IfError(Value(PKDebutLTVInput.Text), Blank()),
        PK_Fin: IfError(Value(PKFinLTVInput.Text), Blank()),
        Taux: IfError(Value(TauxInput.Text), Blank()),
        CantonID_: {Id: CantonLTVInput.Selected.ID, Value: CantonLTVInput.Selected.Title},
        ActeurID0: {Id: ActorLTVInput.Selected.ID, Value: ActorLTVInput.Selected.Title},
        Statut_LTV: {Value: "Imposée"},
        Date_imposition: Now(),
        Poste: {Value: varQuart},
        AgentSaisie: {Claims:"i:0#.f|membership|" & Lower(User().Email), Email:User().Email, DisplayName:User().FullName, Department:"", JobTitle:"", Picture:""},
        DateSaisie: Now()
    }
);
Refresh(Tx_LTV);
```

### Exemple C. Patch Tx_Feedbacks
```powerfx
Patch(
    Tx_Feedbacks,
    Defaults(Tx_Feedbacks),
    {
        Title: "FB#" & Text(Now(), "hhmmss"),
        TravailID: varFeedbackEvent.ID,
        HeureContact: Now(),
        MoyenCom: {Value: ContactMode.Selected.Value},
        StatutContact: (ContactStatusRadio.Selected.Value = "OUI"),
        Commentaire: CommentInput.Text,
        Poste: {Value: varQuart},
        AgentSaisie: {Claims:"i:0#.f|membership|" & Lower(User().Email), Email:User().Email, DisplayName:User().FullName, Department:"", JobTitle:"", Picture:""},
        DateSaisie: Now()
    }
);
Refresh(Tx_Feedbacks);
```

### Exemple D. Patch Tx_incidents_Ruptures
```powerfx
Patch(
    Tx_incidents_Ruptures,
    Defaults(Tx_incidents_Ruptures),
    {
        Title: "INCIDENT-" & Text(Now(), "yyyymmddhhmm"),
        DateIncident: Today(),
        PK: PKIncidentInput.Text,
        Localisation_Type: {Value: LocTypeInput.Selected.Value},
        Heure_D_x00e9_but: IfError(DateTimeValue(HeureDebutIncident.Text), Blank()),
        Heure_Fin: IfError(DateTimeValue(HeureFinIncident.Text), Blank()),
        Etat: {Value: "En cours"},
        Commentaires: CommentIncInput.Text,
        CantonID0: {Id: CantonIncInput.Selected.ID, Value: CantonIncInput.Selected.Title},
        Poste: {Value: varQuart},
        AgentSaisie: {Claims:"i:0#.f|membership|" & Lower(User().Email), Email:User().Email, DisplayName:User().FullName, Department:"", JobTitle:"", Picture:""},
        DateSaisie: Now()
    }
);
Refresh(Tx_incidents_Ruptures);
```

---

## 10. Liens rapides cross-références projet
- Schema exports Graph JSON bruts: `Backend/schemas_export/*.json`
- Skills pour manipulation: `skills/sharepoint-graph-schema/`, `skills/powerapps-backend-alignment/`, `skills/powerapps-llm-yaml/`
- Documentation métier PDF: `Documentation/PERMANANCE EQUIPEMENT.pdf`
- YAMLs écrans: `Concept pages/Ecran */*.yaml`
