from retainium.diagnostics import Diagnostics

def register_query_knowledge_command(subparsers):
    parser = subparsers.add_parser("query", help="Query the knowledge base")
    parser.add_argument("query", help="Query string")
    parser.set_defaults(handler=run)

def run(args, knowledge_db, embedding_handler):
    results = knowledge_db.query(args.query)
    if not results:
        Diagnostics.warning("no matching knowledge found")
    else:
        Diagnostics.note("query results:")
        for entry in results:
            print(f"Score: {entry['score']:.3f}, Text: {entry['document']}")
