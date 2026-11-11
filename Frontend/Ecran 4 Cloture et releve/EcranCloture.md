# Écran — Clôture du poste et relève

**Écran Power Apps :** `scrCloture_2`  
**Source YAML :** `scrCloture_2.yaml`

## Objectif

Présenter le bilan du poste, recueillir le commentaire de fin de service, préparer la transmission au poste suivant et demander une confirmation de clôture.

## Organisation visible dans le YAML

L'écran présente trois étapes :

1. **Synthèse & points ouverts**
2. **Commentaire & transmission**
3. **Confirmation**

Les rubriques de synthèse affichées comprennent :

- Chantiers & Travaux.
- LTV / RAL.
- Ruptures / Incidents.
- Feedbacks terrain et points de contact.
- Détail des événements du poste.
- Commentaire de fin de poste.
- Transmission au poste suivant.
- Aperçu du rapport de fin de poste.
- Confirmation de clôture.

## Variables et sources

- Variable d'étape : `varEtapeCloture`.
- Poste : `varQuart`.
- Identité : `varAgentPermanent`, `varAgentPermanentID`, `varAgentPermanentNom`.
- Sources : `Tx_Travaux`, `Tx_LTV`, `Tx_incidents_Ruptures`, `Tx_Feedbacks`, ainsi que les référentiels nécessaires.

## Règles attendues

- Les compteurs et détails doivent porter sur le bon poste et la bonne période.
- Les événements encore ouverts doivent être identifiés clairement.
- Le commentaire de fin de poste doit être conservé si la règle métier prévoit sa persistance.
- La confirmation doit éviter les doubles clôtures.
- Le poste suivant doit pouvoir consulter et reprendre les événements ouverts.
- Le rapport doit reprendre les données réellement enregistrées, pas uniquement les valeurs encore présentes dans les contrôles.

## État connu

L'écran et son parcours en trois étapes sont présents dans le YAML. Les échanges précédents indiquent que la navigation est en place, mais que la transmission automatique n'est pas finalisée. La présence d'un message annonçant la transmission ne prouve pas qu'une mise à jour SharePoint est réalisée.

Le flux de génération et d'envoi du rapport par Power Automate reste à développer/configurer et à tester.

## Tests obligatoires

- Vérifier chaque compteur avec des lignes SharePoint de test.
- Vérifier les événements ouverts et leur destination après relève.
- Tester une clôture sans événement, avec événements ouverts et avec plusieurs catégories d'événements.
- Tester l'échec réseau ou SharePoint pendant la validation.
- Vérifier qu'un double clic ne crée pas deux clôtures/rapports.
- Vérifier le contenu final du rapport et son destinataire.
