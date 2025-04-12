# Module to add knowledge to the database

# Import required modules
from retainium.diagnostics import Diagnostics
from retainium.knowledge import KnowledgeEntry, compute_text_uuid

# Register command line options for "add"
def register(subparsers):
    parser = subparsers.add_parser("add", help="Add a new knowledge entry")
    parser.add_argument("--text", type=str, required=True, help="Text content of the entry")
    parser.add_argument("--source", type=str, help="Source of the entry (e.g., CLI, URL, etc.)")
    parser.set_defaults(func=run)

# Handling of the "add" command
def run(args, knowledge_db, embedding_handler, llm_handler):
    text = args.text.strip()
    source = args.source or "CLI"
    tags = llm_handler.auto_tags(text)
    Diagnostics.debug(f"auto generated tags: {tags}")

    if not text:
        Diagnostics.error("text is required")
        return

    # Generate the knowledge entry and the corresponding embedding
    entry = KnowledgeEntry(id=compute_text_uuid(text), 
                           text=text, 
                           source=source, 
                           tags=tags)
    embedding_vector = embedding_handler.embed(entry.text)

    # Add the knowledge to the database
    try:
        knowledge_db.add_entry(entry, embedding_vector)
    except Exception as e:
        Diagnostics.error(f"failed to add entry: {e}")

