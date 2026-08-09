import pymupdf

def extract_text(pdf_path: str):

    document = pymupdf.open(pdf_path)

    text = ""

    for page in document:

        text += page.get_text()

    document.close()

    return text