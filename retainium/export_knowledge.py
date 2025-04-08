import json
from retainium.diagnostics import Diagnostics

def register_export_knowledge_command(subparsers):
    parser = subparsers.add_parser("export", help="Export all entries to JSON")
    parser.add_argument("--output", required=True, help="Path to output file")
    parser.set_defaults(handler=run)

def run(args, knowledge_db, *_):
    entries = knowledge_db.export_all()
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2)
        Diagnostics.success(f"Exported {len(entries)} entries to {args.output}")
    except Exception as e:
        Diagnostics.error(f"Failed to export data: {e}")
