import argparse
from retainium.diagnostics import Diagnostics

def process_cli(knowledge_db, embedding_handler):
    parser = argparse.ArgumentParser(description="Retainium AI CLI - Personal Knowledge Database")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")  # Add debug flag
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

    # Enable debugging if --debug is set
    Diagnostics.enable_debug(args.debug)

    if args.command == "add":
        embedding = embedding_handler.embed_text(args.text)
        if embedding is None or not isinstance(embedding, list):
            Diagnostics.error("failed to generate embedding")
            return

        knowledge_db.add_entry(args.text, embedding)
        Diagnostics.note("knowledge added successfully")

    elif args.command == "list":
        entries = knowledge_db.list_entries()
        Diagnostics.debug(f"retrieved entries: {entries}")

        if not entries:
            Diagnostics.warning("no entries found")
        else:
            Diagnostics.note("stored knowledge entries:")
            for entry in entries:
                print(f"ID: {entry['id']}, Text: {entry['document']}")

    elif args.command == "query":
        embedding = embedding_handler.embed_text(args.text)
        Diagnostics.debug(f"generated embedding: {embedding}")

        if embedding is None or not isinstance(embedding, list):
            Diagnostics.error("failed to generate a valid embedding for the query")
            return

        results = knowledge_db.query(embedding)
        Diagnostics.debug(f"query results: {results}")

        if results and isinstance(results, list) and len(results) > 0:
            Diagnostics.note("query results:")
            for i, doc in enumerate(results):
                print(f"{i + 1}. {doc}")
        else:
            Diagnostics.warning("no relevant knowledge found")
