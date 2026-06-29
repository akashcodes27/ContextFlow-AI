from langchain_openai import ChatOpenAI

from app.rag.retriever import retrieve_documents
from app.rag.prompts import RAG_PROMPT


# TEMP LLM (we will swap to DeepSeek later)
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
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