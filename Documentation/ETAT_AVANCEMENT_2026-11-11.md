# État du projet — 11/11/2026

## Situation générale

L'application est en phase de stabilisation fonctionnelle. Les écrans et les principaux parcours existent, mais le Journal de bord reste le principal risque avant une recette complète.

## État par écran

| Écran | Source actuelle | État |
|---|---|---|
| Identification agent | `scrIdentificationAgent.yaml` | Sélection + PIN + statut actif intégrés ; scénarios d'erreur à tester. |
| Prise de poste | `PrisePoste_2.yaml` | P1/P2/P3, suggestion horaire, choix manuel et éléments à reprendre présents ; tests de bout en bout à finaliser. |
| Journal de bord | `JournalDeBord_3.yaml` | Travaux création confirmée ; modification avec ID stable à corriger ; LTV création/reprise à retester ; incidents à auditer. |
| Feedback terrain | `scrFeedback.yaml` | Écran et mécanismes de sauvegarde présents ; validation SharePoint/historique à rejouer. |
| Clôture et relève | `scrCloture_2.yaml` | Parcours en étapes et synthèse présents ; transfert réel des événements et automatisation du rapport non finalisés. |

## Priorités immédiates

1. Corriger le mode modification Travaux pour préserver l'ID.
2. Corriger et tester création/reprise/modification LTV.
3. Auditer les opérations CRUD Incidents/Ruptures.
4. Vérifier les types et noms internes SharePoint.
5. Tester le parcours complet identification → prise de poste → journal → feedback → clôture.
6. Finaliser la transmission au poste suivant et le rapport de fin de poste.
7. Organiser une recette avec les permanents.

## Règle de qualité

Aucune fonctionnalité ne passe au statut « validée » sur la seule base de sa présence dans le YAML. La validation exige un test dans Power Apps, une vérification de la donnée SharePoint enregistrée et un contrôle des cas d'erreur.
