import os
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from Backend.app.core.config import settings

class PineconeRAGService:
    def __init__(self):
        self.embedding_model = None
        self.pinecone_index = None
        self.local_documents = [] # Fallback document store if Pinecone API key is not set
        
    def _lazy_init(self):
        if self.embedding_model is None:
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
            
        if settings.PINECONE_API_KEY and self.pinecone_index is None:
            try:
                import pinecone
                pinecone.init(
                    api_key=settings.PINECONE_API_KEY,
                    environment=settings.PINECONE_ENVIRONMENT
                )
                if settings.PINECONE_INDEX_NAME in pinecone.list_indexes():
                    self.pinecone_index = pinecone.Index(settings.PINECONE_INDEX_NAME)
            except Exception as e:
                print(f"Warning: Pinecone initialization failed: {e}. Falling back to local search.")

    def add_documents(self, filename: str, chunks: List[str]) -> int:
        self._lazy_init()
        embeddings = self.embedding_model.encode(chunks)
        
        if self.pinecone_index:
            vectors = []
            for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
                vectors.append((
                    f"{filename}_chunk_{i}",
                    emb.tolist(),
                    {"filename": filename, "text": chunk}
                ))
            self.pinecone_index.upsert(vectors=vectors)
        else:
            for chunk, emb in zip(chunks, embeddings):
                self.local_documents.append({
                    "filename": filename,
                    "text": chunk,
                    "embedding": emb
                })
        return len(chunks)

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        self._lazy_init()
        query_emb = self.embedding_model.encode(query)
        
        if self.pinecone_index:
            try:
                res = self.pinecone_index.query(
                    vector=query_emb.tolist(),
                    top_k=top_k,
                    include_metadata=True
                )
                matches = [match['metadata']['text'] for match in res.get('matches', [])]
                if matches:
                    return matches
            except Exception as e:
                print(f"Pinecone query error: {e}")
                
        # Local cosine similarity fallback
        if not self.local_documents:
            return []
            
        import numpy as np
        scores = []
        for doc in self.local_documents:
            sim = np.dot(query_emb, doc['embedding']) / (np.linalg.norm(query_emb) * np.linalg.norm(doc['embedding']))
            scores.append((sim, doc['text']))
            
        scores.sort(key=lambda x: x[0], reverse=True)
        return [text for score, text in scores[:top_k]]

rag_service = PineconeRAGService()
