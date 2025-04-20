# Copyright (C) 2024-2025 Soumitra Chatterjee
# Licensed under the GNU AGPL-3.0. See LICENSE file for details.

# Module to list all knowledge from the database
import json
from retainium.diagnostics import Diagnostics
from retainium.knowledge import KnowledgeEntry

# Register command line options for "list"
def register(subparsers):
    parser = subparsers.add_parser("list", help="List all stored knowledge")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--terse", action="store_true", help="List brief ids")
    parser.set_defaults(func=run)

# Handling of the "list" command
def run(args, knowledge_db, embedding_handler, llm_handler):
    entries = knowledge_db.list_entries()
    if not entries:
        Diagnostics.warning("no entries found in knowledge database")
        return

    nr = len(entries)
    Diagnostics.note(f"listing {nr} stored knowledge entries:")
    for entry in entries:
        if args.json:
            print(json.dumps(entry.to_dict(), indent=2))
        else:
            metadata = entry.to_metadata()
            id = entry.id
            if args.terse:
                id = entry.id[:16]
            print(f"[{id}]\n{entry.text} {metadata}\n\n")

