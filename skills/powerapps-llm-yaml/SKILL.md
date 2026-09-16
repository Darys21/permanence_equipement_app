---
name: powerapps-llm-yaml
description: Génère, audite et corrige des fichiers YAML Power Apps Canvas respectants les conventions du projet (colonnes SharePoint exactes, types Choix, cascade, Patch, filtres Poste, validations).
---

## But
Fournir aux agents LLM une base fiable pour écrire ou mettre à jour des écrans Power Apps Canvas au format YAML, en restant aligné sur le schéma SharePoint backend, les user stories PDF et les conventions de nommage du dépôt PERMANANCE EQUIPEMENT.

## Quand déclencher
- Création d'un nouvel écran Power Apps (.yaml)
- Mise à jour d'un OnSelect SaveButton / Patch / Reset / Refresh
- Ajout d'une colonne frontend (TextBox, ComboBox, Radio, Label, Gallery)
- Modification cascade liste de choix, filtres, OnChange navigation
- Correction erreur PA1001 YamlInvalidSyntax, nom colonne non trouvé, delegation warning
- Vérification cohérence OnVisible, Set variables session, Navigate

## Prérequis ALWAYS
Avant toute modification d'un YAML Power Apps:
1. Lire `Backend/contextBD.md` pour connaître les colonnes et types exacts des 6 listes SP
2. Lire `Documentation/PERMANENCE EQUIPEMENT.pdf` (ou `script/pdf_output.txt`) pour les US
3. Lire `PROJET_ANALYSE.md` sections schémas 6 listes
4. Lire la section RAPPORT_REVUE_POWER_APPS.md pour erreurs corrigeables classiques
5. Vérifier que la navigation cible l'écran EXISTANT (pas `JournalDeBord_1_backup`), vérifier variable `varQuart` / `varOngletJournal` / `varEtapeCloture` / `varFeedbackEvent`

## Règles OBLIGATOIRES
### Nommage colonne
- `Title` jamais `Titre` (colonne SP natif, renommée en UI mais interne = Title)
- Poste: si colonne SP Texte → `Poste = varQuart` ; si Choix → `Poste = {Value: varQuart}` (obéir `contextBD.md`)
- Agent: si colonne Texte → `Agent: User().FullName` ; si Person → utiliser record `{Claims,Email,DisplayName}` selon schema réel
- Types Choix SP en ECRITURE → syntaxe `{Value: <Selected.Value>}`
- Types Choix SP en LECTURE → `.Value` (ex: `Statut_LTV.Value`, `Etat.Value`, `Division.Value`)
- Noms FK: `CantonID`, `ActeurID`, `TravailID` SANS espace ni accent
- Heures 6 Travaux: `Heure_Demande`, `Heure_Fin_Prevue`, `Heure_Autorisee`, `Heure_Engagement`, `Heure_Degagement`, `Heure_Voie_Retablie` ; vérifier pluriel "Heures_" vs singulier selon schema réel (garder 100% ce qui est dans Backend/contextBD.md section 3 Tx_Travaux)

### Patch Power Fx
- Creation utiliser `Defaults(NomListe)` en 2nd argument, JAMAIS `Patch(Filter(...), Defaults(...), {...})`
- Pattern création: `Patch(Liste, Defaults(Liste), {col1:...}); Refresh(Liste); Reset(ctrl1); Reset(ctrl2); Notify(...)`
- Guard clauses: `If(IsBlank(Champ), Notify(Erreur), Patch(...))`
- Date parsing toujours `IfError(DateTimeValue(TextInput.Text), Blank())` ; jamais `DateTimeValue` sans protection
- Nombre: PK `IfError(Value(TextInput.Text), Blank())`
- Audit 3 colonnes systématiquement: `Agent/Poste/DateSaisie` renseignés sur TOUT Patch transactionnel

