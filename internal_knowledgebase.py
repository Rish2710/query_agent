import chromadb
import json
import requests
from config import CHROMADB_PATH, GINA_API_URL, GINA_API_KEY

# Initialize ChromaDB Client
client = chromadb.PersistentClient(path=CHROMADB_PATH)
collection = client.get_or_create_collection(name="analytics_reports")

def generate_embedding(text):
    """Generates embeddings using Gina API."""
    headers = {"Authorization": f"Bearer {GINA_API_KEY}", "Content-Type": "application/json"}
    payload = json.dumps({
        "model": "jina-embeddings-v2-base-en",
        "input": [text]
    })
    response = requests.request("POST", GINA_API_URL, headers=headers, data=payload)
    return response.json()['data'][0]['embedding']


def search_reports(query):
    """Searches for relevant reports in ChromaDB."""
    vector = generate_embedding(query)
    results = collection.query(query_embeddings=[vector], n_results=1)
    return results["metadatas"][0] if results["ids"] else None
