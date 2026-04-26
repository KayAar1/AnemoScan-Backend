"""
RAG Engine for AnemiaCare Chatbot
----------------------------------
Builds a FAISS vector index from the knowledge base at startup,
then retrieves the top-k most relevant chunks for each user query.
Uses sentence-transformers (all-MiniLM-L6-v2 — ~90 MB, CPU-friendly).
"""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from knowledge_base import ANEMIA_CHUNKS

# ── Model & Index (loaded once at startup) ──────────────────
_model: SentenceTransformer = None
_index: faiss.IndexFlatIP = None
_chunks: list[str] = []


def _build_index():
    global _model, _index, _chunks

    print("[RAG] Loading embedding model...")
    _model = SentenceTransformer("all-MiniLM-L6-v2")

    print(f"[RAG] Embedding {len(ANEMIA_CHUNKS)} knowledge chunks...")
    _chunks = ANEMIA_CHUNKS
    embeddings = _model.encode(_chunks, convert_to_numpy=True, show_progress_bar=True)

    # Normalize for cosine similarity via inner product
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norms

    dim = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dim)
    _index.add(embeddings.astype("float32"))
    print(f"[RAG] Index ready — {_index.ntotal} vectors, dim={dim}")


def initialize():
    """Call once at app startup."""
    _build_index()


def retrieve(query: str, top_k: int = 4) -> list[str]:
    """
    Returns the top_k most relevant knowledge chunks for the given query.
    """
    if _index is None:
        raise RuntimeError("RAG engine not initialized. Call initialize() first.")

    q_emb = _model.encode([query], convert_to_numpy=True)
    q_emb = q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True)

    scores, indices = _index.search(q_emb.astype("float32"), top_k)

    results = []
    for idx, score in zip(indices[0], scores[0]):
        if idx >= 0 and score > 0.2:   # minimum relevance threshold
            results.append(_chunks[idx])

    return results
