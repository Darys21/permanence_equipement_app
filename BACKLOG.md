# Backlog du projet — Permanence Équipement

**Dernière consolidation : 13/11/2026**  
**Dépôt de référence :** `Darys21/permanence_equipement_app`  
**Sources de synchronisation :** YAML Power Apps de `Darys21/PERMANENCE-EQUIPEMENT/pa_yaml_script`, retours des permanents et historique des corrections réalisées.

## Règles de suivi

- **Terminé (code)** : implémenté ou corrigé dans les sources selon les derniers échanges.
- **À valider** : présent dans le code, mais recette fonctionnelle ou métier incomplète.
- **En cours / bloquant** : problème connu ou comportement non fiable.
- **À faire** : non implémenté ou non démontré.
- **À clarifier** : décision métier contradictoire ou incomplète.

> Un élément « terminé (code) » n'est pas automatiquement considéré comme validé en production. Les tests Power Apps + SharePoint restent nécessaires.

---

## 1. Authentification et identification du permanent

| ID | Action | Statut | Notes |
|---|---|---|---|
| AUTH-01 | Écran de sélection du permanent depuis `Ref_Permanents` | Terminé (code) | Remplace l'ancienne hypothèse d'auto-identification M365. |
| AUTH-02 | Authentification par code PIN personnel | Terminé (code) | Champ masqué, longueur configurée à 4 caractères dans le YAML source. |
| AUTH-03 | Bloquer la navigation si aucun permanent ou PIN valide | Terminé (code) | Contrôle présent dans le bouton de validation. |
| AUTH-04 | Passer le permanent connecté à `Actif = Oui` | Terminé (code) | Colonne SharePoint de type Choix. |
| AUTH-05 | Libérer l'ancien permanent (`Actif = Non`) au changement d'agent | Terminé (code) | Mise à jour des autres agents actifs prévue dans la formule actuelle. |
| AUTH-06 | Conserver l'identité dans les variables globales de session | Terminé (code) | `varAgentPermanent`, `varAgentPermanentNom`, `varAgentPermanentID`. |
| AUTH-07 | Tester PIN erroné, agent absent, changement d'agent et statut SharePoint | À valider | Recette complète à refaire sur l'environnement cible. |
| AUTH-08 | Bloquer les doubles sessions d'un même agent | À clarifier | Définir la règle métier et son comportement en cas de session abandonnée. |

## 2. Prise de poste — `PrisePoste_2`

| ID | Action | Statut | Notes |
|---|---|---|---|
| POSTE-01 | Proposer automatiquement P1, P2 ou P3 selon l'heure | Terminé (code) | P1 : 06h–14h ; P2 : 14h–22h ; P3 : 22h–06h. |
| POSTE-02 | Autoriser le choix manuel du poste | Terminé (code) | Les trois postes restent disponibles. |
| POSTE-03 | Conserver P3 | Terminé / décision récente | P3 a été explicitement confirmé comme conservé. Les anciennes notes demandant sa suppression sont obsolètes. |
| POSTE-04 | Rendre le deuxième permanent facultatif | Terminé (code) | La prise de poste ne doit pas être bloquée si ce champ est vide. |
| POSTE-05 | Afficher les éléments à reprendre | Présent dans le YAML / à valider | Travaux, LTV/RAL actifs, incidents et ruptures en cours. Vérifier le filtrage réel et la continuité entre postes. |
| POSTE-06 | Bloquer le démarrage si l'identité ou le poste manque | Terminé (code) | Garde-fous présents dans le parcours. |
| POSTE-07 | Tester P1/P2/P3, suggestion horaire et reprise des événements | À valider | Tests de bout en bout requis. |
| POSTE-08 | Définir et enregistrer un poste exceptionnel | À clarifier | Règle métier et modèle de données à définir avant développement. |
| POSTE-09 | Automatiser la transmission des événements ouverts au poste suivant | À faire | Ne pas confondre affichage des éléments à reprendre et transfert réellement persisté. |

## 3. Journal de bord — `JournalDeBord_3`

**Priorité critique : fiabilité des données et conservation des identifiants SharePoint.**

