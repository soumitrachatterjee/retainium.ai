from retainium.add_knowledge import register_add_knowledge_command
from retainium.list_knowledge import register_list_knowledge_command
from retainium.query_knowledge import register_query_knowledge_command

def register_all_commands(subparsers):
    register_add_knowledge_command(subparsers)
    register_list_knowledge_command(subparsers)
    register_query_knowledge_command(subparsers)
