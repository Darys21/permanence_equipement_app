import json
from pathlib import Path

base = Path(r"c:\Users\jyd.anguilet\Downloads\Joan - SETRAG\PERMANANCE EQUIPEMENT\Backend\schemas_export")
SKIP = {
    "Author","Created","Modified","Editor","Attachments","ContentType","ComplianceAssetId",
    "GUID","ID","Path","_UIVersionString","Version","_HasCopyRestrictions",
    "_ComplianceFlags","_ComplianceTag","_CommentCount","_DisplayName","_IsRecord",
    "_LikeCount","_ModerationComments","_ModerationStatus","_UIVersion","AppAuthor",
    "AppEditor","CheckoutUser","FileDirRef","FileLeafRef","FileRef","File_x0020_Type",
    "MetaInfo","Order","Owshiddenversion","ProgId","ServerRedirectedEmbedUrl","ServerUrl",
    "SyncClientId","TemplateUrl","WorkflowInstanceID","PermMask","FileSizeDisplay",
    "ItemChildCount","FolderChildCount","SMTotalFileCount","SMTotalFileStreamSize",
    "SMTotalSize","SortPriority","OriginalSourcePath","IsCurrentVersion","PolicyDisabled",
    "Thumbnail","_SourceUrl","_SharedFileIndex","LinkFilenameNoMenu","LinkFilename",
    "File_x0020_Size","InstanceID","SortBehavior","FSObjType","ParentUniqueId","StreamHash",
    "CheckedOutUserId","WorkflowVersion","CheckedOutTitle","VirusStatus","CheckedOutTo",
    "SMTotalCountInFolder","ScopeId","UniqueId","NoExecute","_Level","_IsCurrentVersion",
    "_HasCopyDestinations","CopySource","owshiddenversion","ContentTypeId","WikiField",
    "CanvasContent1","BannerImageUrl","FirstPublishedDate","PageLayoutType","PromotedState",
    "ScheduledArchiveEndDate","ScheduledArchiveStatus","ScheduledPublishDate",
    "CommentsDisabled","LikeCount","LikedBy","CommentCount","ComplianceAssetId",
}

for p in sorted(base.glob("*.json")):
    obj = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(obj, dict):
        cols = obj.get("value", [])
    else:
        cols = obj
    data = [c for c in cols if c.get("name") not in SKIP and not c.get("hidden")]
    print()
    print("=" * 90)
    print(f"LISTE: {p.stem.upper()} ({len(data)} colonnes utiles non cachees)")
    print("=" * 90)
    hdr = f"{'name':<32} {'displayName':<28} {'columnType':<18} {'req':<5}"
    print(hdr + " details")
    print("-" * 90)
    for c in data:
        nm = c.get("name","")
        dn = (c.get("displayName","") or nm)[:28]
        ct = c.get("columnType","?")
        rq = "OUI" if c.get("required") else ""
        extra = ""
        if c.get("choice") and c["choice"].get("choices"):
            ch = c["choice"]["choices"]
            extra = "CHOIX: " + " | ".join(ch[:5])
            if len(ch) > 5: extra += " ..."
        if c.get("lookup"):
            l = c["lookup"]
            lid = str(l.get("listId","?"))[:14]
            extra = f"LOOKUP listId={lid} col={l.get('columnName','')}"
            if l.get("allowMultipleValues"): extra += " [MULTI]"
        if c.get("number"):
            n = c["number"]
            extra = "NUMBER dec=%s disp=%s" % (n.get("decimalPlaces","?"), n.get("displayAs",""))
        if c.get("text"):
            t = c["text"]
            multi = bool(t.get("allowMultipleLines"))
            extra = "TEXT max=%s multi=%s" % (t.get("maxLength","?"), multi)
        if c.get("dateTime"):
            dt = c["dateTime"]
            extra = "DATETIME disp=%s fmt=%s" % (dt.get("displayAs","?"), dt.get("format",""))
        if c.get("personOrGroup"):
            pg = c["personOrGroup"]
            extra = "PERSON disp=%s multi=%s" % (pg.get("displayAs","?"), bool(pg.get("allowMultipleSelection")))
        if c.get("boolean"):
            extra = "BOOLEAN"
        if c.get("hyperlinkOrPicture"):
            extra = "HYPERLINK"
        line = f"{nm:<32} {dn:<28} {ct:<18} {rq:<5} {extra}"
        print(line)
