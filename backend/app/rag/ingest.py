import uuid

from langchain_core.documents import Document

from app.rag.loaders import load_document
from app.rag.splitter import split_documents
from app.rag.vectorstore import add_documents


def ingest_document(
    *,
    file_path: str,
    user_id: str,
    filename: str,
):
    """
    Complete ingestion pipeline.

    File
      ↓
    Loader
      ↓
    Splitter
      ↓
    Metadata
      ↓
    Vector Store
    """

    # Load document
    documents = load_document(file_path)

    # Split into chunks
    chunks = split_documents(documents)

    # One document id for all chunks
    document_id = str(uuid.uuid4())

    metadata = []

    for chunk in chunks:

        chunk_metadata = {
            "user_id": user_id,
            "document_id": document_id,
            "filename": filename,
        }

        # Preserve existing metadata from loader
        chunk_metadata.update(chunk.metadata)

        metadata.append(chunk_metadata)

    # vectorstore.py entrypoint 
    add_documents(
        docs=chunks,
        metadata=metadata,
    )

    return {
        "document_id": document_id,
        "filename": filename,
        "chunks": len(chunks),
    }