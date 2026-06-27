from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db.init_db import init_db

# Create FastAPI app instance


# ----------------------------
# Lifespan handler (modern way)
# ----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_db()
    print("Database initialized ")

    yield  # app runs here

    # Shutdown logic (optional cleanup)
    print("Shutting down ContextFlow AI...")



app = FastAPI(
    title="ContextFlow AI",
    description="RAG + LangGraph + MCP powered AI system",
    version="0.1.0",
    lifespan=lifespan
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