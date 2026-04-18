from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List
from pypdf import PdfReader


@dataclass
class RawPage:
    source: str
    page_number: int
    text: str


def extract_pages(pdf_paths: Iterable[Path]) -> List[RawPage]:
    pages: List[RawPage] = []
    for pdf_path in pdf_paths:
        reader = PdfReader(str(pdf_path))
        for idx, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if text:
                pages.append(
                    RawPage(
                        source=pdf_path.name,
                        page_number=idx,
                        text=text,
                    )
                )
    return pages
