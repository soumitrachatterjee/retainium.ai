# Module to add knowledge to the database

import hashlib
import base64
from retainium.diagnostics import Diagnostics
from retainium.knowledge import KnowledgeEntry

# Register command line options for "add"
def register(subparsers):
    parser = subparsers.add_parser("add", help="Add a new knowledge entry")
    parser.add_argument("--text", type=str, required=True, help="Text content of the entry")
    parser.add_argument("--tags", nargs="*", help="Optional tags for the entry")
    parser.add_argument("--source", type=str, help="Source of the entry (e.g., CLI, URL, etc.)")
    parser.set_defaults(func=run)

# Compute a hash from the text to serve as the unique id and to aid deduplication
def compute_text_uuid(text: str) -> str:
    sha256_digest = hashlib.sha256(text.strip().encode("utf-8")).digest()
    return base64.urlsafe_b64encode(sha256_digest).decode("utf-8").rstrip("=")

# Handling of the "add" command
def run(args, knowledge_db, embedding_handler, llm_handler):
    text = args.text.strip()
    source = args.source or "CLI"
    tags = args.tags or []

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

