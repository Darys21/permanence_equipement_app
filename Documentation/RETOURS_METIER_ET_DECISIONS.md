# Retours métier, notes de réunion et décisions consolidées

**Consolidation : 11/11/2026**  
**Sources analysées :** dossier `Documentation tirage` du dépôt `Darys21/PERMANENCE-EQUIPEMENT`, backlog de suivi, notes de réunion, notes du 05/10 et historique de travail dans le projet.

Ce document rassemble les demandes utiles à la maintenance de l'application. Les notes historiques contradictoires ne sont pas traitées comme des décisions actuelles sans confirmation.

## 1. Demandes des permanents et améliorations UX

| Demande | Écran concerné | Statut au 11/11/2026 | Commentaire |
|---|---|---|---|
| Identifier le permanent avant l'accès à l'application | Identification | Intégré | Sélection du nom + PIN. |
| Éviter l'accès sans agent sélectionné | Identification | Intégré | Garde-fou présent. |
| Choisir P1/P2/P3 avec suggestion horaire | Prise de poste | Intégré | Les trois postes sont conservés. |
| Afficher les événements à reprendre | Prise de poste | Présent / à tester | Travaux, LTV et incidents ouverts. |
| Recherche du canton par saisie du début du nom | Journal | À faire | Recherche/matching demandé. |
| Motifs standardisés et saisie d'un motif libre | Journal Travaux | À faire | Engagement et dégagement tardifs notamment. |
| Filtres LTV par date et canton | Journal LTV | À faire | Besoin remonté dans les notes d'alignement. |
| Historique des événements | Journal / clôture | À faire | Définir la profondeur et les critères de recherche. |
| Mettre à jour l'intervenant qui reprend un événement | Journal | À faire | Clarifier la conservation de l'historique. |
| Simplifier la vue Travaux | Journal Travaux | À faire | Note complémentaire « Update a faire ». |
| Export Excel de secours | Journal | À faire | Mode de continuité en cas d'indisponibilité de l'application. |
| Import Excel et reconnaissance du chantier | Journal | À faire | Définir mapping et prévention des doublons. |
| Revoir le module Incidents/Accidents | Journal | À clarifier | Validation métier nécessaire. |

## 2. Décisions actuelles à préserver

- Le permanent est identifié par sélection de son nom et saisie d'un PIN.
- Le statut de l'agent est géré via `Ref_Permanents` et la colonne de choix `Actif` (`Oui` / `Non`).
- P1, P2 et P3 sont conservés dans la version actuelle.
- Le deuxième permanent est facultatif.
- La suggestion de poste ne doit pas empêcher le choix manuel.
- La succession ne doit pas devenir un blocage arbitraire.
- La modification d'un événement doit conserver son ID SharePoint.
- Les écrans présents dans les exports YAML ne sont pas réputés validés sans test.

## 3. Divergences dans les notes historiques

### P3 : supprimé ou conservé ?

Une note du 05/10/2026 indiquait « P3 supprimé ». La version actuelle du YAML de prise de poste contient P1, P2 et P3, et les échanges récents ont explicitement confirmé que P3 est conservé. **La décision récente prévaut : ne pas supprimer P3.**

### Travaux et LTV : validés ou encore défaillants ?

La liste de tâches du 05/10 indiquait Travaux création/modification validés et LTV enregistré avec succès. Des échanges ultérieurs ont signalé un changement d'ID lors de la modification Travaux et des problèmes de création/reprise LTV. **Ces fonctionnalités doivent être retestées et ne sont pas considérées comme définitivement validées.**

### Transmission automatique

Les notes évoquent plusieurs cycles de transmission, dont P1 → P2 → P3 → P1. Le comportement actuellement retenu dans l'application conserve P1/P2/P3, mais la règle exacte de succession et la persistance du transfert restent à confirmer. Ne pas coder un transfert automatique sur la seule base d'une note ancienne.

## 4. Notes techniques complémentaires à intégrer au backlog

- Mettre à jour les données de référence des cantons et divisions.
- Épurer la vue de la partie Travaux.
- Clarifier la demande « finaliser la partie » présente dans les notes brèves : le périmètre n'est pas explicite.
- Revoir l'appellation « ATTACHEMENT » dans les choix du régime de travaux. Le schéma backend documente encore cette valeur ; toute suppression nécessite une décision métier et une mise à jour SharePoint coordonnée.
- Vérifier les champs Date/Heure et leur conversion entre contrôles Power Apps et colonnes SharePoint.
- Maintenir la séparation entre environnement de test et production ; ne pas modifier les sources de données de production sans validation.

## 5. Éléments non repris volontairement

- Le document `V2 RAPPORT INSPECTIONS.md` concerne un tableau de bord RH de suivi d'inspections et ne relève pas du périmètre de l'application Permanence Équipement.
- Les URLs Graph brutes contenant les identifiants du site et des listes ne sont pas dupliquées ici. Le dictionnaire de données et les schémas sont documentés dans `Backend/contextBD.md`.
- Les notes de conversation ou prompts destinés à un autre assistant ne sont pas copiés comme spécifications techniques.
