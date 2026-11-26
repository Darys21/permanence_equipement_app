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
| JOUR-12 | Rechercher un canton par saisie/matching | Modifié — non validé (25/11/2026) | Demande issue des retours d'équipe. |
| JOUR-13 | Ajouter des motifs standardisés avec saisie libre complémentaire | Modifié — non validé (25/11/2026) | Engagement et dégagement tardifs : liste de motifs conservée ; si « Autre » est choisi, un champ texte libre (255 car.) apparaît et son contenu est enregistré à la place de « Autre ». Voir §18. |
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
- Le deuxième permanent est obligatoire les mardis et vendredis (journées de grands travaux) ; il reste facultatif les autres jours.
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


## 13. Vérification des demandes des permanents — 16/11/2026

### 13.1 Interface d'accueil — arrière-plan métier DMI

| ID | Action | Statut | Vérification |
|---|---|---|---|
| UX-03 | Ajouter un arrière-plan représentant l'activité DMI (rails, voies, données, équipements) à l'écran d'accueil/identification | Validé par l'utilisateur | L'utilisateur confirme le 16/11/2026 avoir modifié l'image de fond et validé le résultat. |

### 13.2 Accès sécuritaire — identité, mot de passe et verrouillage

| ID | Action | Statut | Vérification |
|---|---|---|---|
| AUTH-12 | Identifier l'agent par son nom et son code PIN personnel | Présent dans le code / test à confirmer | `scrIdentificationAgent` contient une sélection d'agent, un champ PIN masqué et une vérification du PIN dans `Ref_Permanents`. |
| AUTH-13 | Permettre à l'utilisateur de verrouiller son poste avec son mot de passe/PIN, puis de reprendre sa session | Implémenté dans la branche / à valider | Aucun mécanisme de verrouillage/déverrouillage de session n'a été repéré dans les écrans actifs audités. Le bouton « Changer d'agent » revient à l'identification et remet l'agent actif à Non ; ce n'est pas un verrouillage temporaire. |
| AUTH-14 | Définir les règles de sécurité de session (expiration, déverrouillage, protection contre les modifications par un autre agent) | Règle de déverrouillage codée / à valider | Option B validée le 16/11/2026 : le permanent initial ou le deuxième permanent déclaré peut déverrouiller le poste. Le verrouillage ne doit pas modifier le statut Actif, ni perdre le poste ou les données en cours. Définir les contrôles d'identité, les états de session et les cas d'erreur avant implémentation. |

### 13.3 Poste pluri-personnel — deux permanents en activité

| ID | Action | Statut | Vérification |
|---|---|---|---|
| POSTE-12 | Ajouter un menu déroulant pour sélectionner un deuxième permanent sur un même poste | Implémenté dans la branche / à valider | `PrisePoste_2` affiche le permanent connecté et permet de choisir P1/P2/P3 ; aucun second sélecteur de permanent n'a été repéré dans le YAML audité. |
| POSTE-13 | Exiger deux permanents actifs pour les journées de grands travaux | Implémenté dans la branche / à valider | La validation actuelle vérifie l'identité du premier permanent et le choix du poste, mais aucun contrôle n'impose deux permanents pour un cas « grands travaux ». |
| POSTE-14 | Définir les règles de présence du deuxième permanent selon le type de journée/poste | À cadrer | Confirmer si le deuxième permanent est obligatoire uniquement pour les journées de grands travaux ou également dans d'autres situations. |

### 13.4 Anomalie d'affichage LTV non bloquante

| ID | Action | Statut | Vérification |
|---|---|---|---|
| JOUR-27 | Corriger l'erreur de conversion affichée par le compteur LTV `EventCount_22` (« Impossible de convertir la valeur '0 | Imp 0 | Sup 0' en nombre ») | Correctif à faire — non bloquant | L'utilisateur confirme que le LTV s'enregistre correctement et que le message de succès apparaît. Le défaut concerne l'indicateur/compteur d'affichage ; ne pas modifier le chemin de sauvegarde LTV pour traiter cette anomalie. La première proposition de correction de typage n'a pas résolu le problème. **25/11/2026 : cause identifiée et corrigée dans le YAML (Modifié — non validé), voir §19.** |

### 13.5 Résultat de la vérification

- **Déjà présent dans le code :** identification par nom + PIN ; sélection du poste P1/P2/P3 ; changement d'agent.
- **À tester dans Power Apps :** parcours complet d'identification par PIN et prise de poste, y compris PIN invalide.
- **Décision verrouillage :** déverrouillage autorisé au permanent initial ou au deuxième permanent déclaré (option B). L'implémentation reste à faire.
- **À faire :** image métier en arrière-plan ; verrouillage/déverrouillage temporaire par PIN ; sélection d'un deuxième permanent ; règle conditionnelle imposant deux permanents pour les journées de grands travaux.
- **Anomalie non bloquante :** erreur de conversion du compteur LTV, conservée au backlog. La sauvegarde LTV est confirmée fonctionnelle par le test utilisateur du 16/11/2026.
- Les statuts « présent dans le code » ne valent pas validation métier complète.


## 14. Implémentation initiale — deuxième permanent et verrouillage PIN — 16/11/2026

Travail réalisé dans la branche `feature/permanents-lock-session` du dépôt source `Darys21/PERMANENCE-EQUIPEMENT` ; aucune fusion dans `main` ni import Power Apps Studio n'a encore été effectué.

