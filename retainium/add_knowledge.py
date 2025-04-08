# retainium/add_knowledge.py

from retainium.diagnostics import Diagnostics
from retainium.knowledge import KnowledgeEntry

def register_add_knowledge_command(subparsers):
    parser = subparsers.add_parser("add", help="Add a new knowledge entry")
    parser.add_argument("--text", type=str, required=True, help="Text content of the entry")
    parser.add_argument("--tags", nargs="*", help="Optional tags for the entry")
    parser.add_argument("--source", type=str, help="Source of the entry (e.g., CLI, URL, etc.)")
    parser.set_defaults(func=run)

def run(args, knowledge_db, embedding_handler, llm_handler=None):
    text = args.text.strip()
    source = args.source or "CLI"
    tags = args.tags or []

    if not text:
        Diagnostics.error("Text is required.")
        return

    try:
        entry = KnowledgeEntry(text=text, source=source, tags=tags).to_dict()
        embedding_vector = embedding_handler.embed(entry["text"])

        knowledge_db.add_entry(entry, embedding_vector)
        Diagnostics.note("Entry added successfully.")
    except Exception as e:
        Diagnostics.error(f"Failed to add entry: {e}")
