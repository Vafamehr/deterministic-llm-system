# This makes RAG a tool-shaped deterministic capability
from __future__ import annotations

from dataclasses import dataclass,field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class RetrievalQuery:
    query: str
    top_k: int = 5
    namespace: Optional[str] = None  # e.g., "policies", "projects", "docs"


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: str
    text: str
    source: str  # filename/url/id
    score: float
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RetrievalResult:
    chunks: List[RetrievedChunk] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)



def retrieval_tool_input(payload: Dict[str, Any]) -> RetrievalQuery:
    """
    Convert ToolRequest.payload -> RetrievalQuery (strict + deterministic).
    """
    query = payload.get("query")
    if not isinstance(query, str) or not query.strip():
        raise ValueError("retrieval payload requires non-empty string field 'query'")

    top_k = payload.get("top_k", 5)
    if not isinstance(top_k, int) or top_k <= 0 or top_k > 50:
        raise ValueError("retrieval payload field 'top_k' must be int in [1, 50]")

    namespace = payload.get("namespace")
    if namespace is not None and (not isinstance(namespace, str) or not namespace.strip()):
        raise ValueError("retrieval payload field 'namespace' must be a non-empty string when provided")

    return RetrievalQuery(query=query.strip(), top_k=top_k, namespace=(namespace.strip() if isinstance(namespace, str) else None))


def retrieval_tool_output(result: RetrievalResult) -> Dict[str, Any]:
    """
    Convert RetrievalResult -> ToolResult.data (plain JSON-serializable dict).
    """
    return {
        "chunks": [
            {
                "chunk_id": c.chunk_id,
                "text": c.text,
                "source": c.source,
                "score": c.score,
                "meta": dict(c.meta),
            }
            for c in result.chunks
        ],
        "sources": list(result.sources),
        "meta": dict(result.meta),
    }   

###################################################

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(s: str) -> List[str]:
    return _TOKEN_RE.findall(s.lower())


def _load_corpus(namespace: Optional[str]) -> List[Dict[str, Any]]:
    base = Path("data") / "rag"
    folder = base / (namespace or "default")
    if not folder.exists() or not folder.is_dir():
        return []

    docs: List[Dict[str, Any]] = []
    for p in sorted(folder.glob("*.txt")):
        text = p.read_text(encoding="utf-8", errors="replace")
        docs.append(
            {
                "id": p.stem,
                "text": text,
                "source": str(p),
                "meta": {"filename": p.name, "namespace": namespace or "default"},
            }
        )
    return docs


def _score_overlap(query_tokens: List[str], doc_tokens: List[str]) -> float:
    return float(len(set(query_tokens).intersection(set(doc_tokens))))


def _retrieve_from_index(query: str, top_k: int, namespace: Optional[str]) -> List[Dict[str, Any]]:
    """
    Deterministic baseline "index":
    - Loads txt files from data/rag/<namespace>/
    - Scores by keyword overlap
    - Returns top_k hits
    """
    corpus = _load_corpus(namespace)
    if not corpus:
        return []

    q_tokens = _tokenize(query)
    scored: List[Tuple[float, Dict[str, Any]]] = []

    for doc in corpus:
        d_tokens = _tokenize(doc["text"])
        score = _score_overlap(q_tokens, d_tokens)
        if score > 0:
            scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)

    hits: List[Dict[str, Any]] = []
    for score, doc in scored[:top_k]:
        hits.append(
            {
                "id": doc["id"],
                "text": doc["text"],
                "source": doc["source"],
                "score": score,
                "meta": doc.get("meta", {}),
            }
        )
    return hits



#####################################################

# NOTE:
# This assumes you already have some in-memory index or simple retriever.
# Replace `_retrieve_from_index` with your existing retrieval logic.

def execute_retrieval(query: RetrievalQuery) -> RetrievalResult:
    """
    Deterministic retrieval execution.
    No LLM calls.
    No agent decisions.
    Pure data lookup.
    """

    raw_hits = _retrieve_from_index(
        query=query.query,
        top_k=query.top_k,
        namespace=query.namespace,
    )

    chunks = []
    sources = set()

    for hit in raw_hits:
        chunk = RetrievedChunk(
            chunk_id=str(hit["id"]),
            text=hit["text"],
            source=hit["source"],
            score=float(hit.get("score", 0.0)),
            meta=hit.get("meta", {}),
        )
        chunks.append(chunk)
        sources.add(chunk.source)

    return RetrievalResult(
        chunks=chunks,
        sources=sorted(list(sources)),
        meta={
            "top_k": query.top_k,
            "namespace": query.namespace,
            "num_returned": len(chunks),
        },
    )     


# =========================
# Tool wrapper (Chunk 4)
# =========================

from contracts import ToolSpec, ToolRequest, ToolResult

TOOL_NAME = "rag.retrieve"


def _run_retrieval_tool(request: ToolRequest) -> ToolResult:
    try:
        rq = retrieval_tool_input(request.payload)
        rr = execute_retrieval(rq)
        return ToolResult(
            tool_name=TOOL_NAME,
            status="SUCCESS",
            data=retrieval_tool_output(rr),
            error=None,
            meta={"top_k": rq.top_k, "namespace": rq.namespace},
        )
    except Exception as e:
        return ToolResult(
            tool_name=TOOL_NAME,
            status="ERROR",
            data={},
            error=str(e),
            meta={},
        )


RETRIEVAL_TOOL = ToolSpec(
    name=TOOL_NAME,
    description="Deterministic retrieval over data/rag/<namespace>/*.txt (orchestrator-owned).",
    runner=_run_retrieval_tool,
)