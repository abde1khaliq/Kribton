import time
from pathlib import Path
from typing import Optional

import typer
import questionary
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree

from cli.style import console, Q_STYLE
from cli.new_module import new_module as scaffold_module


FILE_ROLES = [
    ("router.py",       "#185FA5", "routing"),
    ("controller.py",   "#534AB7", "handlers"),
    ("service.py",      "#3B6D11", "logic"),
    ("repository.py",   "#0F6E56", "data access"),
    ("schemas.py",      "#854F0B", "validation"),
    ("models.py",       "#993C1D", "ORM"),
    ("dependencies.py", "#5F5E5A", "DI"),
    ("events.py",       "#993356", "domain events"),
    ("exceptions.py",   "#A32D2D", "errors"),
]


def run_new_module(name: Optional[str]) -> None:
    console.print()

    if not name:
        name = questionary.text(
            "Module name",
            style=Q_STYLE,
        ).ask()

    if not name:
        raise typer.Exit()

    project_root = Path.cwd()
    module_path  = project_root / "app" / "modules" / name

    if module_path.exists():
        console.print(f"\n  [error]✕[/error]  Module [bold]{name}[/bold] already exists\n")
        raise typer.Exit(1)

    start = time.monotonic()

    with Progress(
        SpinnerColumn(spinner_name="dots", style="accent"),
        TextColumn("[muted]{task.description}[/muted]"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(f"Scaffolding {name}...", total=None)
        scaffold_module(name, project_root)

    elapsed = time.monotonic() - start

    console.print(
        f"  [success]✓[/success]  [bold]{name}[/bold] "
        f"[muted]scaffolded in {elapsed:.1f}s[/muted]"
    )
    console.print()

    tree = Tree(
        f"[muted]app/modules/[/muted][bold]{name}/[/bold]",
        guide_style="muted",
    )
    for filename, color, role in FILE_ROLES:
        tree.add(f"[bold]{filename}[/bold]  [{color} dim]{role}[/]")

    console.print(tree)
    console.print()