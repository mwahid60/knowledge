"""Qdrant collection manager and vector operations."""
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchAny,
    MatchValue,
    PointStruct,
    VectorParams,
)

from config import (
    QDRANT_API_KEY,
    QDRANT_COLLECTION,
    QDRANT_HOST,
    QDRANT_PORT,
    QDRANT_USE_HTTPS,
    QDRANT_VERIFY_SSL,
    VECTOR_SIZE,
)

client = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT,
    api_key=QDRANT_API_KEY,
    https=QDRANT_USE_HTTPS,
    verify=QDRANT_VERIFY_SSL,
)


def make_point_id(doc_id: str, chunk_index: int) -> str:
    """Generate a deterministic UUID for a chunk.

    Qdrant only accepts unsigned integers or UUIDs as point IDs.
    Using uuid5 ensures the same (doc_id, chunk_index) always yields
    the same UUID across re-syncs.
    """
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{doc_id}-{chunk_index}"))


def ensure_collection():
    """Create collection if it does not exist."""
    try:
        client.get_collection(QDRANT_COLLECTION)
    except Exception:
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
        print(f"Created Qdrant collection: {QDRANT_COLLECTION}")


def upsert_points(points):
    """Insert or update points."""
    if points:
        client.upsert(collection_name=QDRANT_COLLECTION, points=points)


def delete_by_doc_id(doc_id):
    """Remove all points belonging to a document."""
    client.delete(
        collection_name=QDRANT_COLLECTION,
        points_selector=Filter(
            must=[FieldCondition(key="doc_id", match=MatchValue(value=doc_id))]
        ),
    )


def set_payload_by_doc_id(doc_id, payload):
    """Update metadata payload for all points of a document (no re-embed)."""
    client.set_payload(
        collection_name=QDRANT_COLLECTION,
        payload=payload,
        points=Filter(
            must=[FieldCondition(key="doc_id", match=MatchValue(value=doc_id))]
        ),
    )


def search_vectors(vector, limit=5):
    """Semantic similarity search."""
    return client.search(
        collection_name=QDRANT_COLLECTION,
        vector=vector,
        limit=limit,
        with_payload=True,
    )


def scroll_by_doc_ids(doc_ids, limit=200):
    """Retrieve chunks from specific documents."""
    if not doc_ids:
        return []
    return client.scroll(
        collection_name=QDRANT_COLLECTION,
        scroll_filter=Filter(
            must=[FieldCondition(key="doc_id", match=MatchAny(any=list(doc_ids)))]
        ),
        limit=limit,
    )[0]
