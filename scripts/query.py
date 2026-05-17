"""GraphRAG query: semantic search + graph traversal for LLM context."""
import sys

from embedder import embed_text
from qdrant_manager import scroll_by_doc_ids, search_vectors


def graph_rag_retrieve(query, top_k=5, related_per_doc=3):
    """
    1. Semantic search for top_k chunks.
    2. Traverse linked/backlinked documents.
    3. Pull representative chunks from related docs.
    4. Deduplicate and format as rich context.
    """
    print(f"\nQuery: {query}")

    # Phase 1 — Semantic retrieval
    query_vector = embed_text(query, task_type="retrieval_query")
    initial = search_vectors(query_vector, limit=top_k)

    doc_ids_hit = {r.payload["doc_id"] for r in initial}
    print(f"Initial hits: {len(initial)} chunks from {len(doc_ids_hit)} docs")

    # Phase 2 — Graph traversal
    linked_doc_ids = set()
    for point in initial:
        linked_doc_ids.update(point.payload.get("linked_doc_ids", []))
        linked_doc_ids.update(point.payload.get("backlinked_doc_ids", []))

    # Exclude docs already in initial results to avoid duplication
    linked_doc_ids -= doc_ids_hit

    # Phase 3 — Fetch related chunks
    related = []
    if linked_doc_ids:
        limit = max(len(linked_doc_ids) * related_per_doc, 50)
        related = scroll_by_doc_ids(list(linked_doc_ids), limit=limit)
        print(f"Related docs: {len(linked_doc_ids)} docs, {len(related)} chunks fetched")

    # Phase 4 — Deduplicate
    seen = set()
    all_points = []
    for point in initial + related:
        if point.id not in seen:
            seen.add(point.id)
            all_points.append(point)

    # Phase 5 — Format
    return format_context(all_points)


def format_context(points):
    """Group chunks by document and render clean context blocks."""
    # Group by doc_id, preserving chunk order
    by_doc = {}
    for p in points:
        did = p.payload["doc_id"]
        by_doc.setdefault(did, []).append(p)

    for did in by_doc:
        by_doc[did].sort(key=lambda x: x.payload["chunk_index"])

    lines = []
    for doc_id, doc_points in by_doc.items():
        first = doc_points[0].payload
        lines.append("")
        lines.append("=" * 70)
        lines.append(f"DOCUMENT: {first['doc_path']}")
        lines.append(f"DOC_ID:   {doc_id}")
        lines.append(f"TAGS:     {', '.join(first.get('tags', []))}")
        lines.append("=" * 70)

        for p in doc_points:
            heading = p.payload.get("heading", "")
            if heading:
                lines.append(f"\n{heading}")
            lines.append(p.payload["content"])

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python query.py 'your question here'")
        sys.exit(1)

    query = sys.argv[1]
    context = graph_rag_retrieve(query)
    print("\n" + "=" * 70)
    print("RETRIEVED CONTEXT FOR LLM")
    print("=" * 70)
    print(context)
    print("\n" + "=" * 70)
    print(f"Total characters in context: {len(context)}")
