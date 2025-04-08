from retainium.diagnostics import Diagnostics

def register_rebuild_index_command(subparsers):
    parser = subparsers.add_parser("rebuild-index", help="Rebuild ChromaDB index from saved entries")
    parser.set_defaults(handler=run)

def run(args, knowledge_db, embedding_handler, *_):
    entries = knowledge_db.get_all_entries()
    if not entries:
        Diagnostics.warning("No entries found to rebuild index.")
        return

    Diagnostics.note(f"Rebuilding index for {len(entries)} entries...")

    try:
        texts = [entry.text for entry in entries]
        embeddings = embedding_handler.model.encode(texts, convert_to_tensor=False)
        knowledge_db.rebuild_index(entries, embeddings)
        Diagnostics.success("ChromaDB index rebuilt successfully.")
    except Exception as e:
        Diagnostics.error(f"Failed to rebuild index: {e}")
