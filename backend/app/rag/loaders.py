from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
)


class DocumentLoader:

    @staticmethod
    def load(file_path: str):
        path = Path(file_path)

        extension = path.suffix.lower()

        if extension == ".pdf":
            loader = PyPDFLoader(file_path)

        elif extension == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")

        elif extension == ".docx":
            loader = Docx2txtLoader(file_path)

        elif extension in [".md", ".markdown"]:
            loader = UnstructuredMarkdownLoader(file_path)

        else:
            raise ValueError(f"Unsupported file type: {extension}")

        return loader.load()