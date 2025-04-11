# Module to export all knowledge to a file

import json
from retainium.diagnostics import Diagnostics

def register(subparsers):
    parser = subparsers.add_parser("export", help="Export all entries to JSON")
    parser.add_argument("--output", required=True, help="Path to output file")
    parser.set_defaults(func=run)

# Handling of the "export" command
def run(args, knowledge_db, *_):
    kb = knowledge_db.export_all()
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(kb, f, indent=2, ensure_ascii=False)
        Diagnostics.note(f"exported all entries to {args.output}")
    except Exception as e:
        Diagnostics.error(f"failed to export: {e}")

