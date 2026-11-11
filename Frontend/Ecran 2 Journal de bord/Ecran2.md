# Écran — Journal de bord opérationnel

**Écran Power Apps :** `JournalDeBord_3`  
**Source YAML :** `JournalDeBord_3.yaml`  
**Priorité :** critique — fiabilisation CRUD.

## Objectif

Centraliser la saisie, la consultation et la mise à jour des événements opérationnels du poste : travaux, incidents/ruptures et LTV/RAL.

## Organisation visible dans le YAML

L'écran comporte trois espaces fonctionnels :

1. **Chantiers & Travaux**
2. **Incidents & Ruptures**
3. **LTV / RAL (ralentissements)**

Le YAML comprend également des éléments de localisation, des informations sur l'intervenant et le permanent au poste, les heures planifiées et réalisées, des motifs, des commentaires, des filtres/historiques LTV, un accès au pointage terrain et un accès à la clôture du poste.

## Sources de données

- Référentiels : `Ref_Cantons`, `Ref_Acteurs`, `Ref_Permanents`.
- Transactionnel : `Tx_Travaux`, `Tx_LTV`, `Tx_incidents_Ruptures`.
- Feedbacks : `Tx_Feedbacks`.

## Fonctionnalités attendues

### Travaux

- Saisie guidée par division et canton.
- Responsable/intervenant et permanent au poste.
- Informations planifiées : demande, autorisation, fin prévue.
- Informations réalisées : engagement, dégagement, voie rétablie.
- Nature/régime des travaux, PK, motifs et observations.
- Calculs de durée, retards et prolongation lorsque les données le permettent.
- Création, consultation, modification et suppression.

### LTV / RAL

- Localisation canton et PK début/fin.
- Motif de ralentissement et taux en km/h.
- Acteur responsable.
- Statut imposée/supprimée et dates associées.
- Consultation des LTV actives et de l'historique.
- Création, reprise, modification et levée.

### Incidents / ruptures

- Localisation, PK, type de localisation.
- Heures de début et de fin.
- État et commentaires.
- Création, consultation, modification et clôture selon la règle métier.

## Variables de pilotage repérées dans le YAML

- `varOngletJournal` : onglet actif.
- `varActionEnCours` : mode de traitement, notamment création/modification.
- `varTravauxToEdit`, `varLtvToEdit`, `varIncidentToEdit` : enregistrement ciblé.
- `varAttemptedSave` : état de tentative de sauvegarde.
- `varFeedbackEvent` : événement Travaux sélectionné pour le feedback.
- `varQuart` : poste courant.

## État connu à la consolidation du 11/11/2026

| Fonction | État |
|---|---|
| Création Travaux | Fonctionnelle selon les tests précédents |
| Préremplissage Travaux | Présent dans le code |
| Modification Travaux avec conservation du même ID | Problème signalé, à corriger et retester |
| Suppression Travaux | À valider |
| Création LTV | Échec signalé dans les échanges ultérieurs ; à retester |
| Reprise/modification LTV | Problème signalé ; bloquant |
| Incidents/ruptures | Audit CRUD à poursuivre |
| Feedback après sauvegarde | Mécanismes présents ; recette à finaliser |

Une note datée du 05/10/2026 indiquait un test LTV réussi et la modification Travaux validée. Ces indications contredisent les problèmes signalés ensuite. Le statut conservateur est donc « à retester », pas « validé ».

## Règle technique de sauvegarde

- Création : `Patch(Liste, Defaults(Liste), {...})`.
- Modification : `Patch(Liste, enregistrementExistant, {...})`.
- Suppression : cibler l'enregistrement existant.
- Le mode modification ne doit jamais utiliser `Defaults(Liste)`.
- L'ID SharePoint doit rester identique après modification.
- Utiliser les noms internes et types de colonnes documentés dans `Backend/contextBD.md`, après confirmation dans l'environnement réel.

## Demandes métier encore à traiter

- Recherche du canton par saisie/matching.
- Motifs standardisés avec possibilité de saisie libre complémentaire.
- Filtres LTV par date et canton.
- Historique des événements.
- Mise à jour de l'intervenant qui reprend un événement.
- Simplification/épuration de la vue Travaux.
- Clarification de l'appellation « ATTACHEMENT » dans les régimes de travaux.

## Tests de non-régression

Pour chaque liste, tester création, lecture, modification, suppression, champs facultatifs, erreurs de saisie, valeurs Choice/Lookup et contrôle direct dans SharePoint. Pour une modification, comparer l'ID avant et après.
