
from gc import get_referents
import importlib.resources as pkg_resources
import json
import cfn_guard_rs
import pathlib
from rule_library import core, combiners

from dataclasses import dataclass, field
import importlib.resources as pkg_resources


from typing import Any, Dict, List, Sequence
from common import is_guard_rule
from ast import literal_eval
from jinja2 import Environment, FileSystemLoader

from logger import LOG, logdebug



@dataclass
class GuardRuleResult:
    check_id: str = field(default="unidentified")
    message: str = field(default="unidentified")

@dataclass
class GuardRuleSetResult:
    compliant: List[str] = field(default_factory=list)
    non_compliant: Dict[str, List[GuardRuleResult]] = field(default_factory=dict)
    skipped: List[str] = field(default_factory=list)
    
    
    def merge(self, guard_ruleset_result: Any):
        if not isinstance(guard_ruleset_result, GuardRuleSetResult):
            raise TypeError("cannot merge with non GuardRuleSetResult type")
        
        self.compliant.extend(guard_ruleset_result.compliant)
        self.skipped.extend(guard_ruleset_result.skipped)
        self.non_compliant = {**self.non_compliant, **guard_ruleset_result.non_compliant}
    
    def __str__(self):
        
        if not self.compliant and not self.non_compliant and self.skipped:
            return "Couldn't retrieve the result"
        
        environment = Environment(loader=FileSystemLoader("templates/"))
        template = environment.get_template("guard-result-pojo.output")
        return template.render(
            skipped_rules = self.skipped,
            passed_rules = self.compliant,
            failed_rules = self.non_compliant
        )

@logdebug
def get_ruleset():
    static_rule_modules = [core, combiners]
    rule_set = set()
    for module in static_rule_modules:
        for content in pkg_resources.contents(module):
            if not is_guard_rule(content):
                continue
            rule_set.add(pkg_resources.read_text(module, content))
    return rule_set


# def get_ruleset(file_name: str):
#     return pathlib.Path(__file__).parent.joinpath(file_name).read_text()

@logdebug
def get_schema():
    schema = pathlib.Path(__file__).parent.joinpath("sample-schema.json").read_text()
    return json.loads(schema)


@logdebug
def exec_rules(schema: Dict):
    """Closure factory function for schema compliace execution - 
    Read rule compliance status and output guard rule set result
    Creates closure, modifies, and retains the previous state between calls (rule set evaluations)
    Args:
        schema ([Dict]): Resource Provider Schema
    Returns:
        [function]: Closure
    """
    exec_result = GuardRuleSetResult()
    
    @logdebug
    def __exec__(rules: str):
        guard_result = cfn_guard_rs.run_checks(schema, rules)
        def __render_output(evaluation_result: object):
            non_compliant = {}
            for rule_name, checks in guard_result.not_compliant.items():
                
                non_compliant[rule_name] = []
                
                for check in checks:
                    try:
                        _message_dict = literal_eval(check.message.strip())
                        non_compliant[rule_name].append(GuardRuleResult(check_id=_message_dict["check_id"], message=_message_dict["message"]))
                    except Exception as e:
                        LOG.info(str(e) + check.message)
                        non_compliant[rule_name].append(GuardRuleResult())
            
            return GuardRuleSetResult(
                compliant=evaluation_result.compliant,
                non_compliant=non_compliant,
                skipped=evaluation_result.not_applicable
            )

        exec_result.merge(__render_output(guard_result))
        return exec_result
        
    return __exec__
    

@logdebug
def exec_library(schemas: Sequence[Dict[str, Any]], rules: Sequence[str]=None):
    result = []
    
    
    def __execute(schema_exec, ruleset):
        output = None
        for rules in ruleset:
            output = schema_exec(rules)
        return output
    
    for schema in schemas:
        schema_exec = exec_rules(schema=schema)
        ruleset = get_ruleset() | set(rules if rules else {})
        output = __execute(schema_exec=schema_exec, ruleset=ruleset)
        result.append(output)
    
    return result    
    # kms_eval = exec_rules(schema)
    
    # output = None
        
    # for rules in get_ruleset():
    #     output = kms_eval(rules)
    # return output
    


if __name__ == "__main__":
    result = exec_library()
    print(result)
    