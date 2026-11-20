"""ai_workbench.cli - the front door of the AI workbench."""

import platform
import sys

import typer
from rich.console import Console
from rich.table import Table
from promptlab.cli import lab_app



app = typer.Typer(help="AI Workbench - your local-first AI toolkit.")
app.add_typer(lab_app, name="lab")
console = Console()


@app.command()
def doctor() -> None:
    """Check that your workbench is healthy."""
    table = Table(title="AI Workbench health check")
    table.add_column("Check", style="cyan")
    table.add_column("Result", style="green")
    table.add_row("Python version", platform.python_version())
    table.add_row("Platform", platform.system())
    ok = sys.version_info >= (3, 11)
    table.add_row("Python >= 3.11", "yes" if ok else "No - upgrade Python!")

    console.print(table)
    if not ok:
        raise typer.Exit(code=1)


@app.command()
def hello(name: str = "engineer") -> None:
    """Say Hello, warmly."""
    console.print(f"[bold green] Welcome to the workbench, {name}![/bold green]")


if __name__ == "__main__":
    app()
