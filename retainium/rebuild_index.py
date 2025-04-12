# Module to rebuild the index for all existing knowledge in the database

# Import required modules
from retainium.diagnostics import Diagnostics
from retainium.knowledge import KnowledgeEntry, compute_text_uuid

# Register command line options for "rebuild-index"
def register(subparsers):
    parser = subparsers.add_parser("rebuild-index", help="Rebuild ChromaDB index from saved entries")
    parser.set_defaults(func=run)

# Handling of the "rebuild-index" command
def run(args, knowledge_db, embedding_handler, llm_handler):
    entries = knowledge_db.reinitialize_collection(knowledge_db)

    # Empty collection; nothing to rebuild
    if not entries:
        Diagnostics.warning("no existing entries in knowledge database")
        return

    # Re-initialize the database with the cached list of existing entries
    nr = len(entries)
    Diagnostics.note(f"rebuilding index for {nr} knowledge entries")
    for entry in entries:
        text = entry.text
        source = entry.to_metadata()["source"]

        # Add the knowledge to the database
        try:
            knowledge_db.add_entry(text, source, embedding_handler, llm_handler)
        except Exception as e:
            Diagnostics.error(f"failed to add entry: {e}")

    # Report the number of entries in the re-initialized database
    entries = knowledge_db.list_entries()
    nr = len(entries)
    Diagnostics.note(f"database re-initialized with {nr} knowledge entries")

