import argparse
from retainium.diagnostics import Diagnostics
from retainium.commands import register_all_commands

def process_cli(knowledge_db, embedding_handler, llm_handler):
    parser = argparse.ArgumentParser(description="Retainium AI CLI - Personal Knowledge Database")

    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument("--similarity-only", action="store_true", help="Skip LLM and use similarity search only")

    # Create subparser group for commands
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Register subcommands (add, list, query)
    register_all_commands(subparsers)

    args = parser.parse_args()

    Diagnostics.enable_debug(args.debug)

    # Dispatch to the appropriate command handler
    if hasattr(args, "handler"):
        args.handler(args, knowledge_db, embedding_handler)
    else:
        parser.print_help()
