from app.services.pdf_service import extract_text

text = extract_text("uploads/Experiment no 2.pdf")

print(text)