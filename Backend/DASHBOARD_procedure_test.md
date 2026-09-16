# PROCÉDURE TEST DASHBOARD JOURNAL DE BORD (JournalDeBord_3)
## Frontend YAML source: `Frontend/Ecran 2 Journal de bord/dashboard.yaml`

Prérequis exécution:
1. Ouvrir Power Apps Studio - Environnement Eramet - App PERMANENCE EQUIPEMENT.msapp
2. Vérifier données connectées: 6 listes SharePoint (Ref_Cantons, Ref_Acteurs, Tx_Travaux, Tx_LTV, Tx_incidents_Ruptures, Tx_Feedbacks)
3. Assurez-vous utilisateur connecté membre du site PERMANANCEEQUIPEMENT SharePoint

---

## ÉTAPES TEST (10 cas)

### CAS 1. Initialisation ouverture écran (OnVisible)
Action: Ouvrir Journal depuis PrisePoste_1 (bouton Commencer quart), avec varQuart="P1".
Résultat attendu:
- Tabs Travaux/LTV/Incidents affichés; Tab Travaux sélectionné
- Dropdown Division listé valeurs "Division 1 / 2 / 3" (provenance Choices(Ref_Cantons.Division))
- Après sélection Division, Dropdown Canton doit afficher SEULEMENT les cantons de cette division

### CAS 2. Validation champs vides Travaux
Action: onglet 1 Travaux vide, cliquer ENREGISTRER LE CHANTIER.
Résultat attendu: Notify erreur rouge "Sélectionnez Division et Canton" (1er niveau); puis si Division/Canton OK mais Régime/Acteur/3 Heures manquantes → "Travaux : renseignez régime, intervenant, 3 heures et vérifiez chronologie".

### CAS 3. Enregistrement Chantier (Tx_Travaux Patch Defaults)
Valeurs:
- Division: Division 1
- Canton: premier canton liste
- Régime de travaux: TSDL (1ère valeur Choix)
- Intervenant: premier Ref_Acteurs liste
- Heure Demande: 08/09/2026 08:00
- Heure Autorisée: 08/09/2026 08:15
- Heure Engagement: 08/09/2026 08:20
- PK Début: 12400, PK Fin: 12850
- (reste facultatif)

Résultat attendu:
- Notify vert "Chantier enregistré dans Tx_Travaux"
- EventCount "N événements" → incrémente +1
- Gallery Journal du quart: ligne nouvellement créée visible, label "Canton : X | 08/09", Statut "En cours" (car Heures_Degagement = Blank)
- Check SharePoint Tx_Travaux en ligne: colonne Datetravaux = Today, Poste = P1, AgentSaisie = User connecté DisplayName correct

### CAS 4. Garde ordre temporel Travaux invalide
Même valeurs CAS 3 mais:
- Demande: 09:00, Autorisée: 08:30, Engagement: 08:00 (ordre inverse)
Résultat attendu: Notify erreur rouge "chronologie (Demande ≤ Autorisée ≤ Engagement)". Patch ne se déclenche PAS.

### CAS 5. Enregistrement LTV (Tx_LTV Patch Lookup)
Onglet 2 LTV / RAL:
- Division + Canton choix comme CAS 3
- Motif ralentissement: "Défaut de géométrie de la voie"
- Intervenant: 2e acteur liste
- PK Début: 14000 / PK Fin: 15500
- Taux: 60
- Date imposition: 08/09/2026 10:00
- (Date suppression: vide → Statut = Imposée)

Résultat attendu:
- Notify LTV enregistrée
- Gallery Jour → nouvelle ligne LTV; détails "Taux : 60 km/h | Canton : Y"; Statut "Imposée"
- SharePoint Tx_LTV colonnes: CantonID_ {Id: Selected.ID, Value: Selected.Title} (record Lookup, pas simple int!), ActeurID0 {Id,Value} record Lookup

### CAS 6. Enregistrement Incident (Tx_incidents_Ruptures)
Onglet 3 Incidents:
- Division + Canton
- Localisation type: Pleinne barre/FD
- PK: 16250
- Date incident: Today
- Heure Début: 11:00
- (Heure fin vide → Etat = En cours)
- Commentaires: "Desserrage boulons"

Résultat attendu:
- Notify Incident enregistré
- Gallery Jour Incidents → Statut "En cours"; détails PK 16250, Canton correct
- SharePoint colonne Heure_D_x00e9_but correctement horodatée; CantonID0 record Lookup; Localisation_Type record Choice

### CAS 7. Statut Contact Feedback icône Message
Action: Dans Gallery Travaux ligne CAS 3 → cliquer icône Message
Résultat attendu: Set(varFeedbackEvent, ThisItem); Navigation scrFeedback écran Feedback ouvert pré-sélectionné.

### CAS 8. Save multiple - Reset forms
Après CAS 3, vérifier: DivisionInput, CantonInput, RegimeInput, ActorInput, PK, Taux, Dates, Heures, Motifs, Commentaires → tous vides (Reset exécutés).

### CAS 9. Vérification colonne Person record AgentSaisie
Aller dans liste Tx_Travaux SharePoint réelle via navigateur, nouvel élément. Vérifier colonne "AgentSaisie" est affichage Personne, valeur = Votre Nom/Prénom.

### CAS 10. Refresh navigation Aller-Retour
Bouton bas gauche "NOUVEAU POINTAGE TERRAIN" → Nav scrFeedback puis retour Back → Journal du quart toujours même données. Bouton bas droite "TERMINER LE POSTE & BILAN →" → Nav scrCloture_1.

---

## CRITÈRES SUCCÈS
- 10/10 cas réussi sans erreurs runtime Power Apps ("incompatible type", "column doesn't exist", "expected record value text", "expected number error")
- 0 lignes SharePoint colonne nulles sur champs obligatoires Poste/AgentSaisie/DateSaisie
- Types respectés : Choice=record{Value}, Lookup=record{Id,Value}, Person=record{Claims/DisplayName/Email/Department/JobTitle/Picture}
- Valeurs Choice exactes backend: Régime TSDL/VI/DIG/CAT A/CAT B/TAC/TAV, Statut_LTV Imposée/Supprimée

## DIVERGENCES FAUX POSITIFS AUDIT ACTUEL (a vérifier manuellement si runtime OK)
Script compare_front_back.py flagge 5 faux positifs sur dashboard (à ignorer car contexte correct):
- Ligne 718: CantonID = Correct! Colonnes Tx_Travaux.CantonID backend = Number simple (Pas Lookup). Seulement Incidents CantonID0 et LTV CantonID_ sont Lookup.
- Ligne 720: ActeurID = Correct! Tx_Travaux.ActeurID backend = Number simple. Seulement LTV ActeurID0 Lookup.
- Lignes 727 & 750: PK_Debut sur Tx_Travaux/Tx_LTV = Columns backend nommées bien PK_Debut Number (nom unicode PK_d_x00e9_but = seulement colonne Ref_Cantons master data)
- Ligne 928: EventDetails Travaux ThisItem.CantonID = Correct! Tx_Travaux canton ID = number simple, donc LookUp(Ref_Cantons, ID = ThisItem.CantonID).Title.
