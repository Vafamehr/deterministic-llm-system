import requests
import numpy as np
import faiss

OLLAMA = "http://localhost:11434"

def embed(text: str) -> np.ndarray:
    # print(f"{OLLAMA}/api/embeddings")
    r = requests.post(
        f"{OLLAMA}/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text},
        timeout=60,
    )
    r.raise_for_status()
    return np.array(r.json()["embedding"], dtype=np.float32)

def ask_llm(prompt: str) -> str:
    r = requests.post(
        f"{OLLAMA}/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["response"].strip()


if __name__ == "__main__":

    DOCS = [
        "Stockouts usually reduce demand because customers switch to competitors.",
        "Promotions often create temporary demand spikes followed by drops.",
        "Long supplier lead times increase inventory risk.",
        "Poor forecast accuracy leads to excess inventory.",
        "Seasonality strongly affects retail demand patterns.",
    ]

    print("Embedding documents...")
    doc_vecs = [embed(d) for d in DOCS]
    X = np.vstack(doc_vecs).astype(np.float32)  # shape: (n_docs, dim)

    dim = X.shape[1]
    print("Dim:", dim)

    # Use cosine similarity via inner product on normalized vectors
    faiss.normalize_L2(X)

    index = faiss.IndexFlatIP(dim)   # IP = inner product
    index.add(X)

    query = "Why can demand drop when inventory is unavailable?"
    q = embed(query).reshape(1, -1).astype(np.float32)
    faiss.normalize_L2(q)

    k = 2
    scores, ids = index.search(q, k)

    print("\nQuery:", query)
    print("Top hits:")
    for rank, (i, s) in enumerate(zip(ids[0], scores[0]), start=1):
        print(f"{rank}. score={s:.4f} | {DOCS[i]}")

    context = "\n".join([DOCS[i] for i in ids[0]])

    prompt = f"""Use the context to answer the question.

    Context:
    {context}

    Question:
    {query}

    Answer in 3-5 sentences:
    """

    answer = ask_llm(prompt)
    print("\n--- RAG Answer ---")
    print(answer)
    
