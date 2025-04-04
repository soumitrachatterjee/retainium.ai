import argparse

def process_cli(knowledge_db, embedding_handler):
    parser = argparse.ArgumentParser(description="Retainium AI CLI - Personal Knowledge Database")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add Command
    add_parser = subparsers.add_parser("add", help="Add a new entry")
    add_parser.add_argument("--text", type=str, required=True, help="Text input for the entry")

    # Query Command
    query_parser = subparsers.add_parser("query", help="Query knowledge base")
    query_parser.add_argument("--text", type=str, required=True, help="Query text")

    # List Command
    subparsers.add_parser("list", help="List all stored knowledge")

    args = parser.parse_args()

    if args.command == "add":
        embedding = embedding_handler.embed_text(args.text)

        if embedding is None or not isinstance(embedding, list):
            print("Error: Failed to generate a valid embedding.")
            return

        knowledge_db.add_entry(args.text, embedding)
        print("Knowledge added successfully.")
    
    elif args.command == "list":
        entries = knowledge_db.list_entries()
        print("DEBUG: Retrieved entries:", entries)

        if not entries:
            print("No entries found.")
        else:
            print("Stored Knowledge Entries:")
            for entry in entries:
                print(f"ID: {entry['id']}, Text: {entry['document']}")

    elif args.command == "query":
        embedding = embedding_handler.embed_text(args.text)

        if embedding is None or not isinstance(embedding, list):
            print("Error: Failed to generate a valid embedding for the query.")
            return

        print(f"DEBUG: Generated embedding: {embedding}")
        results = knowledge_db.query(embedding)  # Removed 'text' from parameters
        print(f"DEBUG: Query results: {results}")

        if results and isinstance(results, list) and len(results) > 0:
            print("Query Results:")
            for i, doc in enumerate(results):
                print(f"{i + 1}. {doc}")
        else:
            print("No relevant knowledge found.")
