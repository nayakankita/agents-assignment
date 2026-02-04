from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from .config import (
    DATA_DIR,
    CHROMA_DIR,
    EMBED_MODEL_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    COLLECTION_NAME,
)

def load_all_pdfs(data_dir: Path):
    pdf_files = list(data_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {data_dir}")

    documents = []
    for pdf_path in pdf_files:
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        for page in pages:
            page.metadata["source_file"] = pdf_path.name
        documents.extend(pages)

    return documents


def main():
    print(f"📄 Loading PDFs from: {DATA_DIR}")
    docs = load_all_pdfs(DATA_DIR)
    print(f"✅ Loaded {len(docs)} pages")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(docs)
    print(f"🧩 Created {len(chunks)} chunks")

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)

    print(f"🧠 Creating Chroma DB at: {CHROMA_DIR}")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name=COLLECTION_NAME
    )

    vectorstore.persist()
    print("💾 Chroma DB persisted successfully!")


if __name__ == "__main__":
    main()