| ID | Action | Statut | Notes |
|---|---|---|---|
| JOUR-01 | Créer un événement Travaux | Fonctionnel selon les tests précédents | La création a été confirmée fonctionnelle dans les échanges. |
| JOUR-02 | Préremplir le formulaire Travaux en modification | Présent / à valider | Le préremplissage existe dans le code. |
| JOUR-03 | Modifier un Travaux sans changer son ID SharePoint | Bloquant / à corriger | Un changement d'ID lors de la modification a été signalé. Vérifier que `Patch` cible l'enregistrement existant et non `Defaults()`. |
| JOUR-04 | Supprimer un Travaux correctement | À valider | Vérifier la cible, la confirmation et le rafraîchissement de la galerie. |
| JOUR-05 | Créer un LTV | Bloquant / à retester | Des échecs d'enregistrement ont été signalés dans les échanges ultérieurs. Une note plus ancienne indique un test réussi : résultat contradictoire, ne pas considérer comme validé. |
| JOUR-06 | Reprendre et modifier un LTV existant | Bloquant / à corriger | La reprise impossible a été signalée. Préserver l'ID de l'enregistrement. |
| JOUR-07 | Gérer le statut LTV imposée / supprimée | Présent dans le YAML / à valider | Vérifier les valeurs Choice SharePoint exactes, les dates et les filtres. |
| JOUR-08 | Créer, modifier et supprimer un incident/une rupture | À auditer | Contrôler le schéma Lookup `CantonID0`, les champs et les opérations CRUD. |
| JOUR-09 | Valider l'ordre chronologique et les calculs de durée/retard | À valider | Vérifier les champs Date/Heure, les valeurs vides et les cas de prolongation. |
| JOUR-10 | Vérifier les filtres et galeries par poste | À valider | Ne pas supposer que les données ouvertes sont automatiquement transférées entre postes. |
| JOUR-11 | Vérifier les messages de succès/échec et la conservation du formulaire en cas d'erreur | À valider | Feedback visible uniquement après confirmation de la sauvegarde. |
| JOUR-12 | Rechercher un canton par saisie/matching | À faire | Demande issue des retours d'équipe. |
| JOUR-13 | Ajouter des motifs standardisés avec saisie libre complémentaire | À faire | Engagement et dégagement tardifs notamment. |
| JOUR-14 | Ajouter un historique des événements | À faire | Historique complet consultable, selon règles d'accès à définir. |
| JOUR-15 | Ajouter les filtres LTV par date et canton | À faire | Besoin issu des notes d'alignement métier. |
| JOUR-16 | Permettre la mise à jour de l'intervenant qui reprend un événement | À faire | Conserver l'historique de l'intervenant précédent si la règle métier le demande. |
| JOUR-17 | Épurer la vue Travaux | À faire | Note complémentaire du fichier « Update a faire ». |

### Règle technique non négociable

- Création : utiliser `Defaults(Liste)`.
- Modification : utiliser l'enregistrement existant comme deuxième argument de `Patch` (ou son ID résolu par `LookUp`).
- Suppression : cibler explicitement l'enregistrement existant.
- Après chaque opération : contrôler `IfError`, le résultat de sauvegarde, l'ID conservé et le rafraîchissement de la source.
- Ne jamais utiliser `Defaults()` dans le chemin de modification.

### Quick wins UI rapportés comme réalisés le 05/10/2026

| ID | Action | Statut | Notes |
|---|---|---|---|
| JOUR-18 | Normaliser les titres `Title` dans Travaux, LTV et Incidents | Réalisé selon note du 05/10 / à contrôler | Vérifier la non-régression. |
| JOUR-19 | Ajouter le champ « Titre de chantier » | Réalisé selon note du 05/10 / à contrôler | Champ et écriture SharePoint indiqués comme livrés. |
| JOUR-20 | Afficher le canton avant le titre dans la galerie Travaux | Réalisé selon note du 05/10 / à contrôler | Vérifier l'ordre actuel des colonnes. |
| JOUR-21 | Afficher canton, taux puis titre dans la galerie LTV | Réalisé selon note du 05/10 / à contrôler | Vérifier l'ordre actuel des colonnes. |
| JOUR-22 | Colorer les LTV imposées en rouge et supprimées en vert ; mettre en évidence 10 km/h | Réalisé selon note du 05/10 / à contrôler | Vérifier les couleurs et les valeurs Choice. |
| JOUR-23 | Clarifier le message de validation LTV et conserver le motif en texte simple | Réalisé selon note du 05/10 / à contrôler | Rejouer le parcours LTV après correction de la sauvegarde. |

## 4. Feedback terrain — `scrFeedback`

