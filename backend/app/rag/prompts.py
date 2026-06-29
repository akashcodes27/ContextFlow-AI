from langchain_core.prompts import ChatPromptTemplate


RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful AI assistant.

Answer ONLY using the supplied context.

If the answer is not present,
say you don't know.

Context:

{context}
"""
        ),

        (
            "human",
            "{question}"
        ),
    ]
)