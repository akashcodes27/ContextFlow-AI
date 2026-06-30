from langchain_openai import ChatOpenAI

from app.rag.retriever import retrieve_documents
from app.rag.prompts import RAG_PROMPT
from app.config import (
    DEEPSEEK_MODEL, DEEPSEEK_API_KEY)


# DeepSeek-V4-Flash via OpenAI-compatible API
llm = ChatOpenAI(
    model=DEEPSEEK_MODEL,
    openai_api_key=DEEPSEEK_API_KEY,
    openai_api_base="https://api.deepseek.com/v1",
    temperature=0.2,
    max_tokens=4096,
)


def generate_answer(query: str, user_id: str):

    # 1. Retrieve documents
    docs = retrieve_documents(
        query=query,
        user_id=user_id,
        k=5
    )

    # 2. Build context
    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # 3. Create prompt
    prompt = RAG_PROMPT.invoke({
        "question": query,
        "context": context
    })

    # 4. LLM call
    response = llm.invoke(prompt)

    return {
        "query": query,
        "response": response.content,
        "sources": [
            {
                "content": doc.page_content[:200],
                "metadata": doc.metadata
            }
            for doc in docs
        ]
    }