| ID | Action | Statut | Notes |
|---|---|---|---|
| FB-01 | Écran de nouveau pointage terrain | Terminé (code) | Écran présent dans le YAML source. |
| FB-02 | Rattacher le pointage à un chantier Travaux | Terminé (code) / à valider | Contrôler la relation via `TravailID`. |
| FB-03 | Saisir heure, moyen de contact, PK, statut et commentaire | Terminé (code) | Contrôler les types et valeurs Choice/Boolean SharePoint. |
| FB-04 | Consulter le résumé et l'historique des pointages | Présent dans le YAML / à valider | Tester le filtrage par chantier et poste. |
| FB-05 | Enregistrer un pointage et revenir au journal | À valider | Une note antérieure indique SaveFeedback fonctionnel ; refaire un test de bout en bout. |
| FB-06 | Vérifier les retours de sauvegarde et les erreurs | À valider | Ne pas vider les champs en cas d'échec. |
| FB-07 | Définir l'édition/suppression des feedbacks | À clarifier | Règle métier non confirmée. |

## 5. Clôture et relève — `scrCloture_2`

| ID | Action | Statut | Notes |
|---|---|---|---|
| CLOT-01 | Écran de clôture structuré en étapes | Terminé (code) | Synthèse, commentaire/transmission, confirmation. |
| CLOT-02 | Afficher le bilan Travaux, LTV, incidents et feedbacks | Présent dans le YAML / à valider | Vérifier les compteurs et les détails affichés. |
| CLOT-03 | Saisir un commentaire de fin de poste | Présent dans le YAML / à valider | Tester la persistance si elle est attendue. |
| CLOT-04 | Prévisualiser le rapport de fin de poste | Présent dans le YAML / à valider | Vérifier les données et les périodes. |
| CLOT-05 | Valider la clôture et empêcher les doubles validations | À valider | Tester le comportement après clic et en cas d'erreur. |
| CLOT-06 | Transférer réellement les événements ouverts au poste suivant | À faire | La présence d'un texte de transmission dans l'écran ne prouve pas le transfert SharePoint. |
| CLOT-07 | Générer et envoyer automatiquement le rapport | À faire | Nécessite un flux Power Automate et sa configuration. |
| CLOT-08 | Définir la boucle de succession des postes | À clarifier | Les notes historiques se contredisent sur P3 ; la décision récente confirme P3 conservé. |

## 6. SharePoint et qualité des données

| ID | Action | Statut | Notes |
|---|---|---|---|
| SP-01 | Utiliser les référentiels `Ref_Permanents`, `Ref_Cantons`, `Ref_Acteurs` | Terminé (code) | Connexions utilisées par les écrans. |
| SP-02 | Utiliser les listes transactionnelles Travaux, LTV, Incidents/Ruptures et Feedbacks | Terminé (code) | Contrôle des opérations CRUD encore nécessaire. |
| SP-03 | Vérifier les noms internes, types, colonnes obligatoires et valeurs Choice | À valider | S'appuyer sur `Backend/contextBD.md` et confirmer dans l'environnement réel. |
| SP-04 | Mettre à jour les données des cantons et divisions | À faire | Note « Update a faire ». |
| SP-05 | Vérifier les relations Lookup et clés étrangères | À valider | En particulier LTV et Incidents. |
| SP-06 | Vérifier les champs audit (poste, agent, date de saisie) | À valider | Cohérence entre listes et écrans. |
| SP-07 | Décider du retrait de l'appellation « ATTACHEMENT » | À clarifier | Valeur actuellement documentée dans le choix Régime travaux ; vérifier l'impact métier et SharePoint avant modification. |

### Qualité des saisies et environnements

| ID | Action | Statut | Notes |
|---|---|---|---|
| SP-08 | Contrôler le format Date/Heure avant Patch | À valider | Une réunion a identifié un problème de format ; la solution proposée consiste à reconstruire la valeur DateTime à partir de la date, de l'heure et des minutes. |
| SP-09 | Vérifier les sources SharePoint des environnements de test et de production | À faire | Power Apps ne bascule pas automatiquement toutes les sources ; vérifier chaque connexion avant publication. |
| UX-01 | Ajouter des points de contrôle dans les formulaires | À faire | Demande issue des notes de réunion ; préciser les contrôles métier et les messages attendus. |
| UX-02 | Revoir les paramètres de recherche des contrôles de données | À clarifier | Note ancienne évoquant la désactivation de l'autorisation de recherche ; clarifier le besoin exact avant modification. |

## 7. Demandes complémentaires et continuité d'activité

