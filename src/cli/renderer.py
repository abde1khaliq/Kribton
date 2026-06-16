from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates"

env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    undefined=StrictUndefined,
    keep_trailing_newline=True,
)

def render_template(template_name: str, context: dict) -> str:
    if not template_name:
        return ""
    return env.get_template(template_name).render(**context)