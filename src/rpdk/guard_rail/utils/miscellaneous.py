
from jinja2 import Environment, FileSystemLoader, PackageLoader, ChoiceLoader, select_autoescape
from pathlib import Path
from importlib.util import find_spec

def jinja_loader(module_name):
    options = {}
    spec = find_spec(module_name)
    
    if spec is None or spec.origin is None:
        loader = PackageLoader(module_name)
    else:
        path = Path(spec.origin).resolve(strict=True)
        print(str(path.parent / "templates"))
        loader = FileSystemLoader(str(path.parent / "templates"))
    options["loader"] = ChoiceLoader([loader, PackageLoader(module_name)])
    if "autoescape" not in options:
        options["autoescape"] = select_autoescape(["html", "htm", "xml"])

    # bandit doesn't detect if we set "autoescape" dynamically
    env = Environment(**options)
    return env

