from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .load_pdfs import RawPage


@dataclass
class Chunk:
    chunk_id: str
    source: str
    page_number: int
    text: str


def _normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def chunk_pages(
    pages: Iterable[RawPage],
    chunk_size: int = 900,
    overlap: int = 150,
) -> List[Chunk]:
    chunks: List[Chunk] = []
    for page_idx, page in enumerate(pages):
        clean = _normalize_whitespace(page.text)
        start = 0
        local_idx = 0
        while start < len(clean):
            end = min(len(clean), start + chunk_size)
            piece = clean[start:end].strip()
            if piece:
                chunks.append(
                    Chunk(
                        chunk_id=f"{page.source}-p{page.page_number}-c{local_idx}",
                        source=page.source,
                        page_number=page.page_number,
                        text=piece,
                    )
                )
            if end == len(clean):
                break
            start = max(0, end - overlap)
            local_idx += 1
    return chunks
