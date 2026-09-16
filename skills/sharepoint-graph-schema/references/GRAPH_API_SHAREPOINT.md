# REFERENCES - Microsoft Graph SharePoint

## Vue d'ensemble endpoints Graph v1.0 SharePoint

Documentation off: `https://learn.microsoft.com/fr-fr/graph/api/resources/sharepoint-site?view=graph-rest-1.0`

### 1. Récupérer l'id d'un site via son URL

Format endpoint `GET /sites/{hostname}:/{server-relative-path}`:
```
GET https://graph.microsoft.com/v1.0/sites/erametgroup.sharepoint.com:/sites/PERMANANCEEQUIPEMENT?$select=id,displayName,webUrl
```

Output: `{"id": "erametgroup.sharepoint.com,<guid_1>,<guid_2>", "displayName": "...", "webUrl": "..."}`

L'id site = composite `<hostname>,<siteId>,<webId>` - utiliser tel quel dans les requêtes listes/colonnes.

### 2. Lister toutes les listes d'un site

```
GET https://graph.microsoft.com/v1.0/sites/{site_id}/lists?$select=id,name,displayName,webUrl,list,lastModifiedDateTime,createdDateTime
```

Filtrer sur displayName:
```
GET https://graph.microsoft.com/v1.0/sites/{site_id}/lists?$filter=displayName in ('Ref_Cantons','Ref_Acteurs','Tx_Travaux','Tx_Feedbacks','Tx_incidents_Ruptures','Tx_LTV')
```

### 3. Lister colonnes (schema) d'une liste

RÉCUPÉRER TOUTES LES INFOS COLONNES (y compris type choice/lookup/options):
```
GET https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/columns?$select=name,displayName,description,columnType,required,readOnly,hidden,defaultValue,choice,lookup,number,text,dateTime,boolean,personOrGroup,contentApprovalStatus,hyperlinkOrPicture,isDeletable
```

Exemple réponse colonne choix Division:
```json
{
  "name": "Division",
  "displayName": "Division",
  "columnType": "choice",
  "required": true,
  "readOnly": false,
  "hidden": false,
  "choice": {
    "choices": ["Division 1", "Division 2", "Division 3"],
    "displayAs": "menu",
    "allowTextEntry": false
  }
}
```

Exemple colonne DateHeure:
```json
{
  "name": "Date_travaux",
  "displayName": "Date travaux",
  "columnType": "dateTime",
  "dateTime": {"displayAs": "dateOnly", "format": "locale"}
}
```

Exemple colonne Number:
```json
{
  "name": "PK_Debut",
  "columnType": "number",
  "number": {"decimalPlaces": "none", "displayAs": "number"}
}
```

Exemple colonne texte multiligne:
```json
{
  "name": "Commentaires",
  "columnType": "text",
  "text": {"allowMultipleLines": true, "appendChangesToExistingText": false, "linesForEditing": 6, "maxLength": 63999}
}
```

Exemple personne:
```json
{
  "name": "AgentSaisie",
  "columnType": "personOrGroup",
  "personOrGroup": {"allowMultipleSelection": false, "displayAs": "name", "chooseFromType": "peopleAndGroups"}
}
```

Exemple Lookup natif SharePoint:
```json
{
  "name": "CantonID",
  "columnType": "lookup",
  "lookup": {"listId": "{list GUID}", "columnName": "Title", "allowMultipleValues": false}
}
```

### 4. Autorisations

| Scope | Type | Nécessite admin |
| --- | --- | --- |
| `Sites.Read.All` | Déléguée | Facultatif (consent utilisateur parfois suffisant) |
| `Sites.ReadWrite.All` | Déléguée | Facultatif |
| `Sites.Read.All` | Application | OUI ADMIN GRANT |
| `Sites.Selected` | Application/Déléguée | Administration par site, plus sécuritaire |

### 5. Headers toujours ajouter
```
Authorization: Bearer <access_token>
Accept: application/json
ConsistencyLevel: eventual (optionnel sur certains filtres)
```

### 6. Pagination colonnes list
Chaque réponse contient jusqu'à 200 colonnes. Si plus:
```
$top=200&$skiptoken=<continuation>
```
Rare pour nos 6 listes.

### 7. Map columnType → frontend Power Apps YAML Patch

| columnType Graph | Ecriture Patch Power Fx | Lecture .Value? |
| --- | --- | --- |
| text / note / calculatedText | `Champ: "string"` | Non |
| choice (single) | `Champ: {Value: "valeur"}` | OUI `.Value` |
| choice (multi) | `Champ: ForAll(Items, {Value: Value})` | OUI `.Value` each |
| number / currency | `Champ: Value(TextInput.Text)` ou 123 | Non |
| boolean | `Champ: true/false` | Non |
| dateTime | `Champ: DateTimeValue(Text)` ou `Now()` ou `Today()` | Non |
| personOrGroup single | `Champ: {Claims:"i:0#.f|membership|", Email, DisplayName}` | `.DisplayName / .Email` |
| lookup single | `Champ: {Id: numericId, Value: "label"}` | `.Id / .Value` |
| hyperlinkOrPicture | `Champ: {Url: "...", Description: "..."}` | `.Url / .Description` |
