from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore

from qdrant_client import QdrantClient
from qdrant_client.http import models

# from app.config import (
#     QDRANT_HOST,
#     QDRANT_PORT,
# )

from app.rag.embeddings import get_embeddings
from app.db.qdrant_client import qdrant_client as client


COLLECTION_NAME = "contextflow_docs"
# A collection in Qdrant is like a table in PostgreSQL — it holds related vectors that can be searched together.


# ---------------------------------------------------
# Qdrant Client
# ---------------------------------------------------

# client = QdrantClient(
#     host=QDRANT_HOST,
#     port=QDRANT_PORT,
# )


# ---------------------------------------------------
# Collection
# ---------------------------------------------------



# Purpose: Check if a collection exists in Qdrant, if not, create one. 
def ensure_collection():
    """
    Create the collection if it doesn't exist.
    """
    # A collection in Qdrant is like a table in PostgreSQL — it holds related vectors that can be searched together.
    collections = client.get_collections().collections

    collection_names = {
        collection.name
        for collection in collections
    }

    if COLLECTION_NAME not in collection_names:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=1024,
                distance=models.Distance.COSINE,
            ),
            # The distance metric is COSINE, which measures similarity based on the angle between vectors
            # size value depends on the embedding model used. 
        )


# ---------------------------------------------------
# Vector Store
# ---------------------------------------------------

def get_vector_store() -> QdrantVectorStore:

    ensure_collection()

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=get_embeddings(),
    )


# ---------------------------------------------------
# Add Documents
# ---------------------------------------------------

def add_documents(
    documents: list[Document],
    metadata: list[dict],
):
    """
    Store LangChain Documents.
    """

    vector_store = get_vector_store()

    vector_store.add_documents(documents)


# ---------------------------------------------------
# Delete Entire Collection
# ---------------------------------------------------

def delete_collection():

    collections = client.get_collections().collections

    names = {
        c.name
        for c in collections
    }

    if COLLECTION_NAME in names:

        client.delete_collection(
            collection_name=COLLECTION_NAME
        )


# ---------------------------------------------------
# Delete Points
# ---------------------------------------------------

def delete_documents(
    document_id: str,
):

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="document_id",
                        match=models.MatchValue(
                            value=document_id
                        ),
                    )
                ]
            )
        ),
    )