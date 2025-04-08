import json
from retainium.diagnostics import Diagnostics

def register_add_knowledge_command(subparsers):
    parser = subparsers.add_parser("add", help="Add knowledge to the database")
    parser.add_argument("--text", help="Input knowledge as text")
    parser.add_argument("--file", help="Path to file containing knowledge (plain text or JSON)")
    parser.add_argument("--tags", nargs="+", help="Tags for metadata")
    parser.add_argument("--source", help="Source of the knowledge")
    parser.add_argument("--date", help="Date of knowledge")
    parser.set_defaults(handler=run)

def run(args, knowledge_db, embedding_handler):
    input_text = None

    if args.text:
        input_text = args.text
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                if args.file.endswith(".json"):
                    json_data = json.load(f)
                    input_text = json_data.get("text")
                    if not input_text:
                        Diagnostics.error("JSON file does not contain a 'text' field")
                        return
                    args.tags = json_data.get("tags", args.tags)
                    args.source = json_data.get("source", args.source)
                    args.date = json_data.get("date", args.date)
                else:
                    input_text = f.read()
        except Exception as e:
            Diagnostics.error(f"failed to read input file: {e}")
            return

    if not input_text:
        Diagnostics.error("no input text provided")
        return

    embedding = embedding_handler.embed_text(input_text)
    if embedding is None or not isinstance(embedding, list):
        Diagnostics.error("failed to generate embedding")
        return

    metadata = {}
    if args.tags:
        metadata["tags"] = args.tags
    if args.source:
        metadata["source"] = args.source
    if args.date:
        metadata["date"] = args.date

    knowledge_db.add_entry(input_text, embedding, metadata)
    Diagnostics.note("knowledge added successfully")
