from pypdf import PdfReader

def extract_text(file):
    if not file: return ""
    if file.type == "application/pdf":
        return " ".join([p.extract_text() for p in PdfReader(file).pages])
    return str(file.read(), "utf-8")
