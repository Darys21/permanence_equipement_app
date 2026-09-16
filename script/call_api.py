"""
Récupération schema 6 listes SharePoint - ZERO configuration admin.
Utilise client id Microsoft Graph Explorer (public app pré-approuvé Microsoft).
Device code flow: copier code → naviguer https://microsoft.com/devicelogin.

pour l'instant inutilisable après avoir tester car bliqué par accès admin pour l'utilisation de Microsoft graph 
"""
from pathlib import Path
import msal, requests, json, yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Backend" / "schemas_export"
OUT.mkdir(parents=True, exist_ok=True)

# === Constantes - A JAMAIS MODIFIER
CLIENT_ID_GRAPH_EXPLORER = "14d82eec-204b-4c2f-b7e8-296a70dab67e"  # Client ID officiel Microsoft Graph Explorer Public
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPES = ["Sites.Read.All"]
GRAPH = "https://graph.microsoft.com/v1.0"

SITE_HOST = "erametgroup.sharepoint.com"
SITE_PATH = "/sites/PERMANANCEEQUIPEMENT"
LISTES = [
    "Ref_Cantons",
    "Ref_Acteurs",
    "Tx_Travaux",
    "Tx_Feedbacks",
    "Tx_incidents_Ruptures",
    "Tx_LTV",
]

SKIP_BUILTIN = {
    "Author","Created","Modified","Editor","Attachments","ContentType",
    "ComplianceAssetId","GUID","ID","Path","_UIVersionString","Version",
    "_HasCopyRestrictions","_ComplianceFlags","_ComplianceTag","_CommentCount",
    "_DisplayName","_IsRecord","_LikeCount","_ModerationComments","_ModerationStatus",
    "_UIVersion","AppAuthor","AppEditor","CheckoutUser","FileDirRef","FileLeafRef",
    "FileRef","File_x0020_Type","MetaInfo","Order","Owshiddenversion","ProgId",
    "ServerRedirectedEmbedUrl","ServerUrl","SyncClientId","TemplateUrl","WorkflowInstanceID",
    "PermMask","FileSizeDisplay","ItemChildCount","FolderChildCount",
    "SMTotalFileCount","SMTotalFileStreamSize","SMTotalSize",
}

# === 1. Auth
app = msal.PublicClientApplication(CLIENT_ID_GRAPH_EXPLORER, authority=AUTHORITY)
flow = app.initiate_device_flow(scopes=SCOPES)
print("=" * 80)
print(flow["message"])
print("=" * 80)
token = app.acquire_token_by_device_flow(flow)["access_token"]
h = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

# === 2. Site ID
r = requests.get(f"{GRAPH}/sites/{SITE_HOST}:{SITE_PATH}?$select=id,displayName", headers=h)
r.raise_for_status()
site = r.json()
SITE_ID = site["id"]
print(f"[OK] Site: {site['displayName']}")
print(f"[OK] Site ID: {SITE_ID}")

# === 3. Bulk list_id via filter
filt = " or ".join([f"displayName eq '{n}'" for n in LISTES])
rl = requests.get(f"{GRAPH}/sites/{SITE_ID}/lists?$filter={filt}&$select=id,displayName", headers=h).json()["value"]
list_ids = {l["displayName"]: l["id"] for l in rl}

# === 4. Colonnes chaque liste
COL_SELECT = (
    "name,displayName,columnType,required,readOnly,hidden,defaultValue,choice,lookup,"
    "number,text,dateTime,boolean,personOrGroup,hyperlinkOrPicture,contentApprovalStatus,"
    "description,isDeletable"
)
compil = {}

for lname in LISTES:
    if lname not in list_ids:
        print(f"[SKIP] Liste absente: {lname}")
        continue
    lid = list_ids[lname]
    url = f"{GRAPH}/sites/{SITE_ID}/lists/{lid}/columns?$select={COL_SELECT}"
    cols = []
    while url:
        rc = requests.get(url, headers=h)
        rc.raise_for_status()
        d = rc.json()
        cols.extend(d.get("value", []))
        url = d.get("@odata.nextLink", "")
    cleaned = [c for c in cols if c.get("name") not in SKIP_BUILTIN]
    (OUT / f"{lname}.json").write_text(json.dumps(cleaned, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] {lname}: {len(cleaned)} colonnes → Backend/schemas_export/{lname}.json")
    compil[lname] = cleaned

# === 5. ALL_COLUMNS.yaml compact
compact = {}
for ln, cols in compil.items():
    compact[ln] = []
    for c in cols:
        entry = {
            "name": c.get("name"),
            "displayName": c.get("displayName", c.get("name")),
            "type": c.get("columnType", "?"),
            "required": c.get("required", False),
            "readOnly": c.get("readOnly", False),
            "hidden": c.get("hidden", False),
        }
        if c.get("description"): entry["description"] = c["description"]
        if c.get("choice"):
            if c["choice"].get("choices"): entry["choices"] = c["choice"]["choices"]
            if c["choice"].get("allowTextEntry"): entry["choice_allow_text"] = True
        if c.get("lookup"):
            entry["lookup_listId"] = c["lookup"].get("listId")
            entry["lookup_column"] = c["lookup"].get("columnName")
            entry["lookup_multi"] = c["lookup"].get("allowMultipleValues", False)
        if c.get("number"): entry["number"] = c["number"]
        if c.get("text"): entry["text"] = c["text"]
        if c.get("dateTime"): entry["dateTime"] = c["dateTime"]
        if c.get("personOrGroup"): entry["personOrGroup"] = c["personOrGroup"]
        if c.get("defaultValue"): entry["defaultValue"] = c["defaultValue"]
        compact[ln].append(entry)
(OUT / "ALL_COLUMNS.yaml").write_text(
    yaml.safe_dump(compact, allow_unicode=True, sort_keys=False, indent=2),
    encoding="utf-8",
)
print(f"[OK] ALL_COLUMNS.yaml généré: Backend/schemas_export/ALL_COLUMNS.yaml")