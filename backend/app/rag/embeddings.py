from langchain_huggingface import HuggingFaceEmbeddings


_embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5",
    model_kwargs={
        "device": "cpu",
    },
    encode_kwargs={
        "normalize_embeddings": True,
    },
)


def get_embeddings():
    """
    Return the singleton embedding model.
    """

    return _embeddings