import json
from typing import Sequence
import re
from logger import logdebug, LOG
from common import (
    is_guard_rule, 
    schema_file_pattern, 
    guard_file_pattern,
    json_path_extract_pattern, 
    guard_path_extract_pattern, 
    read_file, 
    file_pattern
)

@logdebug
def input_path_validation(input_path: str):
    if not re.search(file_pattern, input_path):
        LOG.info(f"{input_path} is not starting with `file://...`")
        raise ValueError("file path must be specified with `file://...`")



@logdebug
def collect_schemas(schemas: Sequence[str]=None):
    _schemas = []
    
    @logdebug
    def __to_json(schema_raw: str):
        try:
            return json.loads(schema_raw)
        except json.JSONDecodeError as ex:
            raise ValueError(f"Invalid Schema Body {ex}")
        
    if schemas:
        for schema_item in schemas:

            input_path_validation(schema_item)
            
            if re.search(schema_file_pattern, schema_item):
                path = "/" + re.search(json_path_extract_pattern, schema_item).group(0)
                file_obj = read_file(path)
                _schemas.append(__to_json(file_obj))
            else:
                schema_deser = __to_json(schema_item)
                _schemas.append(schema_deser)
    return _schemas
        


    

@logdebug
def collect_rules(rules: Sequence[str]=None):
    _rules = []
    if rules:
        for rule in rules:
            input_path_validation(rule)
            
            if re.search(guard_file_pattern, rule):
                path = "/" + re.search(guard_path_extract_pattern, rule).group(0)
                file_obj = read_file(path)
                _rules.append(file_obj)
            
            else:
                raise ValueError("file extenstion is invalid - MUST be `.guard`")
    return _rules

