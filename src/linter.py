
import importlib.resources as pkg_resources
import json
import cfn_guard_rs
import pathlib


def get_rules():
    rules = pathlib.Path(__file__).parent.joinpath("schema-linter-rules.guard").read_text()
    #pkg_resources.read_text("guard-rail", "schema_rules.guard")
    return rules


def get_schema():
    schema = pathlib.Path(__file__).parent.joinpath("sample-schema.json").read_text()
    #pkg_resources.read_text("guard-rail", "schema.json")
    return schema


guard_result = cfn_guard_rs.run_checks(json.dumps(get_schema()), get_rules())
# print(guard_result)
if guard_result.not_compliant:
    print("schema is not compliant")
    # for name, errs in guard_result.not_compliant.items():
    #     print(name)
else:
    print("schema is compliant")
    