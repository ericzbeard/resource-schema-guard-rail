

import argparse

from arg_handler import collect_schemas, collect_rules
from guard_rail_lib import exec_library
# from colorama import colorama_text


"""
guard-rail 
--schema (scalar/list)
--rules (optional)
--version

"""

def main(args_in=None):
    print("Invoked")      
    parser = setup_args()
    args = parser.parse_args(args=args_in)
    print(args)
    all_schemas = collect_schemas(schemas=args.schemas)
    all_rules = collect_rules(rules=args.rules)
    print(all_rules)
    print(exec_library(all_schemas, all_rules))
    
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
    