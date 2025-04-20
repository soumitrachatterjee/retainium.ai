# Copyright (C) 2024-2025 Soumitra Chatterjee
# Licensed under the GNU AGPL-3.0. See LICENSE file for details.

# Module to import knowledge to the database from a file

# Import required modules
import os
import json
from retainium.diagnostics import Diagnostics
from retainium.text_utils import chunk_text, extract_and_chunk_pdf

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
            elif args.input.endswith(".pdf"):
                # Create a list of JSON entries using the chunks of text from the PDF
                chunks = extract_and_chunk_pdf(args.input)
                Diagnostics.note(f"pdf file chunked into {len(chunks)} chunks")
                json_data = [{ "text": chunk } for chunk in chunks]
            else:
                # Load plain-text data from file and wrap into JSON
                chunks = chunk_text(f.read())
                Diagnostics.note(f"text file chunked into {len(chunks)} chunks")
                json_data = [{ "text": chunk } for chunk in chunks]
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
        source = os.path.realpath(args.input)

        # Add the knowledge to the database
        try:
            knowledge_db.add_entry(text, source, embedding_handler, llm_handler)
        except Exception as e:
            Diagnostics.error(f"failed to add entry: {e}")

