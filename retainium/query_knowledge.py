# Module to query knowledge from the database
from retainium.diagnostics import Diagnostics
from retainium.knowledge import KnowledgeEntry

# Register command line options for "query"
def register(subparsers):
    parser = subparsers.add_parser("query", help="Query the knowledge base")
    parser.add_argument("--text", required=True, help="Text to search for")
    parser.add_argument("--llm", action="store_true", help="Summarize results using LLM")
    parser.set_defaults(func=run)

# Handling of the "query" command
def run(args, knowledge_db, embedding_handler, llm_handler):
    query_text = args.text.strip()
    if not query_text:
        Diagnostics.error("query text is empty")
        return
    Diagnostics.note(f"searching for: {query_text}")

    embedding = embedding_handler.embed(query_text)
    results = knowledge_db.query_entry(embedding)

    if not results:
        Diagnostics.warning(f"no matching entries found")
        return

    # Run the results through the LLM, unless prohibited
    nr = len(results)
    if args.llm and llm_handler:
        context = "\n".join(set(entry.text.strip() for entry in results))
        response = llm_handler.generate_response(f"Summarize the following:\n{context}")
        Diagnostics.note(f"LLM summary based on the top {nr} matching knowledge entries:")
        print(response)
    else:
        Diagnostics.note(f"listing top {nr} matching knowledge entries:")
        for entry in results:
            metadata = entry.to_metadata()
            print(f"[{entry.id}] {entry.text} {metadata}")

