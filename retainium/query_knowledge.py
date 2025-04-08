# retainium/query_knowledge.py

from retainium.diagnostics import Diagnostics

def register_query_knowledge_command(subparsers):
    parser = subparsers.add_parser("query", help="Query the knowledge base")
    parser.add_argument("--text", required=True, help="Text to search for")
    parser.add_argument("--llm", action="store_true", help="Summarize results using LLM")
    parser.set_defaults(handler=run)

def run(args, knowledge_db, embedding_handler, llm_handler=None):
    query_text = args.text.strip()
    if not query_text:
        Diagnostics.error("Query text is empty.")
        return

    Diagnostics.note(f"Searching for: {query_text}")
    embedding = embedding_handler.embed_text(query_text)
    results = knowledge_db.query_similar(embedding)

    if not results:
        Diagnostics.warning("No similar entries found.")
        return

    Diagnostics.note("Top matching entries:")
    for entry in results:
        print(f"- Text: {entry.text[:100]}{'...' if len(entry.text) > 100 else ''}")
        print(f"  Source: {entry.source}")
        print(f"  Tags: {entry.tags}")
        print()

    if args.llm and llm_handler:
        context = "\n\n".join(entry.text for entry in results)
        response = llm_handler.generate_response(f"Summarize the following:\n{context}")
        print("\nLLM Summary:")
        print(response)
