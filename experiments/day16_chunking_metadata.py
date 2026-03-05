from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


REQUIRED_META_KEYS = {"document_id", "section", "source", "year", "chunk_id"}


@dataclass
class Chunk:
    text: str
    meta: Dict[str, object]


def simple_section_chunker(raw_text: str, *, document_id: str, source: str, year: int) -> List[Chunk]:
    """
    Toy chunker: splits on lines that look like headings (start with '## ').
    Each section becomes one chunk preserving meaning.
    """
    lines = [ln.rstrip() for ln in raw_text.splitlines()]
    chunks: List[Chunk] = []

    current_section = "unknown"
    buffer: List[str] = []
    chunk_idx = 0

    def flush():
        nonlocal chunk_idx, buffer
        text = "\n".join([x for x in buffer if x.strip()]).strip()
        if not text:
            return
        chunk_idx += 1
        chunks.append(
            Chunk(
                text=text,
                meta={
                    "document_id": document_id,
                    "section": current_section,
                    "source": source,
                    "year": year,
                    "chunk_id": f"{document_id}::c{chunk_idx:03d}",
                },
            )
        )
        buffer = []

    for ln in lines:
        if ln.startswith("## "):  # heading boundary
            flush()
            current_section = ln.replace("## ", "").strip().lower()
        else:
            buffer.append(ln)

    flush()
    return chunks


def validate_chunks(chunks: List[Chunk]) -> None:
    for c in chunks:
        missing = REQUIRED_META_KEYS - set(c.meta.keys())
        if missing:
            raise ValueError(f"Chunk {c.meta.get('chunk_id')} missing metadata keys: {sorted(missing)}")
        if not c.text or len(c.text) < 20:
            raise ValueError(f"Chunk {c.meta.get('chunk_id')} text too short (likely bad chunking).")


if __name__ == "__main__":
    sample_doc = """
## Termination
Either party may terminate this agreement by providing written notice thirty (30) days prior to termination.

## Payment
The buyer is responsible for payment within fifteen (15) days of invoice receipt.
""".strip()

    chunks = simple_section_chunker(sample_doc, document_id="contract_a", source="local_test", year=2022)
    validate_chunks(chunks)

    for c in chunks:
        print("\n--- CHUNK ---")
        print("chunk_id:", c.meta["chunk_id"])
        print("section :", c.meta["section"])
        print("text    :", c.text)
