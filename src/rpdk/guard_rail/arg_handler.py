import argparse
from functools import wraps
import json
from typing import Sequence
import re
from rpdk.guard_rail.logger import logdebug, LOG
from rpdk.guard_rail.utils.common import (
    schema_file_pattern, 
    guard_file_pattern,
    json_path_extract_pattern, 
    guard_path_extract_pattern, 
    read_file, 
    file_pattern
)



def apply_rule(execute_rule, msg, /):
    def validation_wrapper(func: object):
        @wraps(func)
        def wrapper(args):
            assert execute_rule(args), msg
            return func(args)
        return wrapper
    return validation_wrapper

@apply_rule(
    lambda args:len(args.schemas) == 2 if args.statefull == True else True, 
    "If Statefull mode is executed, then two schemas MUST be provided (current/previous)"
)
def argument_validation(args: argparse.Namespace):
    pass


@logdebug
def setup_args():
    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="v0.1alpha"
    )
    
    parser.add_argument(
        "--schema", 
        dest="schemas",
        action="extend", 
        nargs="+", 
        type=str,
        required=True,
        help="Should specify schema for CFN compliance evaluation (path or plain value)"
    )
    
    parser.add_argument(
        "--statefull", 
        dest="statefull",
        action="store_true",
        default=False,
        help="If specified will execute statefull compliance evaluation"
    )
    
    parser.add_argument(
        "--format", 
        dest="format",
        action="store_false",
        default=False,
        help="Should specify schema for CFN compliance evaluation (path or plain value)"
    )
    
    parser.add_argument(
        "--rules",
        dest="rules",
        action="extend", 
        nargs="+",
        type=str,
        help="Should specify additional rules for compliance evaluation (path of `.guard` file)"
    )
    
    return parser

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

