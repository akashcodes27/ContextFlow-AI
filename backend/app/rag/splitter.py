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



"""
Input Shape:
documents : list[Document]
[
  Document(page_content="<page 1 text, maybe 2500 chars>", metadata={"source": "report.pdf", "page": 0}),
  Document(page_content="<page 2 text, maybe 1800 chars>", metadata={"source": "report.pdf", "page": 1}),
  ...
]




Output Shape:
list[Document]
[
  Document(
    page_content="<chunk 1, ≤1000 chars>",
    metadata={"source": "report.pdf", "page": 0}   # inherited from parent Document
  ),
  Document(
    page_content="<chunk 2, ≤1000 chars, overlaps ~200 chars with chunk 1>",
    metadata={"source": "report.pdf", "page": 0}    # same metadata — split from same parent
  ),
  Document(
    page_content="<chunk 3 ...>",
    metadata={"source": "report.pdf", "page": 1}    # now from the second input Document
  ),
  ...
]


"""