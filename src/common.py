import re

guard_extension = re.compile(r'[\s\S]+(.guard)')

def is_guard_rule(input: str) -> bool:
    return bool(re.search(guard_extension, input))