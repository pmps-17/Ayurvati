import os
import asyncio
from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.dialects.postgresql import INTEGER
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
from pgvector.sqlalchemy import Vector

# ─── 1) CONFIGURE DATABASE CONNECTION ─────────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL")
# Use your actual URL: e.g., postgresql+asyncpg://postgres:MyPass@127.0.0.1:5432/ayurvati

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# ─── 2) DEFINE THE ORM MODEL (matches your existing table) ──────────────────────
class AyurvedaDoc(Base):
    __tablename__ = "ayurveda_docs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    embedding = Column(Vector(768))  # 768 dims for “all-MiniLM-L6-v2”

# ─── 3) SET UP YOUR EMBEDDING MODEL ─────────────────────────────────────────────
# We’ll use “all-MiniLM-L6-v2” but you can choose any 768-dim SBERT model.
sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

# ─── 4) FUNCTION TO EXTRACT RAW TEXT FROM A PDF ─────────────────────────────────
def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Returns all the extracted text from the given PDF file as one long string.
    """
    reader = PdfReader(pdf_path)
    text_chunks = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_chunks.append(text)
    return "\n".join(text_chunks)


# ─── 5) (OPTIONAL) SIMPLE CHUNKER ────────────────────────────────────────────────
def chunk_text(text: str, max_chars: int = 2000) -> list[str]:
    """
    Naïve chunking: split on paragraphs until each chunk is ≤ max_chars.
    Adjust as needed (e.g. sentence-based chunking, sliding window, etc.).
    """
    paragraphs = text.split("\n\n")
    chunks = []
    current = []
    curr_len = 0

    for para in paragraphs:
        if curr_len + len(para) + 2 <= max_chars:
            current.append(para)
            curr_len += len(para) + 2
        else:
            if current:
                chunks.append("\n\n".join(current))
            current = [para]
            curr_len = len(para) + 2

    if current:
        chunks.append("\n\n".join(current))

    return chunks


# ─── 6) MAIN “LOADER” COROUTINE ───────────────────────────────────────────────────
async def load_pdfs_into_pgvector(pdf_folder: str):
    """
    For every PDF in `pdf_folder/`, extract text, chunk it, embed each chunk,
    and insert into the ayurveda_docs table.
    """
    async with AsyncSessionLocal() as session:
        # Ensure the table exists. If not, create it (you can comment this out if already done):
        await session.run_sync(Base.metadata.create_all)

        # Iterate over all .pdf files in that folder
        for filename in os.listdir(pdf_folder):
            if not filename.lower().endswith(".pdf"):
                continue

            pdf_path = os.path.join(pdf_folder, filename)
            print(f"\nProcessing {pdf_path}...")

            # 1) Extract full text
            raw_text = extract_text_from_pdf(pdf_path)
            if not raw_text.strip():
                print("  → Warning: No text found in PDF, skipping.")
                continue

            # 2) Chunk the text (so each chunk is reasonably sized)
            chunks = chunk_text(raw_text, max_chars=1800)
            print(f"  → Extracted {len(chunks)} chunk(s).")

            # For each chunk, compute an embedding & insert into the DB
            for idx, chunk in enumerate(chunks, start=1):
                # Compute the 768-dim vector
                embedding = sbert_model.encode(chunk).tolist()

                # Use “filename_chunkN” as a simple title (or adjust as you wish)
                title = f"{filename} (chunk {idx})"

                # Create the ORM object
                doc = AyurvedaDoc(
                    title=title,
                    content=chunk,
                    embedding=embedding  # SQLAlchemy’s Vector() will handle it
                )

                session.add(doc)

                # Optional: commit every N inserts to avoid one huge transaction
                if idx % 10 == 0:
                    try:
                        await session.commit()
                        print(f"  → Committed up to chunk {idx}.")
                    except IntegrityError as e:
                        await session.rollback()
                        print("  → IntegrityError:", e)
                        # maybe skip duplicates or handle as you see fit

            # Commit any remaining chunks for this PDF
            try:
                await session.commit()
                print(f"  → Finished inserting all chunks of {filename}.")
            except IntegrityError as e:
                await session.rollback()
                print("  → IntegrityError on final commit:", e)

    print("\nAll done! PDF loading complete.")


# ─── 7) ENTRY POINT ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python load_pdfs_to_pgvector.py /path/to/your/pdf_folder")
        sys.exit(1)

    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(f"ERROR: {folder} is not a valid directory.")
        sys.exit(1)

    asyncio.run(load_pdfs_into_pgvector(folder))