| ID | Action | Statut | Notes |
|---|---|---|---|
| EXT-01 | Export Excel de secours | À faire | Exporter la structure de saisie. |
| EXT-02 | Import Excel et reconnaissance d'un chantier | À faire | Définir règles de correspondance et prévention des doublons. |
| EXT-03 | Revue métier du module Incidents/Accidents | À clarifier | Anciennes notes indiquent une attente de validation métier. |
| EXT-04 | Harmoniser les titres et libellés | À valider | Conserver les quick wins déjà intégrés et vérifier l'ensemble des écrans. |

## 8. Recette finale

- [ ] Connexion avec PIN valide et invalide.
- [ ] Prise de poste P1, P2 et P3.
- [ ] Changement d'agent et remise à jour du statut actif.
- [ ] Reprise des événements ouverts.
- [ ] Création, modification et suppression Travaux avec conservation de l'ID en modification.
- [ ] Création, reprise, modification et levée d'un LTV.
- [ ] Création, modification et clôture d'un incident.
- [ ] Ajout et consultation d'un feedback.
- [ ] Clôture du poste, transmission réelle et rapport.
- [ ] Contrôle direct des lignes SharePoint après chaque opération.
- [ ] Test avec plusieurs permanents et validation métier.

## 9. Ordre d'exécution recommandé

1. **Bloquants Journal** : corriger et tester modification Travaux, création/reprise LTV.
2. **Incidents** : audit CRUD et validation du schéma.
3. **SharePoint** : confirmer schémas, référentiels et audit.
4. **Clôture** : valider les étapes et implémenter la transmission réelle.
5. **Feedback** : recette complète et règles d'édition/suppression.
6. **UX métier** : recherche canton, motifs, filtres LTV, historique, simplification Travaux.
7. **Automatisation et continuité** : rapport Power Automate, export/import Excel.
8. **Recette avec les permanents**, puis déploiement.

---

## 10. Décisions à ne pas perdre

- P1, P2 et P3 sont conservés dans la version actuelle ; ne pas supprimer P3 sur la base des notes historiques du 05/10.
- Le deuxième permanent est facultatif.
- La succession est une suggestion/parcours à clarifier, pas un blocage arbitraire.
- Une modification ne doit jamais créer un nouvel ID SharePoint.
- Les écrans présents dans le YAML ne sont pas automatiquement considérés comme testés ni validés.


---

## 11. Mise à jour du suivi — 13/11/2026

Cette section complète le backlog à partir des derniers échanges du projet. Les statuts historiques ci-dessus sont conservés ; les éléments ci-dessous précisent les dernières demandes et validations connues.

### 11.1 Identification et connexion

| ID | Action | Statut | Notes |
|---|---|---|---|
| AUTH-09 | Revoir visuellement la page de connexion/identification avec une interface plus moderne | Maquette réalisée | Une proposition graphique a été générée et appréciée. |
| AUTH-10 | Fournir l'illustration de fond seule, sans le bloc de connexion | À faire | Conserver le visuel validé ; livrer une version exploitable comme image de fond Power Apps. |
| AUTH-11 | Intégrer la nouvelle maquette dans Power Apps avec des contrôles natifs | À faire | Respecter les limites de mise en page et de composants Power Apps. |

### 11.2 Prise de poste

| ID | Action | Statut | Notes |
|---|---|---|---|
| POSTE-10 | Corriger le YAML de l'écran de prise de poste dans le fichier `PrisePoste_3.pa.yaml` | Terminé (import accepté) | Le YAML corrigé a été importé sans erreur selon le dernier retour. |
| POSTE-11 | Vérifier le comportement fonctionnel de l'écran après import | À valider | L'acceptation du YAML ne prouve pas le bon fonctionnement des formules et des données. |

### 11.3 Journal de bord

| ID | Action | Statut | Notes |
|---|---|---|---|
| JOUR-24 | Reprendre la correction du YAML de l'écran Journal de bord | À confirmer | Une demande de correction a été formulée ; ne pas déclarer la correction livrée sans vérifier le commit et le fichier final dans le dépôt. |
| JOUR-25 | Rejouer les scénarios CRUD après correction du YAML | À faire | Tester séparément Travaux, LTV et Incidents/Ruptures : création, modification, suppression et conservation de l'ID SharePoint. |
| JOUR-26 | Valider spécifiquement la sauvegarde et la reprise des LTV | Bloquant / à corriger | Le dernier problème fonctionnel connu reste l'échec de sauvegarde et la reprise impossible d'un LTV. |

### 11.4 Règles de mise à jour du backlog

