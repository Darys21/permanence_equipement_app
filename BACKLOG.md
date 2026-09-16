# Backlog du Projet PERMANANCE EQUIPEMENT

---

## Sprint 0 : Préparation & Infrastructure

| ID  | Tâche                              | Description                                                      | Priorité | Statut |
| --- | ----------------------------------- | ---------------------------------------------------------------- | --------- | ------ |
| 0.1 | Créer le site SharePoint           | Créer un site SharePoint dédié pour le projet                 | Élevée  | Done   |
| 0.2 | Créer les listes Master Data       | Créer Ref_Cantons et Ref_Acteurs avec les colonnes appropriées | Élevée  | Done   |
| 0.3 | Créer les listes Transactionnelles | Créer Tx_Travaux, Tx_Feedbacks, Tx_Incidents_Ruptures, Tx_LTV   | Élevée  | Done   |
| 0.4 | Configurer les permissions          | Définir les permissions pour les utilisateurs sur les listes    | Moyenne   | Done   |

---

## Sprint 1 : Écran 1 - Prise de Poste

| ID  | User Story / Tâche               | Description                                                                       | Priorité | Statut     |
| --- | --------------------------------- | --------------------------------------------------------------------------------- | --------- | ---------- |
| 1.1 | US1.1 - Auto-identification       | Configurer l'application pour détecter automatiquement le profil via compte M365 | Élevée  | En cours  |
| 1.2 | US1.2 - Sélection du Quart       | Ajouter un contrôle pour choisir P1, P2 ou P3                                    | Élevée  | À faire   |
| 1.3 | US1.3 - Aspiration des "En Cours" | Afficher les chantiers et LTV non clôturés du poste précédent                 | Élevée  | À faire   |
| 1.4 | Test Écran 1                     | Tester les fonctionnalités de l'écran 1                                         | Moyenne   | À faire   |

---

## Sprint 2 : Écran 2 - Journal de Bord Opérationnel

| ID  | User Story / Tâche                    | Description                                                              | Priorité | Statut   |
| --- | -------------------------------------- | ------------------------------------------------------------------------ | --------- | -------- |
| 2.1 | US2.1 - Saisie guidée des chantiers   | Implémenter les menus déroulants en cascade (Division → Canton)       | Élevée  | À faire |
| 2.2 | US2.2 - Automatisation des horodatages | Ajouter les champs pour les heures clés et calculer les durées/retards | Élevée  | À faire |
| 2.3 | US2.3 - Verrous de cohérence          | Implémenter les vérifications temporelles                              | Élevée  | À faire |
| 2.4 | US2.4 - Gestion des LTV                | Ajouter la fonctionnalité d'ajout/levée de LTV                         | Élevée  | À faire |
| 2.5 | US2.5 - Déclaration des ruptures      | Ajouter la saisie des incidents de rupture de rail                       | Élevée  | À faire |
| 2.6 | Test Écran 2                          | Tester les fonctionnalités de l'écran 2                                | Moyenne   | À faire |

---

## Sprint 3 : Écran 3 - Feedbacks Terrain & Écran 4 - Clôture

| ID  | User Story / Tâche               | Description                                                            | Priorité | Statut   |
| --- | --------------------------------- | ---------------------------------------------------------------------- | --------- | -------- |
| 3.1 | US3.1 - Ajout de feedbacks        | Implémenter l'ajout de feedbacks horodatés rattachés à un chantier | Élevée  | À faire |
| 3.2 | US4.1 - Validation du poste       | Ajouter le bouton de validation du poste                               | Moyenne   | À faire |
| 3.3 | US4.2 - Automatisation du rapport | Créer le flux Power Automate pour générer et envoyer le rapport     | Élevée  | À faire |
| 3.4 | Test Écrans 3 & 4                | Tester les fonctionnalités des écrans 3 et 4                         | Moyenne   | À faire |

---

## Sprint 4 : Tests, Déploiement & Formation

| ID  | Tâche                  | Description                                                      | Priorité | Statut   |
| --- | ----------------------- | ---------------------------------------------------------------- | --------- | -------- |
| 4.1 | Tests d'intégration    | Tester l'intégration Power Apps ↔ SharePoint ↔ Power Automate | Élevée  | À faire |
| 4.2 | Tests utilisateurs beta | Faire tester l'application par des permanents DMI                | Moyenne   | À faire |
| 4.3 | Déploiement            | Partager l'application avec les utilisateurs                     | Moyenne   | À faire |
| 4.4 | Formation               | Former les utilisateurs à l'application                         | Moyenne   | À faire |

## Suivi d'implementation YAML - 21/08/2026

### Fait ou partiellement fait

- Les quatre ecrans prevus existent dans `Concept pages`.
- La selection P1/P2/P3 et la navigation entre les ecrans sont en place.
- Le journal contient les onglets Travaux, LTV et Incidents.
- La selection Division -> Canton est en place.
- La creation des travaux, LTV et incidents utilise `Patch()`.
- Les references de travaux utilisent `Title` et `DateTravaux` selon le schema fourni.
- Les feedbacks sont rattaches a un travail et tries par `HeureContact`.
- Le statut d'un feedback est selectionnable entre `OUI` et `NON`.

### Reste a implementer dans Power Apps

- Afficher les LTV et incidents a reprendre sur l'ecran 1.
- Ajouter les champs PK, motifs et dates manquants dans les formulaires.
- Calculer les durees et retards et valider l'ordre des heures.
- Ajouter la levee d'une LTV et la cloture d'un incident.
- Filtrer les donnees par poste courant.
- Enregistrer le brouillon et la validation de cloture du poste.
- Definir l'edition et la suppression des feedbacks.

### Hors YAML

- Le rapport de fin de poste et son envoi necessitent Power Automate.
- Le verrouillage global et le suivi d'une session de poste necessitent une regle backend.
- Les noms internes SharePoint doivent etre confirmes dans Power Apps, meme si les noms affiches sont connus.
