import os
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

def run_ingestion():
    print("[1/4] Initializing Nomic embedding model...")
    Settings.embed_model = OllamaEmbedding(
        model_name="nomic-embed-text",
        base_url=OLLAMA_HOST
    )

    print("[2/4] Connecting to Qdrant vector store...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    vector_store = QdrantVectorStore(client=client, collection_name="requirements")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print("[3/4] Reading requirement files from data/docs/...")
    documents = SimpleDirectoryReader("data/docs").load_data()
    print(f"Loaded {len(documents)} document chunk(s).")

    print("[4/4] Building vector index in Qdrant...")
    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True
    )
    print("? Ingestion complete! Requirements successfully stored in Qdrant.")

if __name__ == "__main__":
    run_ingestion()