- `PrisePoste_2.yaml` : ajout d'un ComboBox pour sélectionner un deuxième permanent depuis `Ref_Permanents`, en excluant le permanent initial.
- Règle calendrier : le deuxième permanent est obligatoire lorsque `Weekday(Today(), StartOfWeek.Monday)` vaut 2 (mardi) ou 5 (vendredi) ; il reste facultatif les autres jours.
- Démarrage du service : association des deux enregistrements et du poste dans les variables de session `varPermanentPrincipalSession`, `varPermanentSecondaireSession` et `varSessionPoste`. Le statut SharePoint `Actif` du deuxième permanent passe à Oui au démarrage, puis à Non lors du changement d'agent ou de la clôture.
- Verrouillage manuel : bouton ajouté au journal, au feedback et à la clôture ; un écran de verrouillage est présent sur Prise de poste, Journal, Feedback et Clôture.
- Déverrouillage : le PIN doit correspondre au permanent initial (`varAgentPermanentID`) ou au deuxième permanent déclaré (`varPermanentSecondaireSession.ID`). Le verrouillage ne modifie pas le champ SharePoint `Actif`.
- Changement d'agent : remise à zéro des variables de session pour éviter de conserver le deuxième permanent d'une session précédente.

**Limites et validations restantes :**
- L'association des permanents est actuellement conservée dans les variables globales Power Apps ; elle n'est pas persistée dans une liste SharePoint de sessions. Elle ne constitue donc pas un journal de session durable après fermeture/rechargement de l'application.
- Aucun verrouillage automatique après inactivité n'a été ajouté ; le verrouillage est manuel.
- Vérifier l'import des quatre YAML dans Power Apps Studio, les propriétés de contrôle, la visibilité de l'overlay, les PIN valides/invalides des deux permanents, le comportement mardi/vendredi et les autres jours.
- Vérifier l'affichage du ComboBox dans la zone de prise de poste et la compatibilité réelle de la colonne `Title` dans `Ref_Permanents`.
- Ne passer les tâches à « Terminé » qu'après recette fonctionnelle dans Power Apps et contrôle des données SharePoint.


## 15. Gestion pluripersonnelle et traçabilité individuelle — décisions validées le 16/11/2026

Cette section **remplace les règles contradictoires antérieures** relatives au caractère bloquant du deuxième permanent (notamment POSTE-04, POSTE-13, POSTE-14 et les décisions des sections 10, 13 et 14). Les anciennes notes restent conservées comme historique, mais ne constituent plus la règle métier active.

### 15.1 Décisions métier validées

| ID | Action | Statut | Notes |
|---|---|---|---|
| POSTE-15 | Permettre au premier permanent d'accéder à la prise de poste sans attendre le deuxième | Décision validée / À faire | Le deuxième permanent ne doit jamais bloquer l'accès ou les opérations du premier, y compris le mardi et le vendredi. Ces jours restent des journées où deux permanents sont normalement attendus, mais l'application ne bloque pas le service si le second n'est pas encore connecté. |
| POSTE-16 | Proposer l'ajout d'un deuxième permanent après la connexion du premier | Décision validée / À faire | La proposition apparaît après authentification du premier. Le deuxième peut être ajouté immédiatement ou ultérieurement. |
| POSTE-17 | Permettre le changement d'opérateur sur le même poste | Décision validée / À faire | Bouton « Changer de permanent » ; afficher la liste des permanents associés à la session, puis demander le PIN du permanent qui prend la main. |
| POSTE-18 | Maintenir un seul opérateur actif à la fois | Décision validée / À faire | L'opérateur authentifié est l'auteur par défaut de toutes les opérations qu'il enregistre jusqu'au prochain changement d'opérateur. |
| POSTE-19 | Permettre l'ajout tardif du deuxième permanent | À faire | Le permanent secondaire doit pouvoir rejoindre une session déjà commencée, s'authentifier par PIN et être ajouté aux permanents associés sans perdre les données ni interrompre la session. |
| AUD-01 | Enregistrer l'auteur de chaque opération | Décision validée / À faire | Travaux, incidents/ruptures, LTV et feedbacks : enregistrer automatiquement l'ID et le nom du permanent opérateur au moment de la création. |
| AUD-02 | Rattacher chaque opération à la session de permanence | Décision validée / À faire | Chaque opération doit conserver l'identifiant de la session (poste + période) pour permettre la reconstitution de l'activité globale. |
| AUD-03 | Conserver l'auteur initial et tracer les modifications | À faire | Ne jamais écraser l'auteur initial lors d'une modification. Ajouter séparément l'identité du dernier modificateur et la date de modification ; envisager un journal d'audit complet si l'historique de toutes les modifications est requis. |
| CLOT-09 | Ajouter une synthèse globale de la permanence | Décision validée / À faire | Total des travaux, incidents/ruptures, LTV et feedbacks associés à la session. |
| CLOT-10 | Ajouter une synthèse individuelle par permanent | Décision validée / À faire | Répartition des opérations par auteur, sans double comptage. |
| CLOT-11 | Ajouter un historique détaillé des opérations | Décision validée / À faire | Afficher le type d'opération, l'identifiant/titre, l'auteur, la date/heure et, si pertinent, le dernier modificateur. |

### 15.2 Règles de fonctionnement à implémenter

