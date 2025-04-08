def parse_cli_tags(tag_list):
    if isinstance(tag_list, str):
        return tag_list.split(',')
    return tag_list if tag_list else []
