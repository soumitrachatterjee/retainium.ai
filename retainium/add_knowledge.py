# retainium/add_knowledge.py

import uuid
from retainium.diagnostics import Diagnostics
from retainium.knowledge import KnowledgeEntry

def register_add_knowledge_command(subparsers):
    parser = subparsers.add_parser("add", help="Add a new knowledge entry")
    parser.add_argument("--text", type=str, required=True, help="Text content of the entry")
    parser.add_argument("--tags", nargs="*", help="Optional tags for the entry")
    parser.add_argument("--source", type=str, help="Source of the entry (e.g., CLI, URL, etc.)")
    parser.set_defaults(func=run)

def run(args, knowledge_db, embedding_handler, llm_handler):
    text = args.text.strip()
    source = args.source or "CLI"
    tags = args.tags or []

    if not text:
        Diagnostics.error("Text is required.")
        return

    entry = KnowledgeEntry(id=str(uuid.uuid4()), text=text, source=source, tags=tags)
    embedding_vector = embedding_handler.embed(entry.text)

    try:
        knowledge_db.add_entry(entry, embedding_vector)
        Diagnostics.note("Entry added successfully.")
    except Exception as e:
        Diagnostics.error(f"Failed to add entry: {e}")
