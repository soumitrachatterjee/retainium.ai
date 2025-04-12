# Module to import knowledge to the database from a file

# Import required modules
import os
import json
from retainium.diagnostics import Diagnostics
from retainium.knowledge import KnowledgeEntry, compute_text_uuid

# Register command line options for "import"
def register(subparsers):
    parser = subparsers.add_parser("import", help="Import new knowledge entries from file")
    parser.add_argument("--input", required=True, help="Path to file containing knowledge (plain text or JSON)")
    parser.set_defaults(func=run)

# Handling of the "import" command
def run(args, knowledge_db, embedding_handler, llm_handler):
    json_data = None
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            if args.input.endswith(".json"):
                # Load the JSON data from the file
                json_data = json.load(f)

            else:
                input_text = f.read()
                json_data = {
                                "text": input_text,
                                "tags": [],
                                "source": os.path.basename(file_path),
                                "date": datetime.now().strftime('%Y-%m-%d')
                            }
    except Exception as e:
        Diagnostics.error(f"failed to read input file: {e}")
        return

    # Normalize: if it's a single entry (dict), wrap it in a list
    if isinstance(json_data, dict):
        entries = [json_data]
    elif isinstance(json_data, list):
        entries = json_data
    else:
        Diagnostics.error("invalid JSON format: expected a list or a dict.")

    # Add each entry into the knowledge database
    for entry in entries:
        text = entry["text"].strip()
        if not text:
            Diagnostics.error("text is required")
            continue
        source = os.path.realpath(__file__)
        tags = llm_handler.auto_tags(text)
        #date = datetime.now().strftime('%Y-%m-%d') # TODO 
        Diagnostics.debug(f"auto generated tags: {tags}")

        # Generate the knowledge entry and the corresponding embedding
        entry = KnowledgeEntry(id=compute_text_uuid(text), 
                               text=text, 
                               source=source, 
                               tags=tags)
        embedding_vector = embedding_handler.embed(text)

        # Add the knowledge to the database
        try:
            knowledge_db.add_entry(entry, embedding_vector)
        except Exception as e:
            Diagnostics.error(f"failed to add entry: {e}")

