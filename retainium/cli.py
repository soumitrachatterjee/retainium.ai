import argparse

def process_cli(knowledge_db, embedding_handler):
    parser = argparse.ArgumentParser(description="Retainium AI CLI - Personal Knowledge Database")
    parser.add_argument("command", choices=["add", "query"], help="Command to execute")
    parser.add_argument("--text", type=str, required=True, help="Text input for the command")
    args = parser.parse_args()

    if args.command == "add":
        embedding = embedding_handler.get_embedding(args.text)

        if embedding is None:
            print("Error: Failed to generate embedding.")
            return

        knowledge_db.add_entry(args.text, embedding)
        print("Knowledge added successfully.")
    
    elif args.command == "query":
        results = knowledge_db.query(args.text)
        print("Query Results:")
        for i, doc in enumerate(results.get("documents", [[]])[0]):
            print(f"{i+1}. {doc}")

