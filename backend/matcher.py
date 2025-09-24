# backend/matcher.py
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load model once
MODEL_NAME = os.environ.get("SBERT_MODEL", "all-MiniLM-L6-v2")
print(f"[matcher] Loading SentenceTransformer model: {MODEL_NAME} ...")
model = SentenceTransformer(MODEL_NAME)
print("[matcher] Model loaded.")

def embed_texts(texts):
    """
    Returns embeddings for a list of texts using sentence-transformers.
    """
    if not isinstance(texts, list):
        texts = [texts]
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return embeddings

def get_similarity_score(text_a, text_b):
    """
    Compute cosine similarity (0-100) between two texts using SBERT embeddings.
    Returns float percentage with 2 decimals.
    """
    embs = embed_texts([text_a, text_b])
    a, b = embs[0].reshape(1, -1), embs[1].reshape(1, -1)
    sim = cosine_similarity(a, b)[0][0]
    return round(float(sim * 100), 2)
