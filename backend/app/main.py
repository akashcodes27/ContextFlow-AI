from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app instance
app = FastAPI(
    title="ContextFlow AI",
    description="RAG + LangGraph + MCP powered AI system",
    version="0.1.0"
)

# ----------------------------
# CORS (important for frontend)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later we will restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Health check route
# ----------------------------
@app.get("/")
def root():
    return {
        "message": "ContextFlow AI Backend is running 🚀"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }