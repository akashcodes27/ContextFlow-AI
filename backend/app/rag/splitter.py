from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        "",
    ],
)


def split_documents(documents: list[Document]) -> list[Document]:
    """
    Split documents into overlapping chunks.
    """

    return text_splitter.split_documents(documents)

# This recursive approach ensures chunks are as "natural" as possible while still respecting the size limit.
# Recursive character splitting is a proven baseline and is widely used in production.