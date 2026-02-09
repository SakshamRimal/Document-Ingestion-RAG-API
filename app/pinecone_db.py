import os
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from app.embeddings import get_embeddings

INDEX_NAME = "palmmindproject"

def get_vectorstore():
    # Initialize Pinecone with new SDK
    pc = Pinecone(
        api_key=os.getenv("PINECONE_API_KEY")
    )
    
    # Create index if it doesn't exist
    existing_indexes = [idx["name"] for idx in pc.list_indexes()]
    if INDEX_NAME not in existing_indexes:
        pc.create_index(
            name=INDEX_NAME,
            dimension=384,
            metric="cosine",
            spec={
                "serverless": {
                    "cloud": "aws",
                    "region": "us-east-1"
                }
            }
        )
    
    # Connect to the index using LangChain wrapper
    return PineconeVectorStore.from_existing_index(
        index_name=INDEX_NAME,
        embedding=get_embeddings()
    )
