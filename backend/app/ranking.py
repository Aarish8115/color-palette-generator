import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


def load_ranking_resources(embeddings_path: str, model_name: str = "models/embedding"):
    model = SentenceTransformer(model_name)
    embeddings = np.load(embeddings_path)
    return model, embeddings


def embed_prompt(prompt_text: str, model: SentenceTransformer) -> np.ndarray:
    return model.encode([prompt_text], convert_to_numpy=True)[0]


def cosine_similarity_batch(query_vector: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    query_norm = query_vector / np.linalg.norm(query_vector)
    matrix_norms = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix_norms @ query_norm


def rank_candidates(
    filtered_df: pd.DataFrame,
    prompt_text: str,
    full_embeddings: np.ndarray,
    model: SentenceTransformer
) -> pd.DataFrame:
    if filtered_df.empty:
        return filtered_df

    # use color_id (== original row position) to index into full_embeddings
    candidate_indices = filtered_df["color_id"].to_numpy()
    candidate_embeddings = full_embeddings[candidate_indices]

    query_vector = embed_prompt(prompt_text, model)
    similarities = cosine_similarity_batch(query_vector, candidate_embeddings)

    ranked_df = filtered_df.copy()
    ranked_df["similarity_score"] = similarities
    ranked_df = ranked_df.sort_values("similarity_score", ascending=False)

    return ranked_df