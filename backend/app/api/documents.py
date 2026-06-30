# api/documents.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import os
import shutil
import uuid

from app.db.session import get_db
from app.auth.dependencies import get_current_user
from app.db.models.user import User
from app.rag.ingest import ingest_document  

router = APIRouter(prefix="/documents", tags=["Documents"])


# Create a temporary directory for uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Upload a document to be ingested into the RAG system.
    Supported formats: PDF, DOCX, TXT, MD
    """
    # 1. Validate file type
    allowed_extensions = [".pdf", ".docx", ".txt", ".md", ".markdown"]
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # 2. Save the file temporarily
    file_id = str(uuid.uuid4())
    safe_filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # 3. 👇 THIS CALLS YOUR INGEST.PY!
    try:
        result = ingest_document(
            file_path=file_path,
            user_id=str(current_user.id),
            filename=file.filename,
        )
    except Exception as e:
        # Clean up the file if ingestion fails
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
    
    # 4. Optionally: Save document reference to PostgreSQL
    # (You'll need a Document model in your db/models.py)
    # new_doc = Document(
    #     id=result["document_id"],
    #     user_id=current_user.id,
    #     filename=file.filename,
    #     file_path=file_path,
    #     chunk_count=result["chunks"]
    # )
    # db.add(new_doc)
    # db.commit()
    
    # 5. Clean up the temporary file (optional)
    # os.remove(file_path)  # Uncomment if you don't want to keep the file
    
    return {
        "message": "Document uploaded and ingested successfully!",
        "document_id": result["document_id"],
        "filename": file.filename,
        "chunks": result["chunks"],
    }