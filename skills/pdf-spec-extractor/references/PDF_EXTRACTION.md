# REFERENCES - Extraction PDF + Generation PDF

## PyPDF2 / pypdf (lecture texte)

- `PdfReader(str_path)` ouvre PDF.
- `.pages` iterable de PageObject.
- `.extract_text()` renvoie str. Pages vides souvent = PDF image sans couche texte.

## reportlab (génération PDF process)

Pages A4, SimpleDocTemplate, styles paragraphe. Template minimal:
```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("out.pdf", pagesize=A4)
styles = getSampleStyleSheet()
story = [Paragraph("Titre Niv1", styles['Title']), Spacer(1, 12)]
story.append(Paragraph("Texte normal.", styles['BodyText']))
doc.build(story)
```

## Pipeline extraction spec PERMANENCE EQUIPEMENT

Schéma extraction:
1. Ouvrir PDF PERMANENCE EQUIPEMENT.pdf
2. Page 1: User Stories 1/2/3/4
3. Page 2: Colonnes par liste (6 tables)
4. Page 3: Annexes / process

## Fichiers texte générés
- `.txt` UTF-8 (non print cp1252) pour éviter encode erreur
- Fichiers JSON pour colonnes parsées (si besoin)
- Fichiers diff texte pour rapports

## Nommage colonnes standard
Depuis PDF, les colonnes mentionnées comme:
- Tx_Travaux: Title, Date_travaux, CantonID, Regime_travaux, ActeurID, Heure_demande, Heure_Fin_Prevue, Heures_Autorisee, Heure_engagement, Heures_Degagement, Heures_Voie_Retablie, Motif_Engagement, Motifs_Engagement_Tardif, Motif_Degagement_Tardif, Poste, AgentSaisie, DateSaisie, PK_Debut, PK_Fin
- Ref_Cantons: Title, Division, PK_Debut, PK_Fin
- Tx_Feedbacks: TravailID, HeureContact, MoyenCom, StatutContact, Commentaire

IMPORTANT: Les noms internes SharePoint exposés à Power Apps PEUVENT différer (casse, accent, pluriel Heure vs Heures). Utiliser `sharepoint-graph-schema` pour valeur finale.
