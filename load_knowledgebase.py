import chromadb
import json
from config import CHROMADB_PATH
from internal_knowledgebase import generate_embedding

# Initialize ChromaDB Client
client = chromadb.PersistentClient(path=CHROMADB_PATH)
collection = client.get_or_create_collection(name="reports")


def load_reports():
    """Loads sample reports into ChromaDB if not already present."""
    with open("reports.json", "r") as f:
        reports = json.load(f)

    for report in reports:
        title = report["title"]
        desc = report["description"]
        vector = generate_embedding(title + " " + desc)

        collection.add(ids=[title], embeddings=[vector], metadatas=[{"title": title, "desc": desc}])