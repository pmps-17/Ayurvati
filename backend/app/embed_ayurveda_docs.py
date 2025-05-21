import os
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract
from sentence_transformers import SentenceTransformer
import asyncio
from backend.app.models import AyurvedaDoc, SessionLocal

PDF_FOLDER = "assets"  # Folder containing your PDFs

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

async def process_pdf(pdf_path, session):
    # Try direct text extraction first
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        page_text = page.get_text()
        if page_text.strip():
            text += page_text + "\n"
    doc.close()
    # If no text extracted, use OCR on images
    if not text.strip():
        print(f"Using OCR for: {pdf_path}")
        images = convert_from_path(pdf_path)
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"
    # Only process if text found
    if text.strip():
        embedding = model.encode(text[:2048]).tolist()  # Truncate if very long
        title = os.path.basename(pdf_path)
        doc = AyurvedaDoc(
            title=title,
            content=text[:10000],   # Store only first 10k chars for demo; adjust as needed
            embedding=embedding
        )
        session.add(doc)
        print(f"Processed and embedded: {title}")
    else:
        print(f"No text found for: {pdf_path}")

async def main():
    async with SessionLocal() as session:
        for filename in os.listdir(PDF_FOLDER):
            if filename.lower().endswith('.pdf'):
                await process_pdf(os.path.join(PDF_FOLDER, filename), session)
        await session.commit()
    print("All PDFs processed!")

if __name__ == "__main__":
    asyncio.run(main())
