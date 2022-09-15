import re

from logger import logdebug, LOG

from enum import Enum, auto

file_pattern = re.compile(r'^(file:\/\/)')



guard_extension = re.compile(r'[\s\S]+(.guard)')
schema_file_pattern = re.compile(r'^(.+)\/([^\/]+)(\.json)$')
guard_file_pattern = re.compile(r'^(.+)\/([^\/]+)(\.guard)$')

json_path_extract_pattern = r"(?![file:\/])(.+)\/([^\/]+)(\.json)$"
guard_path_extract_pattern = r"(?![file:\/])(.+)\/([^\/]+)(\.guard)$"


@logdebug
def is_guard_rule(input: str) -> bool:
    return bool(re.search(guard_extension, input))

@logdebug
def read_file(file_path: str):
    try:
        with open(file_path, "r", encoding='utf8') as file:
            return file.read()
    except IOError as ex:
        LOG.info("File not found. Please check the path.")
        raise ex