# Écran — Identification agent

**Écran Power Apps :** `scrIdentificationAgent`  
**Source YAML :** `scrIdentificationAgent.yaml`  
**Source SharePoint :** `Ref_Permanents`

## Objectif

Identifier le permanent qui prend le service avant d'autoriser l'accès à la prise de poste. Le parcours utilise une sélection de nom et un code PIN personnel, et non une identification automatique basée uniquement sur le compte Microsoft 365.

## Parcours utilisateur

1. Le permanent sélectionne son nom dans la liste.
2. Il saisit son code PIN personnel.
3. Il clique sur « VALIDER ET PRENDRE LE POSTE ».
4. L'application vérifie la correspondance entre l'identifiant sélectionné et le PIN.
5. Si les informations sont valides, le statut du permanent sélectionné passe à `Actif = Oui`, les variables de session sont renseignées et l'utilisateur est envoyé vers `PrisePoste_2`.
6. En cas d'erreur, un message indique que le nom ou le PIN est incorrect.

## Contrôles et données

- Source : `Ref_Permanents`.
- Colonne de statut : `Actif` / `Actif ` selon le nom exposé dans Power Apps, de type Choix `Oui` / `Non`.
- Code PIN : colonne `CodePIN`.
- Variables de session : `varAgentPermanent`, `varAgentPermanentNom`, `varAgentPermanentID`, `varAgentAuthentifie`, `varIDShowError`, `varAgentPreselect`.
- Le PIN est saisi dans un champ masqué avec une longueur maximale configurée à 4 caractères dans le YAML synchronisé.

## Règles fonctionnelles

- Aucun accès à l'étape suivante sans sélection d'un permanent et PIN valide.
- Un autre permanent précédemment actif est remis à `Non` par la logique actuelle lors d'une authentification réussie.
- Le changement d'agent depuis la prise de poste doit remettre l'agent précédent à `Non` et vider les variables de session.

## Tests obligatoires

- Nom non sélectionné.
- PIN vide, incorrect et correct.
- Statut SharePoint après authentification.
- Changement d'agent après une session active.
- Rafraîchissement de la liste après Patch.
- Gestion d'un agent déjà actif ou d'une session interrompue.

## Points de vigilance à vérifier

- Confirmer le nom interne exact de la colonne `Actif` dans le connecteur Power Apps.
- Vérifier la propriété utilisée pour récupérer le nom du permanent (`Title` ou champ exposé équivalent) dans les variables de session.
- Un PIN stocké en clair dans une liste SharePoint ne constitue pas une authentification forte. Vérifier les permissions de la liste et la politique de sécurité avant mise en production.
- Prévoir une règle de limitation des tentatives ou de gestion des PIN erronés si nécessaire.
