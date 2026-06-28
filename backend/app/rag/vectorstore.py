from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from app.config import QDRANT_HOST, QDRANT_PORT
from app.rag.embeddings import get_embeddings


COLLECTION_NAME = "contextflow_docs"


# -----------------------------
# Qdrant client singleton
# -----------------------------
client = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT
)


# -----------------------------
# Ensure collection exists
# -----------------------------
def ensure_collection():
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=qmodels.VectorParams(
                size=1024,  # bge-large-en-v1.5 = 1024 dims
                distance=qmodels.Distance.COSINE,
            ),
        )


# -----------------------------
# Get LangChain Vector Store
# -----------------------------
def get_vector_store():
    ensure_collection()

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=get_embeddings(),
    )


# -----------------------------
# Add documents (chunks)
# -----------------------------
def add_documents(docs: list, metadata: list[dict]):
    """
    docs: list of LangChain Document chunks
    metadata: list of metadata dicts aligned with docs
    """

    vector_store = get_vector_store()

    # attach metadata to each document
    for doc, meta in zip(docs, metadata):
        doc.metadata.update(meta)

    vector_store.add_documents(docs)


# -----------------------------
# Similarity search (with user filter)
# -----------------------------
def similarity_search(query: str, user_id: str, k: int = 5):
    vector_store = get_vector_store()

    results = vector_store.similarity_search(
        query=query,
        k=k,
        filter={
            "must": [
                {
                    "key": "user_id",
                    "match": {"value": user_id},
                }
            ]
        },
    )

    return results