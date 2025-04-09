def register_rebuild_index_command(subparsers):
    parser = subparsers.add_parser("rebuild-index", help="Rebuild ChromaDB index from saved entries")
    parser.set_defaults(func=run)

def run(args, knowledge_db, *_):
    knowledge_db.rebuild_index()
