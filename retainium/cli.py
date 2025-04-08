# retainium/cli.py

import argparse
from retainium import add_knowledge, list_knowledge, query_knowledge, export_knowledge, rebuild_index

def process_cli(knowledge_db, embedding_handler, llm_handler):
    parser = argparse.ArgumentParser(prog="retainium", description="CLI for knowledge retention and search")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Register all subcommands
    add_knowledge.register_add_knowledge_command(subparsers)
    list_knowledge.register_list_knowledge_command(subparsers)
    query_knowledge.register_query_knowledge_command(subparsers)
    export_knowledge.register_export_knowledge_command(subparsers)
    rebuild_index.register_rebuild_index_command(subparsers)

    args = parser.parse_args()

    # Dispatch to the selected command's handler
    if hasattr(args, "func"):
        args.func(args, knowledge_db, embedding_handler, llm_handler)
    else:
        parser.print_help()
