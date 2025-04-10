# Module to list all knowledge from the database
import json
from retainium.diagnostics import Diagnostics
from retainium.knowledge import KnowledgeEntry

# Register command line options for "list"
def register(subparsers):
    parser = subparsers.add_parser("list", help="List all stored knowledge")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.set_defaults(func=run)

# Handling of the "list" command
def run(args, knowledge_db, embedding_handler, llm_handler):
    entries = knowledge_db.list_entries()
    if not entries:
        Diagnostics.warning("no entries found in knowledge database")
        return

    nr = len(entries)
    Diagnostics.note(f"listing {nr} stored knowledge entries:")
    for entry in entries:
        if args.json:
            print(json.dumps(entry.to_dict(), indent=2))
        else:
            metadata = entry.to_metadata()
            print(f"[{entry.id[:16]}] {entry.text} {metadata}")

