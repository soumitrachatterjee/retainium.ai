from retainium.diagnostics import Diagnostics

def register_subcommand(subparsers):
    parser = subparsers.add_parser("list", help="List all stored knowledge")
    parser.set_defaults(func=run)

def run(args, knowledge_db, embedding_handler):
    entries = knowledge_db.list_entries()
    Diagnostics.debug(f"retrieved entries: {entries}")

    if not entries:
        Diagnostics.warning("no entries found")
    else:
        Diagnostics.note("stored knowledge entries:")
        for entry in entries:
            print(f"ID: {entry['id']}, Text: {entry['document']}")
