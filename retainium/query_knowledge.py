from retainium.diagnostics import Diagnostics

def register_query_knowledge_command(subparser):
    parser = subparser.add_parser("query", help="Query the knowledge base")
    parser.add_argument("--text", required=True, help="Text to search for similar knowledge")
    parser.set_defaults(handler=run_query_knowledge_command)

def run_query_knowledge_command(args, knowledge_db, embedding_handler, llm_handler=None):
    query_text = args.text.strip()
    if not query_text:
        Diagnostics.error("Query text is empty.")
        return

    Diagnostics.note(f"Searching for: {query_text}")
    query_vector = embedding_handler.embed_text(query_text)
    results = knowledge_db.query(query_vector, top_k=5)

    if not results:
        Diagnostics.note("No similar entries found.")
        return

    Diagnostics.note(f"Top {len(results)} matches:")
    for result in results:
        print(f"- Score: {result.get('score', 0):.4f}")
        print(f"  Text: {result.get('document', '')}")
        print()
