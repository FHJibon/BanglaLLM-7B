from fastapi import APIRouter, UploadFile, File, HTTPException
from Backend.app.schemas.chat import DocumentUploadResponse
from Backend.app.utils.text_processor import parse_file_content, chunk_text
from Backend.app.services.pinecone_rag import rag_service

router = APIRouter()

@router.post("/admin/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected.")
        
    ext = file.filename.split('.')[-1].lower()
    if ext not in ['pdf', 'txt', 'md']:
        raise HTTPException(status_code=400, detail="Only PDF, TXT, and MD files are supported.")
        
    content_bytes = await file.read()
    raw_text = parse_file_content(file.filename, content_bytes)
    chunks = chunk_text(raw_text)
    
    if not chunks:
        raise HTTPException(status_code=400, detail="No text could be extracted from document.")
        
    num_indexed = rag_service.add_documents(file.filename, chunks)
    
    return DocumentUploadResponse(
        filename=file.filename,
        status="Success",
        num_chunks=num_indexed,
        message=f"Successfully indexed {num_indexed} chunks into the vector store."
    )
