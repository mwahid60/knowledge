"""Main orchestrator: detect changes, chunk, embed, sync, and update relationships."""
import glob
import os
from datetime import datetime

from qdrant_client.models import PointStruct

from chunker import chunk_markdown
from config import EXCLUDED_FILES, SCAN_PATTERNS, SAFE_CHUNK_LIMIT, VAULT_PATH
from embedder import embed_text
from markdown_parser import (
    extract_links,
    parse_markdown,
    path_to_doc_id,
    resolve_link_path,
)
from qdrant_manager import (
    delete_by_doc_id,
    ensure_collection,
    make_point_id,
    set_payload_by_doc_id,
    upsert_points,
)
from state_manager import compute_file_hash, load_state, save_state


def get_all_markdown_files():
    """Discover all eligible markdown files in the vault."""
    files = []
    for pattern in SCAN_PATTERNS:
        full_pattern = os.path.join(VAULT_PATH, pattern)
        for filepath in glob.glob(full_pattern, recursive=True):
            rel = os.path.relpath(filepath, VAULT_PATH).replace(os.sep, "/")
            if rel in EXCLUDED_FILES:
                continue
            files.append(rel)
    return sorted(files)


def sync_file(rel_path, state):
    """Sync a single file into Qdrant. Returns (changed:bool, doc_id:str)."""
    filepath = os.path.join(VAULT_PATH, rel_path)
    doc_id = path_to_doc_id(rel_path)
    current_hash = compute_file_hash(filepath)

    if doc_id in state and state[doc_id].get("last_hash") == current_hash:
        print(f"  [SKIP] {rel_path}")
        return False, doc_id

    print(f"  [SYNC] {rel_path}")

    # Parse markdown
    frontmatter, body = parse_markdown(filepath)
    raw_links = extract_links(body, rel_path)
    resolved = [resolve_link_path(l, rel_path) for l in raw_links]
    linked_doc_ids = [path_to_doc_id(r) for r in resolved if r]

    # Chunk content
    chunks = chunk_markdown(body, max_chars=SAFE_CHUNK_LIMIT)

    # Remove old points for this document
    delete_by_doc_id(doc_id)

    # Embed and insert
    points = []
    for i, chunk in enumerate(chunks):
        point_id = make_point_id(doc_id, i)
        vector = embed_text(chunk["content"])
        payload = {
            "doc_id": doc_id,
            "doc_path": rel_path,
            "chunk_index": i,
            "total_chunks": len(chunks),
            "heading": chunk["heading"],
            "heading_level": chunk["heading_level"],
            "content": chunk["content"],
            "chunk_type": chunk["type"],
            "part": chunk["part"],
            "tags": frontmatter.get("tags", []) if frontmatter else [],
            "linked_doc_ids": linked_doc_ids,
            "backlinked_doc_ids": [],
            "char_count": len(chunk["content"]),
        }
        points.append(PointStruct(id=point_id, vector=vector, payload=payload))

    if points:
        upsert_points(points)

    # Update local state
    state[doc_id] = {
        "relative_path": rel_path,
        "last_hash": current_hash,
        "last_chunk_count": len(chunks),
        "last_modified": datetime.now().isoformat(),
    }

    return True, doc_id


def build_link_graph(all_files):
    """Build complete outgoing-link graph from all files."""
    graph = {}  # doc_id -> [target_doc_id, ...]

    for rel_path in all_files:
        doc_id = path_to_doc_id(rel_path)
        _, body = parse_markdown(os.path.join(VAULT_PATH, rel_path))
        raw_links = extract_links(body, rel_path)
        resolved = [resolve_link_path(l, rel_path) for l in raw_links]
        targets = [path_to_doc_id(r) for r in resolved if r]
        graph[doc_id] = targets

    return graph


def sync_relationships(all_files, changed_doc_ids):
    """Update linked_doc_ids / backlinked_doc_ids payloads without re-embedding."""
    graph = build_link_graph(all_files)

    # Determine affected documents
    affected = set(changed_doc_ids)
    for cid in changed_doc_ids:
        for tid in graph.get(cid, []):
            affected.add(tid)
        for sid, targets in graph.items():
            if cid in targets:
                affected.add(sid)

    print(f"  [REL] Updating {len(affected)} affected documents...")

    for doc_id in affected:
        outgoing = graph.get(doc_id, [])
        incoming = [sid for sid, targets in graph.items() if doc_id in targets]
        set_payload_by_doc_id(
            doc_id,
            {
                "linked_doc_ids": outgoing,
                "backlinked_doc_ids": incoming,
            },
        )
        print(f"    {doc_id}: {len(outgoing)} out, {len(incoming)} in")


def sync_all():
    """Run full sync pipeline."""
    ensure_collection()
    state = load_state()
    files = get_all_markdown_files()

    print(f"Scanning {len(files)} markdown files...\n")

    changed_doc_ids = []
    for rel_path in files:
        changed, doc_id = sync_file(rel_path, state)
        if changed:
            changed_doc_ids.append(doc_id)

    # Persist state immediately after inserts
    save_state(state)

    if changed_doc_ids:
        print(f"\n{len(changed_doc_ids)} documents changed. Updating graph relationships...")
        sync_relationships(files, changed_doc_ids)
    else:
        print("\nNo changes detected. Relationships are up-to-date.")

    print("\nDone.")


if __name__ == "__main__":
    sync_all()
