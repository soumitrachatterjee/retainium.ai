from retainium.diagnostics import Diagnostics
from retainium.llm import LLMHandler

def register_subcommand(subparsers):
    parser = subparsers.add_parser("query", help="Query knowledge base")
    parser.add_argument("--text", type=str, required=True, help="Query text")
    parser.set_defaults(func=run)

def run(args, knowledge_db, embedding_handler):
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
            Diagnostics.note("query results (llm-based)")
            print(f"{response}")
        except Exception as e:
            Diagnostics.warning(f"failed to invoke LLM: {e}")
            Diagnostics.note("(fall-back) similarity search results:")
            for i, doc in enumerate(results):
                print(f"{i + 1}. {doc}")
    else:
        Diagnostics.note("similarity search results:")
        for i, doc in enumerate(results):
            print(f"{i + 1}. {doc}")
