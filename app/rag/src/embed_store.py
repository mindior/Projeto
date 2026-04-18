from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from .chunking import Chunk


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def get_embedder() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def build_and_save_index(
    chunks: List[Chunk],
    store_dir: Path,
) -> None:
    store_dir.mkdir(parents=True, exist_ok=True)

    embedder = get_embedder()
    texts = [c.text for c in chunks]
    embeddings = embedder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings.astype("float32"))

    faiss.write_index(index, str(store_dir / "index.faiss"))

    metadata = [
        {
            "chunk_id": c.chunk_id,
            "source": c.source,
            "page_number": c.page_number,
            "text": c.text,
        }
        for c in chunks
    ]
    (store_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_index(store_dir: Path) -> Tuple[faiss.Index, list[dict]]:
    index = faiss.read_index(str(store_dir / "index.faiss"))
    metadata = json.loads((store_dir / "metadata.json").read_text(encoding="utf-8"))
    return index, metadata
