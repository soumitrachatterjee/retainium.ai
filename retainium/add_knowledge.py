from retainium.diagnostics import Diagnostics

def register_subcommand(subparsers):
    parser = subparsers.add_parser("add", help="Add a new entry")
    parser.add_argument("--text", type=str, required=True, help="Text input for the entry")
    parser.set_defaults(func=run)

def run(args, knowledge_db, embedding_handler):
    embedding = embedding_handler.embed_text(args.text)
    if embedding is None or not isinstance(embedding, list):
        Diagnostics.error("failed to generate embedding")
        return

    knowledge_db.add_entry(args.text, embedding)
    Diagnostics.note("knowledge added successfully")