- La connexion du premier permanent ouvre la session et permet de commencer immédiatement.
- Après cette connexion, proposer l'ajout d'un deuxième permanent. Le choix « pas maintenant » ne bloque jamais la navigation.
- Le deuxième permanent peut être ajouté plus tard depuis la session active.
- Un bouton de changement d'opérateur affiche les permanents associés à la session ; le permanent choisi saisit son propre PIN.
- Un seul opérateur est actif à la fois sur le poste partagé. Son identité est affichée clairement dans l'interface.
- Chaque création de Travaux, Incident/Rupture, LTV ou Feedback écrit automatiquement l'auteur actif et l'identifiant de session.
- Le verrouillage du poste reste distinct du changement d'opérateur : déverrouiller ne doit pas, à lui seul, changer l'opérateur actif.
- La clôture présente une synthèse globale, une synthèse par permanent et un historique détaillé.
- Les permanents attendus les mardis et vendredis peuvent être signalés dans l'interface, mais l'absence du deuxième ne doit pas empêcher le premier de travailler.

### 15.3 Préparation SharePoint — schéma cible à confirmer avant implémentation

**Nouvelle liste recommandée :** `Tx_SessionsPermanence`, pour persister chaque session de poste (ne pas dépendre uniquement des variables Power Apps).

Colonnes proposées :
- `Title` (Texte, valeur descriptive de la session).
- `DateDebut` (Date et heure).
- `DateFin` (Date et heure, facultative tant que la session est ouverte).
- `Poste` (Choix : P1, P2, P3).
- `PermanentPrincipalID` (Nombre entier, ID SharePoint de `Ref_Permanents`).
- `PermanentPrincipalNom` (Texte, instantané du nom).
- `PermanentSecondaireID` (Nombre entier, facultatif).
- `PermanentSecondaireNom` (Texte, facultatif).
- `StatutSession` (Choix : En cours, Clôturée, Abandonnée).

