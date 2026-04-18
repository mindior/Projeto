from __future__ import annotations

from pathlib import Path
from typing import List, Dict

import numpy as np

from .embed_store import get_embedder, load_index


# 🔥 limiar mínimo de qualidade
MIN_SCORE = 0.25


def search(
    query: str,
    store_dir: Path,
    top_k: int = 4,
) -> List[Dict]:

    embedder = get_embedder()
    index, metadata = load_index(store_dir)

    # 🔹 gerar embedding da query
    query_embedding = embedder.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    # 🔹 busca vetorial
    scores, indices = index.search(query_embedding, top_k)

    results: List[Dict] = []

    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        item = metadata[idx].copy()
        item["score"] = float(score)

        results.append(item)

    # 🔥 FILTRO DE QUALIDADE
    filtered_results = [r for r in results if r["score"] >= MIN_SCORE]

    # 🔥 ordenação por score (segurança extra)
    filtered_results.sort(key=lambda x: x["score"], reverse=True)

    return filtered_results