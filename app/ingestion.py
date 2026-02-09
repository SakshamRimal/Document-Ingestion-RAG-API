from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from app.pinecone_db import get_vectorstore
from app.db.crud import save_chunk
from sqlalchemy.orm import Session
import os

def ingest_document(file_path: str, chunk_strategy: str, db: Session):
    # Determine file type and use appropriate loader
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif file_ext == ".txt":
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")
    
    documents = loader.load()

    # Choose chunking strategy
    if chunk_strategy == "recursive":
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    else:
        splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=100)

    chunks = splitter.split_documents(documents)

    vectorstore = get_vectorstore()

    texts = [c.page_content for c in chunks]
    metadatas = [{"source": c.metadata.get("source"), "document_name": os.path.basename(file_path)} for c in chunks]

    # Upsert to Pinecone
    ids = vectorstore.add_texts(texts=texts, metadatas=metadatas)

    # Save metadata to DB
    for i, chunk in enumerate(chunks):
        save_chunk(
            db=db,
            document_name=os.path.basename(file_path),
            source=chunk.metadata.get("source"),
            chunk_text=chunk.page_content,
            chunk_index=i,
            vector_id=ids[i]
        )
