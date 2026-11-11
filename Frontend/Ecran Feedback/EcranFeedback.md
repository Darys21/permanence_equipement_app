# Écran — Feedback terrain

**Écran Power Apps :** `scrFeedback`  
**Source YAML :** `scrFeedback.yaml`

## Objectif

Enregistrer un pointage terrain lié à un chantier Travaux, puis permettre la consultation du résumé et de l'historique des points de contact.

## Parcours utilisateur

1. Ouvrir le pointage depuis un événement Travaux ou le journal.
2. Sélectionner/confirmer le chantier concerné.
3. Renseigner l'heure du pointage.
4. Choisir le mode de contact.
5. Renseigner la localisation exacte (PK) si nécessaire.
6. Indiquer le statut du contact.
7. Ajouter les observations terrain.
8. Enregistrer le pointage et revenir au journal.

## Informations visibles dans le YAML

- Chantier concerné (poste en cours).
- Heure du pointage.
- Mode de contact.
- Localisation exacte (PK).
- Statut du contact.
- Observations terrain.
- Résumé du chantier.
- Historique des pointages.

## Source et relation SharePoint

- Liste : `Tx_Feedbacks`.
- Relation vers le chantier : `TravailID`, qui doit contenir l'ID de l'enregistrement `Tx_Travaux`.
- Le poste courant est porté par `varQuart`.
- L'événement sélectionné est porté par `varFeedbackEvent`.

## Points techniques à contrôler

- Le statut de contact doit respecter le type réel de la colonne SharePoint (Boolean si le schéma actuel le confirme), et non être envoyé comme une valeur Choice.
- Les valeurs du mode de contact doivent correspondre exactement aux choix configurés dans SharePoint.
- Le pointage doit rester rattaché au bon ID Travaux.
- L'historique doit être filtré sur le chantier concerné, et non seulement sur le titre affiché.
- Les messages de succès ne doivent apparaître qu'après confirmation de l'enregistrement.

## État et tests

L'écran et ses sections sont présents dans le YAML. Une note du 05/10 mentionne SaveFeedback comme validé, mais la recette doit être rejouée avec vérification de la ligne SharePoint, de la relation `TravailID`, du statut et de l'historique.

## À clarifier

- L'édition et la suppression d'un pointage sont-elles autorisées ?
- Le feedback doit-il rester limité aux événements Travaux ?
