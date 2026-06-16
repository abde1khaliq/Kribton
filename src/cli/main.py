from typing import Optional

import typer

from cli.commands.init import run_init
from cli.commands.new import run_new_module

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode="rich",
    pretty_exceptions_enable=False,
    help="Anakonda",
)

new_app = typer.Typer(
    no_args_is_help=True,
    help="Scaffold a resource inside an existing project",
)

app.add_typer(new_app, name="new")


@app.command("init")
def init(
    project_name: Optional[str] = typer.Argument(None, help="Project directory name"),
) -> None:
    """Create a new project."""
    run_init(project_name)


@new_app.command("module")
def new_module(
    name: Optional[str] = typer.Argument(None, help="Module name (snake_case)"),
) -> None:
    """Add a new vertical-slice module to the project."""
    run_new_module(name)


if __name__ == "__main__":
    app()