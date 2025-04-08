import json
from retainium.diagnostics import Diagnostics

def register_list_knowledge_command(subparsers):
    parser = subparsers.add_parser("list", help="List all stored knowledge")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.set_defaults(handler=run)

def run(args, knowledge_db, *_):
    entries = knowledge_db.get_all_entries()
    if not entries:
        Diagnostics.warning("No entries found.")
        return

    if args.json:
        print(json.dumps([e.__dict__ for e in entries], indent=2))
        return

    Diagnostics.note("Stored knowledge entries:")
    for entry in entries:
        print(f"- ID: {entry.id}")
        print(f"  Text: {entry.text[:100]}{'...' if len(entry.text) > 100 else ''}")
        print(f"  Source: {entry.source}")
        print(f"  Tags: {entry.tags}")
        print()
