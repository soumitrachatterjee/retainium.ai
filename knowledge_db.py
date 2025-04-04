import chromadb
from sentence_transformers import SentenceTransformer
import os

# Initialize ChromaDB client
db = chromadb.PersistentClient(path="./knowledge_db")
collection = db.get_or_create_collection(name="knowledge")

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def add_knowledge(text):
    """Adds knowledge to the database."""
    embedding = embedding_model.encode(text).tolist()
    doc_id = str(len(collection.get()['ids']))  # Unique ID
    collection.add(ids=[doc_id], documents=[text], embeddings=[embedding])
    print("Knowledge added successfully!")

def query_knowledge(query):
    """Retrieves relevant knowledge based on query."""
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=3)
    
    if results["documents"]:
        print("Relevant knowledge found:")
        for doc in results["documents"][0]:
            print(f"- {doc}")
    else:
        print("No relevant knowledge found.")

def main():
    while True:
        print("\n1. Add Knowledge")
        print("2. Query Knowledge")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            text = input("Enter the knowledge to store: ")
            add_knowledge(text)
        elif choice == "2":
            query = input("Enter your query: ")
            query_knowledge(query)
        elif choice == "3":
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
