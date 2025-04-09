def register_export_knowledge_command(subparsers):
    parser = subparsers.add_parser("export", help="Export all entries to JSON")
    parser.add_argument("--output", required=True, help="Path to output file")
    parser.set_defaults(func=run)

def run(args, knowledge_db, *_):
    knowledge_db.export_all(args.output)
