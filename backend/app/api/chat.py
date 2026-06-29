from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.chat_service import generate_answer


router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    user_id: str


@router.post("/chat")
def chat(request: ChatRequest):

    result = generate_answer(
        query=request.query,
        user_id=request.user_id
    )

    return result