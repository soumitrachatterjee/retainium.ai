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
        metadata = entry.to_metadata()
        source = metadata["source"]
        tags = llm_handler.auto_tags(text)

        # Ignore empty entries, if any, with a warning
        if not text:
            Diagnostics.warning("ignoring entry with missing text")
            continue

        # Generate the knowledge entry and the corresponding embedding
        embedding_vector = embedding_handler.embed(text)
        kb = KnowledgeEntry(id=compute_text_uuid(text), 
                            text=text, 
                            source=source, 
                            tags=tags)

        # Add the knowledge to the database
        try:
            knowledge_db.add_entry(kb, embedding_vector)
            Diagnostics.debug(f"rebuilt index: {kb}")
        except Exception as e:
            Diagnostics.error(f"failed to add entry: {e}")

    # Report the number of entries in the re-initialized database
    entries = knowledge_db.list_entries()
    nr = len(entries)
    Diagnostics.note(f"database re-initialized with {nr} knowledge entries")

