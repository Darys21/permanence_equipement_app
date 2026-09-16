
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Extract text from both PDFs
permanence_text = extract_text_from_pdf(r"c:\Users\jyd.anguilet\Downloads\Joan - SETRAG\PERMANANCE EQUIPEMENT\Documentation\PERMANENCE EQUIPEMENT.pdf")
process_text = extract_text_from_pdf(r"c:\Users\jyd.anguilet\Downloads\Joan - SETRAG\PERMANANCE EQUIPEMENT\Documentation\process_developpement_app.pdf")

print("=== PERMANENCE EQUIPEMENT.PDF ===")
print(permanence_text)
print("\n=== PROCESS_DEVELOPPEMENT_APP.PDF ===")
print(process_text)
