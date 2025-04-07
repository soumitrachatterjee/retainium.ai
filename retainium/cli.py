import argparse
from retainium.diagnostics import Diagnostics
from retainium.llm import LLMHandler

def process_cli(knowledge_db, embedding_handler):
    parser = argparse.ArgumentParser(description="Retainium AI CLI - Personal Knowledge Database")

    # Enable debug output
    parser.add_argument("--debug", action="store_true", help="Enable debug output")

    # Restrict to similarity searches only (avoid LLM-based queries)
    parser.add_argument(
        "--similarity-only",
        action="store_true",
        help="Skip LLM and use similarity search only"
    )

    # Add subparsers for individual commands
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
        context = "\n".join(doc if isinstance(doc, str) else doc.get("document", "") for doc in results)
    
        # Initialize LLM
        llm_handler = LLMHandler()

        # Run the query
        if not args.similarity_only and llm_handler.enabled:
            try:
                response = llm_handler.query(args.text, context=context)

                # Emit the response from the LLM
                Diagnostics.note("query results (llm-based):")
                print("\n", response)
            except Exception as e:
                Diagnostics.warning(f"failed to invoke LLM: {e}")
                Diagnostics.note("(fall-back) similarity search results:")
                for i, doc in enumerate(results):
                    print(f"{i + 1}. {doc}")
        else:
            Diagnostics.note("similarity search results:")
            for i, doc in enumerate(results):
                print(f"{i + 1}. {doc}")

