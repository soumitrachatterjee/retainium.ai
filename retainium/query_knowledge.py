from retainium.diagnostics import Diagnostics

def register_query_knowledge_command(subparsers):
    parser = subparsers.add_parser("query", help="Query the knowledge base")
    parser.add_argument("--text", required=True, help="Text to search for")
    parser.add_argument("--llm", action="store_true", help="Summarize results using LLM")
    parser.set_defaults(func=run)

def run(args, knowledge_db, embedding_handler, llm_handler=None):
    query_text = args.text.strip()
    if not query_text:
        Diagnostics.error("Query text is empty.")
        return
    Diagnostics.note(f"Searching for: {query_text}")

    embedding = embedding_handler.get_embedding(query_text)
    results = knowledge_db.query(embedding)

    if not results or not results.get("documents") or not results["documents"][0]:
        Diagnostics.warning("No similar entries found.")
        return

    Diagnostics.note("Top matches:")
    for doc, metadata, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        print(f"- Text: {doc}")
        print(f"  Metadata: {metadata}")
        print(f"  Distance: {dist:.4f}\n")

    if args.llm and llm_handler:
        context = "\n\n".join(results["documents"][0])
        response = llm_handler.generate_response(f"Summarize the following:\n{context}")
        print("\nLLM Summary:")
        print(response)
