# Écran — Prise de poste

**Écran Power Apps :** `PrisePoste_2`  
**Source YAML :** `PrisePoste_2.yaml`

## Objectif

Permettre au permanent identifié de sélectionner son poste, consulter les éléments à reprendre et démarrer le service.

## Parcours utilisateur

1. À l'ouverture, l'écran vérifie la présence de `varAgentPermanentID` et `varAgentPermanentNom`. Si l'identité manque, retour vers `scrIdentificationAgent`.
2. Les référentiels et listes transactionnelles sont actualisés.
3. Le poste est suggéré à partir de l'heure locale :
   - P1 : 06h00–14h00 ;
   - P2 : 14h00–22h00 ;
   - P3 : 22h00–06h00.
4. Le permanent peut conserver la suggestion ou choisir manuellement P1, P2 ou P3.
5. Il consulte les éléments à reprendre.
6. Il démarre le service et accède au journal de bord.

## Éléments à reprendre affichés

- Chantiers et travaux en cours (`Tx_Travaux`).
- LTV/RAL actifs (`Tx_LTV`).
- Incidents et ruptures en cours (`Tx_incidents_Ruptures`).

## Variables et données

- Identité : `varAgentPermanent`, `varAgentPermanentNom`, `varAgentPermanentID`.
- Poste : `varQuartSuggere`, `varQuart`.
- Référentiels rafraîchis : `Ref_Cantons`, `Ref_Acteurs`, `Ref_Permanents`.
- Listes transactionnelles rafraîchies : `Tx_Travaux`, `Tx_LTV`, `Tx_incidents_Ruptures`, `Tx_Feedbacks`.

## Règles fonctionnelles confirmées dans les échanges

- Les trois postes P1, P2 et P3 sont conservés.
- La suggestion horaire ne remplace pas le choix manuel.
- Le deuxième permanent est facultatif.
- La succession ne doit pas devenir un verrou empêchant la prise de poste.
- L'accès au journal nécessite un agent et un poste définis.

## À valider

- Les filtres exacts des éléments à reprendre et leur continuité d'un poste au suivant.
- La cohérence entre le poste sélectionné et le champ `Poste` des listes SharePoint.
- Le parcours complet P1/P2/P3, y compris les changements d'agent.
- Le cas d'un poste exceptionnel, qui nécessite une règle métier et un modèle de données dédiés.
- La transmission réelle des événements ouverts : leur affichage sur cet écran ne suffit pas à prouver qu'ils sont transférés ou réaffectés dans SharePoint.
