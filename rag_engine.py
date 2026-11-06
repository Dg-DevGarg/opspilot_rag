import os
import glob
import chromadb
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq Client and Local Vector DB
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="opspilot_docs")


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150):
    """Splits text into overlapping character chunks so context isn't cut off."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def index_documents(force_reindex: bool = False):
    """Reads all .md files from data/, chunks them, and stores embeddings in ChromaDB."""
    global collection

    if collection.count() > 0 and not force_reindex:
        return

    if force_reindex and collection.count() > 0:
        chroma_client.delete_collection("opspilot_docs")
        collection = chroma_client.get_or_create_collection(name="opspilot_docs")

    md_files = glob.glob("data/*.md")
    documents, ids, metadatas = [], [], []

    chunk_counter = 0
    for filepath in md_files:
        filename = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        file_chunks = chunk_text(content)
        for i, chunk in enumerate(file_chunks):
            documents.append(chunk)
            ids.append(f"chunk_{chunk_counter}")
            metadatas.append({"source": filename, "chunk_index": i})
            chunk_counter += 1

    collection.add(documents=documents, ids=ids, metadatas=metadatas)
    print(f"Indexed {len(md_files)} files ({len(documents)} total chunks) into ChromaDB.")


def investigate_incident(query: str, top_k: int = 4):
    """Retrieves top-k relevant chunks and generates an incident report via gpt-oss-120b."""
    index_documents()

    results = collection.query(query_texts=[query], n_results=top_k)
    retrieved_chunks = results["documents"][0]
    retrieved_meta = results["metadatas"][0]
    distances = results["distances"][0]

    # Build context string with clear source filenames
    context_blocks = []
    unique_sources = []
    for chunk, meta, dist in zip(retrieved_chunks, retrieved_meta, distances):
        src = meta["source"]
        if src not in unique_sources:
            unique_sources.append(src)
        context_blocks.append(f"[Source File: {src} | Distance: {dist:.3f}]\n{chunk}")

    context_text = "\n\n---\n\n".join(context_blocks)

    system_prompt = (
        "You are OpsPilot, an AI Production Incident Investigation Assistant.\n"
        "Analyze the incoming incident alert using ONLY the provided internal documentation.\n\n"
        "Structure your response with these exact sections:\n"
        "1. **Potential Root Cause**: Explain what is failing and why.\n"
        "2. **Matching Historical Incidents / Runbooks**: Reference matching IDs (e.g., INC-101) or runbooks.\n"
        "3. **Step-by-Step Remediation Plan**: Concrete commands and actions to fix the issue.\n"
        "4. **Source Citations**: List the exact filenames used.\n\n"
        "STRICT GUARDRAIL: If the provided context does not contain relevant information to diagnose "
        "the query, do not guess or make up steps. State: "
        "'I couldn't find sufficient information in the available documentation to diagnose this incident.'"
    )

    user_prompt = f"### Retrieved Documentation:\n{context_text}\n\n### Incoming Incident Alert:\n{query}"

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1
    )

    return {
        "report": response.choices[0].message.content,
        "sources": unique_sources,
        "chunks": retrieved_chunks,
        "distances": distances
    }


if __name__ == "__main__":
    sample_alert = (
        "Payment API is returning HTTP 503 errors. Database connections are timing out "
        "after deployment."
    )
    print(f"Testing Incident Alert:\n'{sample_alert}'\n")
    output = investigate_incident(sample_alert)
    print("=== OPSPILOT INVESTIGATION REPORT ===\n")
    print(output["report"])
    print("\n=== RETRIEVED SOURCES ===")
    print(", ".join(output["sources"]))