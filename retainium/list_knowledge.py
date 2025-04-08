from retainium.diagnostics import Diagnostics

def register_list_knowledge_command(subparsers):
    parser = subparsers.add_parser("list", help="List all stored knowledge")
    parser.set_defaults(handler=run)

def run(args, knowledge_db, embedding_handler):
    entries = knowledge_db.list_entries()

    if not entries:
        Diagnostics.warning("no entries found")
        return

    Diagnostics.note("stored knowledge entries:")
    for entry in entries:
        entry_id = entry.get("id", "<no-id>")
        text = entry.get("text") or entry.get("document", {}).get("text", "<no-text>")
        tags = entry.get("tags", [])
        source = entry.get("source", "")

        print(f"- ID: {entry_id}")
        print(f"  Text: {text[:100]}{'...' if len(text) > 100 else ''}")
        print(f"  Tags: {tags}")
        print(f"  Source: {source}")
        print()
