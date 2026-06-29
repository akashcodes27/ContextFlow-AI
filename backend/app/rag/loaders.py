from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
)


def load_document(file_path: str) -> list[Document]:
    """
    Load a supported document using the appropriate LangChain loader.
    """

    extension = Path(file_path).suffix.lower()

    loaders = {
        ".pdf": PyPDFLoader,
        ".txt": TextLoader,
        ".docx": Docx2txtLoader,
        ".md": UnstructuredMarkdownLoader,
        ".markdown": UnstructuredMarkdownLoader,
    }

    if extension not in loaders:
        raise ValueError(f"Unsupported file type: {extension}")

    loader_class = loaders[extension]

    if extension == ".txt":
        loader = loader_class(file_path, encoding="utf-8")
    else:
        loader = loader_class(file_path)

    return loader.load()




"""
load_document function takes a file path as input, Path object is used to extract the file extension using suffix attribute. It then checks if the extension is in the loaders dictionary, which maps file extensions to their corresponding LangChain loader classes. If the extension is supported, it initializes the appropriate loader class and loads the document, returning a list of Document objects.
"""