- Cocher ou passer une tâche à « Terminé (code) » uniquement lorsqu'une modification est effectivement présente dans le dépôt.
- Passer une tâche à « À valider » lorsque le code est modifié mais que le scénario Power Apps/SharePoint n'a pas été testé.
- Conserver « Bloquant » tant qu'un défaut reproductible empêche le parcours métier.
- Ajouter une note de test (scénario, résultat, date) lors de chaque validation.
- Ne pas assimiler un YAML importé sans erreur à une fonctionnalité métier validée.
- Lorsqu'une demande est corrigée, mettre à jour la ligne existante plutôt que créer un doublon ; conserver les identifiants historiques.

### 11.5 Prochaine séquence de travail

1. Confirmer la version du YAML Journal de bord présente dans le dépôt.
2. Corriger et tester la création, la modification et la reprise des LTV.
3. Vérifier que les modifications Travaux conservent leur ID SharePoint.
4. Exécuter les tests CRUD des incidents et ruptures.
5. Tester le parcours complet identification → prise de poste → journal → clôture.
6. Préparer l'image de fond seule et intégrer la nouvelle interface de connexion.


## 11. Standard de développement `.pa.yaml` adopté — 16/11/2026

Le workflow contraint est désormais documenté dans [`docs/PA_YAML_WORKFLOW.md`](docs/PA_YAML_WORKFLOW.md).

À appliquer à toute intervention YAML : découverte du périmètre et des dépendances, plan par écran, vérification des contrôles/propriétés, génération minimale, audit statique, validation YAML/import/compilation, QA visuelle et fonctionnelle, contrôle SharePoint, puis compte rendu avec preuves.

**Limite d'outillage constatée :** les outils `list_controls`, `describe_control`, `compile_canvas` et les QAChecks Canvas ne sont pas exposés dans la session connectée. Ne jamais prétendre les avoir exécutés. Tant qu'ils ne sont pas disponibles, vérifier les contrôles à partir du YAML existant et de Power Apps Studio, et signaler les validations qui restent manuelles.

**Prochaine application :** reprendre `JournalDeBord_3.pa.yaml` depuis sa source de vérité, cartographier les opérations CRUD, puis traiter en priorité la sauvegarde/reprise LTV et la modification Travaux avec conservation de l'ID. Aucun statut du backlog métier n'est automatiquement changé par l'adoption de ce workflow.


## 12. Audit P0 — versions actives confirmées et première correction — 16/11/2026

Versions confirmées par l'utilisateur dans Power Apps Studio :
- Prise de poste : `PrisePoste_2`.
- Journal de bord : `JournalDeBord_3`.

### P0.1 — Cohérence des noms d'écrans

Audit des cinq fichiers présents dans `Darys21/PERMANENCE-EQUIPEMENT/pa_yaml_script` : les navigations observées ciblent `JournalDeBord_3`, `PrisePoste_2`, `scrIdentificationAgent`, `scrFeedback` et `scrCloture_2`. Aucune référence à `JournalDeBord_4` n'a été trouvée dans ces sources. Les noms de navigation du dépôt sont donc cohérents avec les versions actives confirmées ; aucune renommage n'a été effectué. À recontrôler dans l'application complète si d'autres fichiers/sources existent hors de ce dépôt.

### P0.2 — Diagnostic création / modification / reprise LTV

Le YAML contient un chemin de création/modification via `Patch(Tx_LTV, LookUp(...), ...)` ou `Defaults(Tx_LTV)`, ainsi que des champs Lookup/Choice. Le code seul ne permet pas d'identifier la cause de l'échec. Le diagnostic reste ouvert dans l'attente du message exact affiché au clic sur « ENREGISTRER LTV » et du schéma réel de `Tx_LTV` (noms internes et types, notamment colonnes avec espaces finaux). La chaîne `Imposée (Active)` n'est pas présente dans le fichier audité ; les filtres utilisent `Imposée` et `Supprimée`.

### P0.3 — Préserver le Title lors de la modification LTV

Correction appliquée dans `pa_yaml_script/JournalDeBord_3.yaml` : lors d'une modification, `Title` reprend désormais `varLtvToEdit.Title` (avec valeur de repli uniquement si le titre existant est vide). À la création, le titre généré reste inchangé. Commit source : `df6c1494d62b256ff74c1ab4f798b9f0cff0ab8b`.

**Statut :** correction présente dans le dépôt source ; import Power Apps Studio et test de modification LTV encore à effectuer. Aucun statut fonctionnel n'est déclaré terminé.
