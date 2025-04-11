# Command line parsing module
import argparse
from retainium.diagnostics import Diagnostics
from retainium import add_knowledge, list_knowledge, query_knowledge, export_knowledge, rebuild_index

def process_cli(knowledge_db, embedding_handler, llm_handler):
    parser = argparse.ArgumentParser(prog="retainium.ai", description="Retainium AI - Personal Knowledge Database")

    # Enable debug support
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    
    # Create subparser group for commands
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Register all subcommands
    add_knowledge.register(subparsers)
    list_knowledge.register(subparsers)
    query_knowledge.register(subparsers)
    export_knowledge.register(subparsers)
    rebuild_index.register(subparsers)

    # Parse command line arguments
    args = parser.parse_args()

    # Enable debug mode if specified on the command line
    Diagnostics.enable_debug(args.debug)

    # Dispatch to the selected command's handler
    if hasattr(args, "func"):
        args.func(args, knowledge_db, embedding_handler, llm_handler)
    else:
        parser.print_help()
