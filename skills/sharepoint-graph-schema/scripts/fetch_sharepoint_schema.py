"""
fetch_sharepoint_schema.py
=========================
Extrait schema (colonnes, types, options de choix) des 6 listes SharePoint PERMANANCE EQUIPEMENT via Microsoft Graph API.

Authentification: device-code (interactif, defaut) ou client-credentials (batch).
Input: .env a la racine projet (voir references/env.example).
Output: JSON + YAML dans OUTPUT_DIR (defaut Backend/schemas_export/)

Dependances:
    pip install msal requests PyYAML python-dotenv
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import requests
import yaml
from dotenv import load_dotenv
from msal import ConfidentialClientApplication, PublicClientApplication

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

# ====== CONFIG ======
TENANT_ID = os.environ.get("SHAREPOINT_TENANT_ID", "")
CLIENT_ID = os.environ.get("SHAREPOINT_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("SHAREPOINT_CLIENT_SECRET", "") or None
AUTH_MODE = os.environ.get("AUTH_MODE", "device").lower()
SITE_URL = os.environ.get("SITE_URL", "https://erametgroup.sharepoint.com/sites/PERMANANCEEQUIPEMENT")
TARGET_LISTS = [
    s.strip()
    for s in os.environ.get(
        "TARGET_LISTS",
        "Ref_Cantons,Ref_Acteurs,Tx_Travaux,Tx_Feedbacks,Tx_incidents_Ruptures,Tx_LTV",
    ).split(",")
    if s.strip()
]
OUTPUT_DIR = ROOT / os.environ.get("OUTPUT_DIR", "Backend/schemas_export")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES_DELEGATE = ["https://graph.microsoft.com/Sites.Read.All"]
SCOPE_APP = ["https://graph.microsoft.com/.default"]

# Colonnes built-in toujours ignorer (readonly system)
SKIP_INTERNAL_NAMES = {
    "Author", "Created", "Modified", "Editor", "Attachments", "ContentType",
    "ComplianceAssetId", "GUID", "ID", "Path", "_UIVersionString", "Version",
    "_HasCopyRestrictions", "_ComplianceFlags", "_ComplianceTag", "_CommentCount",
    "_DisplayName", "_IsRecord", "_LikeCount", "_ModerationComments",
    "_ModerationStatus", "_UIVersion", "AppAuthor", "AppEditor",
    "CheckoutUser", "FileDirRef", "FileLeafRef", "FileRef", "File_x0020_Type",
    "MetaInfo", "Order", "Owshiddenversion", "ProgId", "ServerRedirectedEmbedUrl",
    "ServerUrl", "SyncClientId", "TemplateUrl", "WorkflowInstanceID",
    "PermMask", "FileSizeDisplay", "ItemChildCount", "FolderChildCount",
    "SMTotalFileCount", "SMTotalFileStreamSize", "SMTotalSize",
}


def acquire_token() -> str:
    if not TENANT_ID or not CLIENT_ID:
        print("ERREUR: SHAREPOINT_TENANT_ID et SHAREPOINT_CLIENT_ID requis dans .env")
        sys.exit(1)

    authority = f"https://login.microsoftonline.com/{TENANT_ID}"

    if AUTH_MODE == "device" or CLIENT_SECRET is None:
        app = PublicClientApplication(CLIENT_ID, authority=authority)
        flow = app.initiate_device_flow(scopes=SCOPES_DELEGATE)
        if "user_code" not in flow:
            raise RuntimeError(f"Device flow echoue: {flow}")
        print("==" * 40)
        print(flow["message"])
        print("==" * 40)
        result = app.acquire_token_by_device_flow(flow)
    elif AUTH_MODE == "client_credentials":
        app = ConfidentialClientApplication(
            CLIENT_ID,
            client_credential=CLIENT_SECRET,
            authority=authority,
        )
        result = app.acquire_token_for_client(scopes=SCOPE_APP)
    else:
        raise RuntimeError(f"AUTH_MODE inconnue: {AUTH_MODE}")

    if "access_token" not in result:
        raise RuntimeError(
            f"Echec acquisition token: {result.get('error_description', result)}"
        )
    print("[OK] Token Graph obtenu.")
    return result["access_token"]


def headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}", "Accept": "application/json"}


def parse_site_host_and_path(url: str) -> tuple[str, str]:
    # https://erametgroup.sharepoint.com/sites/PERMANANCEEQUIPEMENT -> ("erametgroup.sharepoint.com", "/sites/PERMANANCEEQUIPEMENT")
    url = url.rstrip("/")
    if url.startswith("https://"):
        url = url[8:]
    elif url.startswith("http://"):
        url = url[7:]
    host, _, path = url.partition("/")
    if not path.startswith("/"):
        path = "/" + path
    return host, path


def get_site_id(token: str) -> str:
    host, path = parse_site_host_and_path(SITE_URL)
    req = f"{GRAPH}/sites/{host}:{path}?$select=id,displayName,webUrl"
    r = requests.get(req, headers=headers(token))
    r.raise_for_status()
    data = r.json()
    site_id = data["id"]
    print(f"[OK] Site: {data.get('displayName')}")
    print(f"[OK] Site ID: {site_id}")
    return site_id


def get_target_list_ids(token: str, site_id: str) -> list[dict[str, str]]:
    filt = " or ".join([f"displayName eq '{n}'" for n in TARGET_LISTS])
    url = f"{GRAPH}/sites/{site_id}/lists?$filter={filt}&$select=id,name,displayName"
    r = requests.get(url, headers=headers(token))
    r.raise_for_status()
    lists_found = r.json().get("value", [])
    matched: list[dict[str, str]] = []
    for target_name in TARGET_LISTS:
        found = next((l for l in lists_found if l["displayName"] == target_name), None)
        if not found:
            print(f"[WARN] Liste absente: {target_name}")
            continue
        print(f"[OK] Liste: {target_name} => list_id={found['id']}")
        matched.append(found)
    return matched


def list_columns(token: str, site_id: str, list_id: str) -> list[dict[str, Any]]:
    url = (
        f"{GRAPH}/sites/{site_id}/lists/{list_id}/columns?"
        "$select=name,displayName,columnType,required,readOnly,hidden,"
        "defaultValue,choice,lookup,number,text,dateTime,boolean,personOrGroup,"
        "contentApprovalStatus,hyperlinkOrPicture,isDeletable,description"
    )
    all_cols: list[dict[str, Any]] = []
    while url:
        r = requests.get(url, headers=headers(token))
        r.raise_for_status()
        data = r.json()
        all_cols.extend(data.get("value", []))
        url = data.get("@odata.nextLink", "")
    return [c for c in all_cols if c.get("name") not in SKIP_INTERNAL_NAMES]


def write_list_output(display_name: str, columns: list[dict[str, Any]]) -> None:
    json_path = OUTPUT_DIR / f"{display_name}.json"
    json_path.write_text(
        json.dumps(columns, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"  -> {json_path}")


def write_yaml_all(per_list: dict[str, list[dict[str, Any]]]) -> None:
    compact: dict[str, Any] = {}
    for lname, cols in per_list.items():
        compact[lname] = []
        for c in cols:
            entry: dict[str, Any] = {
                "name": c["name"],
                "displayName": c.get("displayName", c["name"]),
                "type": c.get("columnType", "unknown"),
                "required": c.get("required", False),
                "readOnly": c.get("readOnly", False),
                "hidden": c.get("hidden", False),
            }
            if c.get("description"):
                entry["description"] = c.get("description")
            if c.get("choice"):
                entry["choices"] = c["choice"].get("choices", [])
            if c.get("lookup"):
                entry["lookup"] = {
                    "listId": c["lookup"].get("listId"),
                    "columnName": c["lookup"].get("columnName"),
                    "multi": c["lookup"].get("allowMultipleValues", False),
                }
            if c.get("number"):
                entry["number"] = c["number"]
            if c.get("text"):
                entry["text"] = c["text"]
            if c.get("dateTime"):
                entry["dateTime"] = c["dateTime"]
            if c.get("personOrGroup"):
                entry["personOrGroup"] = c["personOrGroup"]
            if c.get("defaultValue"):
                entry["defaultValue"] = c.get("defaultValue")
            compact[lname].append(entry)
    yaml_path = OUTPUT_DIR / "ALL_COLUMNS.yaml"
    yaml_path.write_text(
        yaml.safe_dump(compact, allow_unicode=True, sort_keys=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n[OK] YAML global: {yaml_path}")


def main() -> None:
    token = acquire_token()
    site_id = get_site_id(token)
    lists = get_target_list_ids(token, site_id)
    if not lists:
        print("[ERREUR] Aucune liste cible trouvee.")
        sys.exit(2)
    per_list: dict[str, list[dict[str, Any]]] = {}
    for l in lists:
        cols = list_columns(token, site_id, l["id"])
        print(f"  -> {len(cols)} colonnes pertinentes pour {l['displayName']}")
        write_list_output(l["displayName"], cols)
        per_list[l["displayName"]] = cols
    write_yaml_all(per_list)
    print("\n[TERMINE] Schema exporte avec succes.")


if __name__ == "__main__":
    main()
