from app.rag.vectorstore import get_vector_store


def retrieve_documents(
    query: str,
    user_id: str,
    k: int = 5,
):
    vector_store = get_vector_store()

    return vector_store.similarity_search(
        query=query,
        k=k,
        filter={
            "must": [
                {
                    "key": "user_id",
                    "match": {
                        "value": user_id
                    }
                }
            ]
        }
    )