Colonnes à ajouter aux listes transactionnelles `Tx_Travaux`, `Tx_LTV`, liste Incidents/Ruptures réelle et liste Feedback réelle :
- `SessionPosteID` (Nombre entier, ID SharePoint de l'élément dans `Tx_SessionsPermanence`).
- `PermanentAuteurID` (Nombre entier, ID SharePoint du permanent dans `Ref_Permanents`).
- `PermanentAuteurNom` (Texte sur une ligne, instantané du nom au moment de l'enregistrement).
- `DateEnregistrement` (Date et heure).
- `PermanentModificateurID` (Nombre entier, facultatif).
- `PermanentModificateurNom` (Texte sur une ligne, facultatif).
- `DateModification` (Date et heure, facultative).

Les colonnes système SharePoint `ID`, `Created` et `Modified` restent disponibles ; les colonnes explicites ci-dessus servent à rattacher les opérations au permanent et à la session métier. Vérifier les noms internes après création. Les colonnes d'auteur ne doivent pas être des colonnes Personne M365 : les permanents sont authentifiés par le référentiel `Ref_Permanents`, pas nécessairement par leur compte Microsoft 365.

**Attention :** les noms exacts des listes Incidents/Ruptures et Feedback ainsi que les schémas réels doivent être confirmés dans `Backend/contextBD.md` et dans SharePoint avant toute création de colonnes. Éviter de créer des doublons si un champ équivalent existe déjà.

### 15.4 Ordre de réalisation proposé

1. Auditer les listes SharePoint et leurs noms internes/types réels.
2. Créer `Tx_SessionsPermanence` et les colonnes de rattachement/auteur après validation du schéma.
3. Implémenter la création et la persistance de la session de permanence.
4. Implémenter l'ajout initial ou tardif du deuxième permanent et le changement d'opérateur avec PIN.
5. Afficher l'opérateur actif et injecter automatiquement son identité dans les Patch des quatre familles d'opérations.
6. Préserver l'auteur initial et enregistrer les informations de modification.
7. Construire les trois vues de clôture : globale, individuelle et historique détaillé.
8. Tester avec deux permanents, y compris changement d'opérateur, verrouillage/déverrouillage, ajout tardif et clôture.

Aucun YAML ni formulaire n'est modifié par cette décision de backlog. Les changements de schéma SharePoint et de code restent à réaliser après audit.

## 16. État réel des écrans et du backend — vérification de main — 17/11/2026

Cette section fait foi pour l'état technique constaté dans les fichiers actuellement présents sur la branche main. Elle corrige les statuts devenus obsolètes des sections 13 à 15, sans supprimer l'historique des décisions.

### 16.1 Verrouillage du poste — présent dans les YAML de main

| Écran | Verrouillage automatique après 10 min | Verrouillage manuel | Déverrouillage par PIN |
|---|---|---|---|
| PrisePoste_2 | Présent (LockTimer_PO, 600 000 ms) | Présent | Présent |
| JournalDeBord_3 | Présent (LockTimer_JB, 600 000 ms) | Présent | Présent |
| scrFeedback | Présent (LockTimer_FB, 600 000 ms) | Présent | Présent |
| scrCloture_2 | Présent (LockTimer_CL, 600 000 ms) | Présent | Présent |
| scrIdentificationAgent | Non applicable | Non applicable | Authentification initiale par PIN |

- Les quatre écrans opérationnels ont un overlay de verrouillage et une action de déverrouillage.
- Le PIN accepté est celui du permanent principal ou du deuxième permanent déclaré, selon la formule présente dans les YAML.
- Le déverrouillage conserve la session Power Apps en mémoire ; il ne doit pas être confondu avec un changement d'opérateur.
- Journal, Feedback et Clôture possèdent également un timer de surveillance des champs de saisie pour réinitialiser le délai lors de changements détectés. Prise de poste réinitialise principalement le timer via les événements des contrôles.
- À valider dans Power Apps Studio : chronométrer réellement les 10 minutes sur chaque écran ; vérifier les interactions non détectées (défilement, clics sur contrôles sans événement instrumenté, navigation) ; tester PIN valide/invalide des deux permanents et vérifier qu'aucune donnée saisie n'est perdue.
- Le verrouillage protège l'interface partagée ; il ne remplace pas les autorisations SharePoint côté serveur.

Correction de statut : les affirmations des sections 13 et 14 selon lesquelles le verrouillage automatique n'existait pas sont historiques et ne décrivent plus les fichiers actuellement présents sur main. Le verrouillage automatique et manuel est maintenant présent dans les quatre écrans opérationnels audités.

### 16.2 Versions des écrans auditées sur main

| Fichier | SHA du contenu vérifié |
|---|---|
| Frontend/Ecran 1 Prise de poste/scrIdentificationAgent.yaml | a1e69abbc909c0d6e3a1e93707bc393ca73f362a |
| Frontend/Ecran 1 Prise de poste/PrisePoste_2.yaml | 5ec1d7105c0f01b8c3726d242064d116f2d774a4 |
| Frontend/Ecran 2 Journal de bord/JournalDeBord_3.yaml | 79503fb6e122745a6d73653dcf202d8949cb7c98 |
| Frontend/Ecran Feedback/scrFeedback.yaml | e4e59c45c15a91590bcb6cd74492ce22ad8390b8 |
| Frontend/Ecran 4 Cloture et releve/scrCloture_2.yaml | 9e5aff180ee35140e8da42100e177ab5912e15d4 |

Ces SHA identifient les contenus audités sur main le 17/11/2026. Ils ne prouvent pas que Power Apps Studio contient exactement ces mêmes fichiers ni que l'import et la recette fonctionnelle ont été réalisés.

### 16.3 Backend SharePoint — colonnes déjà présentes dans les exports

L'audit des exports JSON de Backend/schemas_export/ dans main a confirmé :

- La liste Tx_SessionsPermanence existe et contient notamment DateDebut, DateFin, Poste, PermanentPrincipalID, PermanentPrincipalNom, PermanentSecondaireID, PermanentSecondaireNom et StatutSession.
- Les quatre listes transactionnelles exportées — Tx_Travaux, Tx_LTV, Tx_incidents_Ruptures et Tx_Feedbacks — contiennent les champs SessionPosteID, PermanentAuteurID, PermanentAuteurNom, DateEnregistrement, PermanentModificateurID, PermanentModificateurNom et DateModification.

Conséquence : ne pas recréer ces listes ou colonnes. La priorité est désormais de raccorder les écrans à ce schéma existant et de confirmer dans l'environnement SharePoint cible que les exports correspondent bien à la structure publiée.

Documentation à synchroniser : Backend/contextBD.md décrit encore un ancien schéma (six listes) et ne documente pas correctement la liste de sessions ni les champs d'audit. Mettre ce document à jour à partir des exports JSON vérifiés.

### 16.4 Fonctionnalités encore à développer dans les écrans

| ID | Action restante | Statut au 17/11/2026 | Critère d'acceptation |
|---|---|---|---|
| SESSION-01 | Créer une session SharePoint dans Tx_SessionsPermanence au démarrage de la prise de poste | À faire | Un élément est créé avec date de début, poste, permanent principal et statut « En cours » ; son ID est conservé dans varSessionPoste ou variable dédiée. |
| SESSION-02 | Retrouver/rétablir la session après navigation ou rechargement | À faire | L'application retrouve la session ouverte et ne crée pas une deuxième session par erreur. Prévoir une réauthentification PIN si nécessaire. |
| POSTE-20 | Proposer l'ajout du deuxième permanent après l'authentification du premier | À faire | Le premier peut continuer immédiatement ; « Plus tard » n'empêche aucune opération, y compris mardi/vendredi. |
| POSTE-21 | Ajouter un deuxième permanent à une session déjà commencée | À faire | Le permanent est sélectionné dans Ref_Permanents, authentifié par son PIN et rattaché à la session persistée. |
| POSTE-22 | Changer l'opérateur actif par bouton et PIN | À faire | Le bouton affiche les permanents associés ; le PIN du permanent sélectionné est vérifié ; la session de poste n'est pas recréée. |
| POSTE-23 | Afficher clairement l'opérateur actif | À faire | Le nom de l'opérateur actuellement authentifié est visible sur les écrans opérationnels. |
| AUD-04 | Alimenter automatiquement les champs d'auteur et de session à chaque création | À faire | Chaque Patch de Travaux, LTV, Incident/Rupture et Feedback renseigne l'ID de session, l'ID/nom de l'auteur actif et la date d'enregistrement. |
| AUD-05 | Alimenter les champs de modification sans écraser l'auteur initial | À faire | Les modifications renseignent le modificateur et la date ; les champs d'auteur initial restent inchangés. |
| CLOT-12 | Calculer une synthèse globale à partir de la session persistée | À faire | Les opérations rattachées à l'ID de session sont comptées une seule fois. |
| CLOT-13 | Afficher une synthèse individuelle par permanent | À faire | Les opérations sont réparties selon PermanentAuteurID/PermanentAuteurNom. |
| CLOT-14 | Afficher l'historique détaillé des opérations de la session | À faire | Chaque ligne affiche le type, le titre/identifiant, l'auteur et la date ; le dernier modificateur est affiché si renseigné. |
| DOC-01 | Synchroniser Backend/contextBD.md avec les exports JSON | À faire | Toutes les listes, colonnes, types et choix actuels sont documentés ; les divergences sont signalées. |

### 16.5 Ordre de réalisation actualisé

1. Prise de poste : implémenter la création persistante de session dans Tx_SessionsPermanence et conserver son ID.
2. Gestion des permanents : ajouter le deuxième permanent après connexion ou ultérieurement, sans bloquer le premier.
3. Opérateur actif : implémenter le changement d'opérateur par sélection + PIN et afficher l'identité active.
4. Traçabilité : raccorder les Patch des quatre listes transactionnelles aux champs d'auteur, de session et de modification.
5. Clôture : produire les synthèses globale et individuelle ainsi que l'historique détaillé.
6. Documentation et recette : synchroniser contextBD.md puis tester les parcours complets dans Power Apps Studio et contrôler les éléments SharePoint créés.

### 16.6 Périmètre de cette vérification

- Audit statique des cinq YAML et des exports de schéma sur main.
- Aucun YAML n'a été modifié pendant cet audit.
- Aucun test d'exécution Power Apps Studio ni test réel SharePoint n'a été réalisé dans le cadre de cette vérification.
- Ne pas déclarer les fonctionnalités « terminées » sur la seule base de la présence d'un contrôle ou d'une formule dans le YAML.



## 17. Audit des nouveaux commentaires métier — 20/11/2026

Audit réalisé sur les fichiers actuellement présents dans `main`, notamment :
- `Frontend/Ecran 1 Prise de poste/PrisePoste_2.yaml` — contenu SHA `3fa86f8938878405ab2ce746792665265b83b8a6`.
- `Frontend/Ecran 2 Journal de bord/JournalDeBord_3.yaml` — contenu SHA `79503fb6e122745a6d73653dcf202d8949cb7c98`.
- Exports backend `Backend/schemas_export/Tx_LTV.json` — SHA `0da994aee06e2fd0296e22058451848aa236eb49`.
- Export backend `Backend/schemas_export/Tx_incidents_Ruptures.json` — SHA `7a36977c5262b799258f2c3a9cb760907da89708`.

Cette section complète les sections précédentes et fait foi pour les nouveaux commentaires examinés. Elle ne vaut pas validation fonctionnelle dans Power Apps Studio.

### 17.1 Succession automatique des postes et éléments en cours

| ID | Commentaire / action | État constaté | Statut backlog / critère |
|---|---|---|---|
| POSTE-24 | À la connexion suivante, rendre accessible uniquement le poste successeur (P1 → P2 → P3 → P1) | Non implémenté dans le YAML audité : `OnVisible` calcule un poste suggéré selon l'heure et les boutons P1/P2/P3 restent sélectionnables. | À faire. Déterminer le poste précédent réellement clôturé et appliquer la succession métier, sans confondre l'heure actuelle avec le poste successeur. |
| POSTE-25 | N'afficher que les Travaux réellement en cours dans les éléments à reprendre | Partiellement implémenté : galerie Travaux filtrée par `IsBlank(Heures_Degagement)`. La formule ne vérifie pas explicitement le statut de chantier ni le poste successeur. | À valider / améliorer. Confirmer que l'absence de dégagement est le critère métier officiel et que seuls les chantiers attendus sont affichés. |
| POSTE-26 | N'afficher que les incidents réellement en cours dans les éléments à reprendre | Partiellement implémenté : la galerie utilise `IsBlank(Heure_Fin) || Etat.Value = "En cours" || IsBlank(Etat)`. Cette condition peut inclure des enregistrements incomplets ou incohérents. | À corriger. Définir une règle unique basée sur le statut réel et vérifier les données historiques. |
| POSTE-27 | N'afficher que les LTV actives dans les éléments à reprendre | Présent partiellement : filtre sur `Imposée` et ancienne valeur `Imposée (Active)`. Le schéma JSON actuel ne documente que `Imposée` et `Supprimée`. | À corriger / valider : retirer l'ancienne valeur si elle n'existe plus dans l'environnement et filtrer sur le statut Choice exact. |

### 17.2 LTV par poste — imposition et suppression

Constat : l'écran Journal de bord possède déjà un formulaire LTV avec statut `Imposée` / `Supprimée`, date d'imposition, date de suppression, canton, PK début/fin, taux, motif et acteur lié. Les LTV supprimées sont visuellement différenciées en vert dans la galerie et les imposées en rouge. Le formulaire et les données sont donc partiellement présents ; le commentaire n'est pas entièrement couvert.

L'export actuel de `Tx_LTV` confirme notamment :
- `Statut_LTV` : Choice `Imposée` / `Supprimée`.
- `Date_imposition` et `Date_Suppression` : DateTime.
- `CantonID_` : Lookup vers le référentiel des cantons.
- `PK_Debut`, `PK_Fin`, `Taux` : Number.
- `ActeurID0` : Lookup vers le référentiel des acteurs.
- Les champs de rattachement de session et d'audit existent déjà.

| ID | Action | État constaté | Statut backlog / critère |
|---|---|---|---|
| LTV-01 | Distinguer clairement les rubriques Imposition et Suppression | Partiellement présent via statut, dates et couleur ; séparation fonctionnelle complète à confirmer dans l'UX. | À valider / compléter. Les deux parcours doivent afficher les champs propres à l'action. |
| LTV-02 | Afficher la date de suppression | Champ SharePoint et contrôle présents. | Présent dans le code / à valider fonctionnellement. |
| LTV-03 | Afficher la région et déterminer automatiquement la zone kilométrique correspondante | Non démontré dans le YAML LTV audité ; l'enregistrement référence le canton et les PK, mais aucun champ Région n'est visible dans le schéma Tx_LTV examiné. | À faire / dépendance backend à auditer. Vérifier le référentiel des cantons et ses bornes PK avant de définir le calcul. |
| LTV-04 | Afficher le canton | Lookup canton présent dans le formulaire. | Présent dans le code / à valider. |
| LTV-05 | Enregistrer l'auteur de la suppression (CDT, CBR, etc.) | Le champ `ActeurID0` existe et est utilisé comme acteur associé ; il faut confirmer qu'il représente bien l'auteur de la suppression et qu'il est renseigné distinctement lors d'une suppression. | À clarifier / compléter. Ne pas confondre acteur associé à la LTV et auteur de l'action de suppression. |
| LTV-06 | Comptabiliser le nombre de LTV par région | Non démontré. Un compteur global Imp/Sup existe, mais pas de regroupement fiable par région. | À faire. Calculer les totaux par région à partir du référentiel et des LTV, sans double comptage. |
| LTV-07 | Reprendre les mêmes informations pour l'imposition | Date d'imposition, canton, PK, taux et acteur sont présents dans le modèle actuel. La logique métier et la présentation dédiée restent à vérifier. | Présent partiellement / à valider. |

### 17.3 Momentum incident

L'export de `Tx_incidents_Ruptures` contient actuellement `DateIncident` (date seule), `Heure_D_x00e9_but`, `Heure_Fin`, `PK` (texte), `Etat` (Choice : `Consolidée`, `Traitée`, `En cours`), `CantonID0` (Lookup) et `Commentaires`. Il ne contient pas de colonnes distinctes pour toutes les étapes horaires demandées ni de champ dédié à l'acteur responsable du traitement.

| ID | Action | État constaté | Statut backlog / critère |
|---|---|---|---|
| INC-01 | Enregistrer l'heure de déclaration | Partiellement couvert : date et heure de début existent, mais leur correspondance exacte avec l'heure de déclaration doit être confirmée. | À clarifier / compléter. |
| INC-02 | Enregistrer l'heure d'engagement | Non démontré dans le formulaire Incident/Rupture ni dans le schéma actuel. | À faire. |
| INC-03 | Enregistrer les heures d'intervention | Non démontré ; aucun champ dédié aux heures d'intervention multiples n'est présent dans le schéma examiné. | À faire. Définir si une ou plusieurs interventions peuvent être enregistrées. |
| INC-04 | Enregistrer le PK exact | Partiellement couvert : champ `PK` texte présent, sans validation de format ou de précision démontrée. | À valider / améliorer. |
| INC-05 | Gérer les états En cours, Consolidation et Réparation définitive | Partiellement couvert : Choice actuel `En cours`, `Consolidée`, `Traitée`. Le libellé et la sémantique de `Traitée` ne sont pas équivalents de façon certaine à « Réparation définitive ». | À clarifier puis adapter. Ne pas renommer les choix SharePoint sans validation métier. |
| INC-06 | Identifier l'acteur responsable du traitement | Non démontré comme champ métier distinct ; `AgentSaisie` et les champs d'auteur/audit ne remplacent pas nécessairement le responsable du traitement. | À faire / dépendance schéma à confirmer. |

### 17.4 Vue globalisante quotidienne des LTV et impact trains

| ID | Action | État constaté | Statut backlog / critère |
|---|---|---|---|
| GLOB-01 | Consolider les LTV de tous les postes sur une journée | Partiellement présent : le Journal contient un filtre de périmètre « Journée complète », mais la vue et sa formule doivent être vérifiées pour garantir l'inclusion exacte de P1, P2 et P3 sur la date choisie. | À valider / compléter. |
| GLOB-02 | Afficher l'impact sur les trains marchandises et voyageurs | Non démontré dans le formulaire LTV ni dans le schéma Tx_LTV examiné. | À faire. Définir les champs ou la règle de calcul et la source des circulations impactées. |
| GLOB-03 | Afficher les LTV actives en cours dans la vue globale | Le statut `Imposée` existe ; une vue agrégée quotidienne consolidant les trois postes n'est pas démontrée. | À faire / compléter. |
| GLOB-04 | Remplacer le fichier Excel global LTV par une vue consolidée dans l'application | Non implémenté comme livrable complet. | À faire. Définir les filtres date, poste, région, canton, statut et les colonnes du fichier Excel de référence. |

### 17.5 Ajout du poste P (2x12) et poste exceptionnel

| ID | Action | État constaté | Statut backlog / critère |
|---|---|---|---|
| POSTE-28 | Ajouter le poste P (2x12) | Non présent dans les choix P1/P2/P3 visibles et non documenté dans le schéma actuel des colonnes Choice Poste. | À clarifier puis à faire. Confirmer le sens opérationnel de P (2x12), ses horaires et sa relation avec les postes existants avant de modifier les choix SharePoint. |
| POSTE-29 | Permettre une saisie libre pour un poste exceptionnel / force majeure | Non démontré. Le poste de session et les postes transactionnels utilisent actuellement des choix structurés P1/P2/P3. | À clarifier puis à faire. Définir si la saisie libre doit être stockée dans une colonne dédiée ou dans un champ descriptif, sans casser les filtres et statistiques existants. |

### 17.6 Points de vigilance backend

- Ne pas créer de doublons de colonnes : les champs de session et d'audit existent déjà dans les exports transactionnels.
- Le schéma Tx_LTV confirme les dates d'imposition/suppression, le canton, les PK, le taux, l'acteur associé et les statuts, mais pas une région ni un champ explicite « auteur de suppression ».
- Le schéma Tx_incidents_Ruptures ne confirme pas les trois étapes horaires demandées ni un acteur responsable du traitement.
- Le schéma actuel utilise les choix P1/P2/P3. L'ajout de P (2x12) doit être préparé avec une vérification des dépendances Power Apps, SharePoint et des filtres existants.
- Les calculs région/km doivent s'appuyer sur le référentiel officiel des cantons et ses bornes PK ; ne pas déduire une région depuis un libellé ou inventer des bornes.
- Les statuts « présent dans le code » restent à tester dans Power Apps Studio et sur SharePoint.

### 17.7 Ordre recommandé pour ces nouveaux commentaires

1. Clarifier et implémenter la règle de succession des postes, sans se limiter à une suggestion horaire.
2. Fiabiliser les filtres des éléments réellement en cours sur la prise de poste.
3. Auditer le référentiel des cantons et définir la correspondance région / bornes PK.
4. Compléter les rubriques LTV Imposition / Suppression et les compteurs par région.
5. Définir le modèle des étapes horaires et du responsable pour les incidents.
6. Concevoir la vue globale quotidienne LTV et la mesure d'impact trains.
7. Clarifier le poste P (2x12) et le mécanisme de poste exceptionnel.
8. Réaliser les tests Power Apps Studio et contrôler les données SharePoint avant de passer les tâches à « validé ».



### 17.8 Correction de l'état SESSION-01 / SESSION-02 après audit du YAML actualisé

Le YAML `PrisePoste_2.yaml` actuellement présent sur `main` (SHA `3fa86f8938878405ab2ce746792665265b83b8a6`) contient désormais :
- la recherche de sessions `En cours` du même poste dans une fenêtre glissante de 12 heures ;
- la reprise si le permanent connecté est principal ou secondaire ;
- l'ajout du permanent connecté comme secondaire lorsqu'une session candidate du même poste possède un emplacement secondaire libre ;
- la création d'une session si aucune session candidate n'est réutilisable ;
- la conservation de l'enregistrement dans `varSessionPoste` ;
- la restauration des permanents principal et secondaire depuis leurs IDs SharePoint après sélection de la session.

En conséquence, les statuts historiques de la section 16.4 doivent être lus ainsi :
- `SESSION-01` : **Terminé (code) / À valider** — création persistée présente dans le YAML, mais tests réels SharePoint et Power Apps Studio non fournis.
- `SESSION-02` : **Partiellement implémenté / À valider** — recherche et reprise au clic sur « Valider ma prise de poste » présentes ; aucune restauration automatique de session n'est exécutée dans `OnVisible` après rechargement de l'application.

Cette correction ne valide pas la règle de succession automatique des postes, qui reste suivie séparément par `POSTE-24`. Aucun test d'exécution Power Apps Studio n'a été réalisé lors de cet audit.

## 18. Journal de bord — motifs tardifs et mouvements travaux — 25/11/2026

Fichier modifié : `Frontend/Ecran 2 Journal de bord/JournalDeBord_3.yaml` (ciblé, aucune refonte).

### 18.1 Motifs d'engagement / dégagement tardif (JOUR-13)
- Existant conservé : `MotifEngTardifInput_24` et `MotifDegTardifInput_24` (ComboBox, liste de motifs, facultatifs, onglet Travaux), colonnes texte 255 `Motifs_Engagement_Tardif` / `Motif_Degagement_Tardif`, `Patch` par `LookUp(Tx_Travaux, ID = …)` (pas de doublon en modification).
- Ajouté : `MotifEngLibreInput_24` et `MotifDegLibreInput_24` (TextInput, visibles si « Autre »), hauteur des conteneurs `FldMotifEng_24` / `FldMotifDeg_24` ajustée, formule de sauvegarde, restauration en modification (valeur hors liste → « Autre » + texte repris) et `Reset` après enregistrement.
- Aucune colonne SharePoint créée ni modifiée.
- Statut : **Modifié — non validé**. YAML parsé sans erreur ; import/compilation Studio et tests manuels non faits.
- À tester dans Studio : (1) choisir « Autre » → le champ apparaît ; (2) enregistrer avec texte → SharePoint contient le texte ; (3) rouvrir en modification → « Autre » + texte repris ; (4) modifier sans doublon d'ID ; (5) motif de la liste → enregistré tel quel.

### 18.2 Mouvements travaux — BLOQUÉ
- `based_permanence_file/PERMANENCE EQUIPEMENT RECAP POSTE - AOUT 2023.xlsx` analysé (31 feuilles journalières + feuille `District`) : aucune rubrique ni libellé « Mouvement(s) travaux ». Les travaux n'y apparaissent que comme motifs de ralentissement (« Travaux portique en cours », etc.) et dans « Autres situations à suivre ».
- Rien implémenté. Information manquante : structure exacte de la rubrique (colonnes, ordre, valeurs) — onglet/feuille/capture à indiquer, ou définition métier.

## 19. Journal de bord — recherche dans les listes, compteur LTV, permanent, boutons de pied — 25/11/2026

Fichier modifié : `Frontend/Ecran 2 Journal de bord/JournalDeBord_3.yaml`. Tous les points ci-dessous sont **Modifié — non validé** (YAML parsé sans erreur ; import Studio et tests manuels non faits).

| ID | Point | Changement | À tester dans Studio |
|---|---|---|---|
| JOUR-12 (étendu) | Recherche par saisie dans les listes longues | `IsSearchable: =true` (avec `SearchFields` déjà définis) sur `ActorInput_25` (Responsable intervenant), `RegimeInput_25` (dont Motif de ralentissement en LTV), `MotifEngTardifInput_24`, `MotifDegTardifInput_24` | Taper le début d'un mot : la liste se réduit, un clic sélectionne. Vérifier aussi la recherche « contient » (comportement natif de la propriété) |
| JOUR-27 | Erreur « Impossible de convertir la valeur '0 \| Imp 0 \| Sup 0' en nombre » | Cause : le `Switch` de `EventCount_25` renvoyait un nombre (Travaux, Incidents) et un texte (LTV) ; Power Apps type le résultat sur la 1re branche. Correctif : `Text(CountRows(...))` sur Travaux et Incidents. L'enregistrement LTV n'était pas concerné (erreur d'affichage du compteur seulement) | Onglet LTV : plus de message d'erreur, compteur « n \| Imp x \| Sup y » ; compteurs Travaux/Incidents inchangés |
| JOUR-28 (nouveau) | « Permanent au poste » vide | `PermanentInput_24` était un ComboBox filtré sur `Actif.Value = "Oui"` ; remplacé par un TextInput en lecture seule : `Default = Coalesce(varAgentPermanentNom, LookUp(Ref_Permanents, ID = varAgentPermanentID, Title), "")`. Aucune écriture n'utilise ce contrôle (non référencé dans les `Patch`) | Le nom du permanent connecté s'affiche sur Travaux et LTV |
| JOUR-29 (nouveau) | Boutons Feedback / Clôture invisibles après publication | Capture de l'application publiée (agrandie) : le pied de page est visible mais les deux boutons sont réduits à un trait de ~2 px (leur bordure bleue), aux extrémités gauche et droite. Cause probable : `ActionFeedback_25` et `CloseShiftButton_25` n'avaient ni `FillPortions` ni `LayoutMinWidth` dans `Footer_24` (AutoLayout horizontal) ; la largeur `Width` seule n'est pas respectée dans le lecteur publié, alors que `SaveButton_25` et les onglets définissent `FillPortions`. Correctif : `FillPortions: =0` et `LayoutMinWidth` (340 / 350 ; 200 sous 760 px). Le correctif précédent (`Workspace_25` : `FillPortions: =1`, `LayoutMinHeight` 360) est conservé : il évite aussi que le pied de page sorte de la zone visible sur petit écran | Publier et vérifier sur PC et mobile : les deux boutons affichent leur libellé et naviguent vers `scrFeedback` / `scrCloture_2`. Si toujours écrasés, relever la largeur de fenêtre |

Cette liste reste ouverte : le comportement exact de la recherche (début de mot vs contient) et la visibilité du pied de page ne peuvent être confirmés qu'en Studio / application publiée.

| JOUR-30 (nouveau) | Bouton « Changer d'agent » : colonne `Actif` | `Patch(Ref_Permanents, …, {Actif: …})` utilisait `Actif`, alors que `PrisePoste_2`, `scrIdentificationAgent` et `scrCloture_2` utilisent `'Actif '` (avec espace final). Aligné sur `'Actif '`. Le schéma `Ref_Permanents` n'est pas exporté dans `Backend/schemas_export` : nom à confirmer dans Studio | Modifié — non validé. Cliquer « Changer d'agent » puis vérifier dans SharePoint que `Actif` passe à « Non » |

## 20. État d'avancement — 26/11/2026

Légende : **Validé** = confirmé par vos tests ; **Modifié — non validé** = code modifié, import Studio et recette manuelle à faire ; **Bloqué** = information métier manquante ; **À faire**.

| Domaine | Point | État |
|---|---|---|
| Identification / prise de poste | PIN, P1/P2/P3, session partagée | Validé (tests précédents) |
| Prise de poste | Succession stricte des postes (POSTE-24), filtres « en cours » (POSTE-25/26/27), poste P 2x12 et poste exceptionnel (POSTE-28/29) | À faire / décision métier |
| Journal — Travaux | Motifs tardifs : liste + texte libre si « Autre » (JOUR-13) | Modifié — non validé |
| Journal — Travaux | Mouvements travaux | Bloqué : aucune rubrique dans l'Excel de base ; structure à fournir |
| Journal — listes | Recherche par saisie : Responsable intervenant, motifs tardifs, motif de ralentissement LTV (JOUR-12 étendu) | Modifié — non validé |
| Journal — LTV | Erreur de conversion du compteur (JOUR-27) : affichage seulement, l'enregistrement LTV n'était pas touché | Modifié — non validé |
| Journal — formulaire | « Permanent au poste » vide (JOUR-28) | Modifié — non validé |
| Journal — pied de page | Boutons Feedback / Clôture invisibles une fois publiés (JOUR-29) | Modifié — non validé |
| Journal — agent | Colonne `Actif` du bouton « Changer d'agent » (JOUR-30) | Modifié — non validé |
| Journal — validation | Signalement automatique des champs obligatoires manquants | À faire (étape 2) |
| LTV | Région/km automatiques, auteur de suppression, compteurs par région, vue globale quotidienne, impact trains | À faire / dépendance backend |
| Incidents | Étapes horaires, responsable du traitement, durées, états | À faire / décision métier |
| Clôture / relève | Synthèse de performance, transmission persistante | À faire |

Rien dans ce tableau n'est « Validé métier » avant recette dans Power Apps Studio et contrôle des données SharePoint.
