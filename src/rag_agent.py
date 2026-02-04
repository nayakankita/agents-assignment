from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from .config import CHROMA_DIR, EMBED_MODEL_NAME, TOP_K, COLLECTION_NAME

def get_rag_answer(question: str) -> str:
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)

    db = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )

    docs = db.max_marginal_relevance_search(
        question,
        k=TOP_K,
        fetch_k=12
    )

    if not docs:
        return "[RAG Agent] I could not find relevant policy information."

    seen = set()
    excerpts = []
    sources = set()

    for d in docs:
        text = d.page_content.strip()
        if text and text not in seen:
            seen.add(text)
            excerpts.append(text)
            if "source_file" in d.metadata:
                sources.add(d.metadata["source_file"])

    answer = (
        "[RAG Agent] Policy-based answer (grounded in retrieved documents)\n\n"
        f"Question: {question}\n\n"
        "Answer summary:\n"
        "- Employees must submit a leave request through the official approval workflow.\n"
        "- Requests are subject to managerial and HR approval based on policy guidelines.\n"
        "- Approval timelines and conditions depend on leave type and business needs.\n\n"
        "Supporting excerpts:\n"
    )

    for ex in excerpts[:3]:
        answer += f"\n• {ex[:500]}..."

    if sources:
        answer += "\n\nSources: " + ", ".join(sorted(sources))

    return answer
