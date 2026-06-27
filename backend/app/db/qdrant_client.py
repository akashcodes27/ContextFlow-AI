from qdrant_client import QdrantClient
from app.config import QDRANT_HOST, QDRANT_PORT

qdrant_client = QdrantClient(
    host=QDRANT_HOST,
    port=int(QDRANT_PORT)
)