### Galleries / CountRows
- Filtre session: chaque gallery transactionnelle ET KPI contient `Filter(Tx_X, Poste = varQuart && <date du jour>)`
- Date du jour par type:
  - Tx_Travaux: `DateTravaux = Today()`
  - Tx_incidents_Ruptures: `DateIncident = Today()`
  - Tx_LTV / Tx_Feedbacks: `DateValue(Text(DateSaisie, "dd/mm/yyyy")) = Today()` (car colonne DateHeure)
- Eviter `CountRows(Filter)` sur grands volumes si possible ; accepter mais commenter risque delegation
- LookUp cascade canton: `LookUp(Ref_Cantons, ID = ThisItem.CantonID).Title`
- LookUp acteur: `LookUp(Ref_Acteurs, ID = ThisItem.ActeurID).Title`

### YAML syntaxe Power Apps
- Formules contenant `: `, `"`, ou multilignes → toujours format block YAML `|-`
- Control versions: utiliser versions vues dans YAMLs existants (Classic/Button@2.2.0, Label@2.5.1, Gallery@2.15.0, Classic/ComboBox@2.4.0, Classic/Radio@2.3.0, GroupContainer@1.5.0, Classic/Icon@2.5.0)
- `Navigate(Ecran, ScreenTransition.Fade)` jamais de suffixe backup
- `OnVisible` doit faire `Set(varX, valeur)` puis `Refresh(ToutesListesUtilisees)`

## Structure de contrôle minimum obligatoire sur formulaire
1. OnVisible refresh sources et variables
2. Division ComboBox Items = Choices(Ref_Cantons.Division) (si type Choix backend)
3. Canton ComboBox cascade Filter(Ref_Cantons, Division.Value = DivisionInput.Selected.Value)
4. Label onglet spécifique visible via Switch(varOngletJournal,...)
5. 3 Guard clause validation onglet
6. Patch 3 branches (Switch onglet)
7. Reset tous contrôles Input + Select(Parent)
8. Notify succès

## Vérifications finales OBLIGATOIRES
- Pas de colonnes inventées (non listées Backend/contextBD.md)
- Pas de suffixe backup dans Navigate
- Pas de `Titre` (seulement Title)
- Pas de `Poste.Value` si colonne SP Texte
- Pas de `Date_travaux` / `Régime_travaux` / `Heures_Degagement` / `Date_imposition` non conformes (verifier casse/s dans contextBD.md)
- ComboBox DisplayFields / SearchFields pointent colonnes EXISTANTES Title, Value (jamais ComplianceAssetId)
- Pas de références ThisItem avec `.` cassé genre `ThisItem.` sans champ
- Tous les icônes message d'une ligne Travaux → `Set(varFeedbackEvent, ThisItem); Navigate(scrFeedback)`
- Tout bouton Clôture → passage varEtapeCloture + Navigate final PrisePoste_1

## Exemple workflow typique
1. Utilisateur dit: "Ajouter un champ StatutContact sur Feedback"
2. Lire Backend/contextBD.md colonne Tx_Feedbacks → constater type Choix OUI/NON
3. Modifier Radio Items: `Choices(Tx_Feedbacks.StatutContact)`
4. Modifier Save Patch: `StatutContact: {Value: ContactStatus.Selected.Value}`
5. Ajouter colonne audit Agent/Poste/DateSaisie dans le record Patch
6. Reset(ContactStatus), Refresh(Tx_Feedbacks)
7. Grep global sur `StatutContact`, `Date_travaux`, `Poste.Value` etc pour vérifier zero anomalie subsistante

## Erreurs fréquentes à interdire absolument
- Deviner noms colonnes sans Backend/contextBD.md
- Introduire `Poste = {Value: varQuart}` alors que colonne SP Texte (désynchronisation = patch échouera)
- Oublier `.Value` sur type Choix en lecture ou écriture
- Utiliser record `{Id, Value}` pour CantonID quand c'est type Nombre simple
- Écrire `Choices(Tx_Travaux.Régime_travaux)` avec accent ou casse différent du backend
