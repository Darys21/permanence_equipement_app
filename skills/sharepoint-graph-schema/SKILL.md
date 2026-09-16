---
name: sharepoint-graph-schema
description: Récupère structure exacte listes SharePoint (colonnes, types, choix options) via Microsoft Graph API Device Code Flow ou Client Credentials. Génère JSON + YAML alignable sur frontend Power Apps.
---

## But
Permettre récupération PROGRAMMATIQUE du schéma backend SharePoint réel (6 listes: Ref_Cantons, Ref_Acteurs, Tx_Travaux, Tx_Feedbacks, Tx_incidents_Ruptures, Tx_LTV). Évite déviation entre documentation papier et colonnes backend.

## Quand déclencher
- Avant chaque modification frontend YAML pour vérifier noms colonnes + types exacts
- Après modification colonne SP côté admin, régénérer backend/contextBD.md
- Avant publication nouvelle version app Power Apps, audit frontend vs backend
- Résoudre ambiguïté nom colonne `Date_travaux` vs `DateTravaux`, `Heure_Autorisee` vs `Heures_Autorisee`

## Méthodes authentification supportées

### A - Device Code Flow (RECOMMANDÉ, dev, interactif)
- Entra App Registration type "Public client / native"
- Permissions DELEGUÉES: `Sites.Read.All` + consent admin OU utilisateur
- Credentials requis: `TENANT_ID` + `CLIENT_ID` (pas de secret)
- MFA compatible. Sécurisé.

### B - Client Credentials (batch, automatisé)
- App Registration type "Web" avec secret/certificat
- Permissions APPLICATION: `Sites.Read.All` + ADMIN GRANT OBLIGATOIRE
- CRÉDENTIALS TENANT_ID + CLIENT_ID + CLIENT_SECRET

### C - SharePoint App-Only (legacy ACS)
- Support optionnel via script `sharepoint_acc_only.py`
- Non recommandé Microsoft 365 modern

## Prérequis Python
```bash
pip install msal requests PyYAML rich python-dotenv
```

## Workflow standard

1. Créer `.env` (template dans references/env.example):
   ```
   SHAREPOINT_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   SHAREPOINT_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   SHAREPOINT_CLIENT_SECRET=<optionnel B seulement>
   AUTH_MODE=device | client_credentials
   SITE_URL=https://erametgroup.sharepoint.com/sites/PERMANANCEEQUIPEMENT
   TARGET_LISTS=Ref_Cantons,Ref_Acteurs,Tx_Travaux,Tx_Feedbacks,Tx_incidents_Ruptures,Tx_LTV
   OUTPUT_FORMAT=json,yaml
   OUTPUT_DIR=Backend/schemas_export/
   ```
2. Exécuter: `python skills/sharepoint-graph-schema/scripts/fetch_sharepoint_schema.py`
3. Device Code Flow affiche URL + code → utilisateur valide dans navigateur
4. Script produit:
   - `Backend/schemas_export/<Liste>.json` → colonnes brutes Graph (name, displayName, description, columnType, choice.values, lookup, text.maxLength, number.decimalPlaces, readOnly, required, hidden, defaultValue)
   - `Backend/schemas_export/ALL_COLUMNS.yaml` → condensé 6 listes
   - Mise à jour `Backend/contextBD.md` avec types exactes (optionnel avec flag --update-contextbd)

## Endpoints Graph utilisés (v1.0)
- Récupération site ID:
  `GET https://graph.microsoft.com/v1.0/sites/{tenant_hostname}:/sites/{site_relative_path}?$select=id,displayName,webUrl`
- Listes ciblées:
  `GET https://graph.microsoft.com/v1.0/sites/{site_id}/lists?$filter=displayName in ('A','B',...)`
- Colonnes 1 liste:
  `GET https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/columns?$select=name,displayName,columnType,readOnly,required,hidden,defaultValue,choice,lookup,number,text,dateTime,boolean,personOrGroup,contentApprovalStatus,hyperlinkOrPicture,thumbnail,isDeletable,description`
- Valeurs 1 Choix colonne: `column['choice']['choices']` Array
- Colonnes READ_ONLY built-in filtrées: Author, Created, Modified, Editor, Attachments, ContentType, ComplianceAssetId, GUID, ID, Path, _UIVersionString, Version

## Patch frontend automatique (scripts/generate_patch_yaml.py)
Après export:
```
python skills/sharepoint-graph-schema/scripts/align_frontend_yaml.py \
  --schemas Backend/schemas_export/*.json \
  --input Concept\ pages/Ecran\ 2\ Journal\ de\ bord/dashboard.yaml \
  --output Concept\ pages/Ecran\ 2\ Journal\ de\ bord/dashboard.aligned.yaml
```
Règles alignement:
- Si colonne backend "Date_travaux" type date → corriger frontend `DateTravaux` → `Date_travaux` partout
- Si colonne Poste type "choice" backend → transformer `Poste = varQuart` en `Poste: {Value: varQuart}` en écriture, `.Value` en lecture
- Si CantonID type lookup record → transformer `Selected.ID` en `{Id: Selected.ID, Value: Selected.Title}`

## Vérifications toujours faire
1. Comparer sortie `ALL_COLUMNS.yaml` avec Backend/contextBD.md section existante.
2. Confirmer valeur exacte des options Choix backend avant écriture frontend.
3. Ne jamais faire hypothèse "Division est type Choix"; toujours se baser sur colonne['columnType'] = 'choice'.
4. Toujours filtrer colonnes readonly built-in avant patch (Author/Created/Modified etc).

## Erreurs fréquentes
| Erreur | Cause | Solution |
| --- | --- | --- |
| InvalidClient | TENANT_ID ou CLIENT_ID faux | Vérifier portal Azure App Registration |
| 403 Forbidden | Droits insuffisants | Ajouter permission déléguée Sites.Read.All, consent |
| 404 site not found | SITE_URL typo | Utiliser format exact `https://<tenant>.sharepoint.com/sites/<site_path>` |
| List inconnue filter | Nom liste différent casse | Lister d'abord toutes listes sans filtre |
