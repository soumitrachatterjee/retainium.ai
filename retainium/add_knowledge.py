# Module to add knowledge to the database

# Import required modules
from retainium.diagnostics import Diagnostics

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

    # Add the knowledge to the database
    try:
        knowledge_db.add_entry(text, source, embedding_handler, llm_handler)
    except Exception as e:
        Diagnostics.error(f"failed to add entry: {e}")

