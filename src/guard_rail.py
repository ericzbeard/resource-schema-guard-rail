

from rpdk.guard_rail.arg_handler import setup_args, collect_schemas, collect_rules, argument_validation
from rpdk.guard_rail.core.runner import exec_compliance
from rpdk.guard_rail.core.data_types import Stateless, Statefull
# from colorama import colorama_text

def main(args_in=None):
    parser = setup_args()
    args = parser.parse_args(args=args_in)
    argument_validation(args)
    
    
    all_schemas = collect_schemas(schemas=args.schemas)
    all_rules = collect_rules(rules=args.rules)
    
    
    payload = Stateless(schemas=all_schemas, rules=all_rules)
    out = exec_compliance(payload)
    # out = exec_compliance(Statefull(current_schema={}, previous_schema={}))
    for item in out:
        print()
        print(item)
    print()
    
    