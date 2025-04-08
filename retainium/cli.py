import argparse
import importlib
from retainium.diagnostics import Diagnostics

# List of subcommand modules to register
SUBCOMMAND_MODULES = [
    "retainium.add_knowledge",
    "retainium.list_knowledge",
    "retainium.query_knowledge",
]

def process_cli(knowledge_db, embedding_handler):
    parser = argparse.ArgumentParser(description="Retainium AI CLI - Personal Knowledge Database")

    # Global options
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument(
        "--similarity-only",
        action="store_true",
        help="Skip LLM and use similarity search only"
    )

    # Subparsers
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Dynamically register all subcommands
    for module_name in SUBCOMMAND_MODULES:
        module = importlib.import_module(module_name)
        if hasattr(module, "register_subcommand"):
            module.register_subcommand(subparsers)

    args = parser.parse_args()

    # Enable diagnostics if requested
    Diagnostics.enable_debug(args.debug)

    # Dispatch to appropriate handler
    if hasattr(args, "func"):
        args.func(args, knowledge_db, embedding_handler)
    else:
        parser.print_help()
