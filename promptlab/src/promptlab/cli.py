"""promptlab.cli — the `wb lab` commands: run, sweep, history."""
import typer
from openai import OpenAI
from rich.console import Console
from rich.table import Table

from ai_workbench.config import get_settings
from ai_workbench.logsetup import setup_logging

from promptlab.journal import append_experiment, read_history
from promptlab.lab import experiment_to_dict, run_once, sweep as sweep_grid

lab_app = typer.Typer(help="Prompt lab — run, sweep and review experiments.")
console = Console()


def _client() -> tuple[OpenAI, str]:
    """Build an OpenAI-compatible client pointed at our local server."""
    s = get_settings()
    return OpenAI(base_url=s.base_url, api_key=s.api_key), s.model


def _parse_floats(text: str) -> list[float]:
    """Turn "0,0.5,1.0" into [0.0, 0.5, 1.0], forgiving stray spaces."""
    return [float(piece.strip()) for piece in text.split(",") if piece.strip()]


@lab_app.command()
def run(
    prompt: str,
    system: str = typer.Option("You are a helpful assistant.", help="System prompt."),
    temperature: float = typer.Option(0.7, min=0.0, max=2.0),
    top_p: float = typer.Option(0.9, min=0.0, max=1.0),
    max_tokens: int = typer.Option(500, help="Generation cap."),
) -> None:
    """Run ONE experiment, journal it, and show the result."""
    setup_logging()
    client, model = _client()
    exp = run_once(client, prompt, system, model, temperature, top_p, max_tokens)
    append_experiment(experiment_to_dict(exp))
    console.print(f"[bold]temp={exp.temperature} top_p={exp.top_p}[/bold] "
                  f"({exp.completion_tokens} tok, {exp.seconds}s)\n")
    console.print(exp.output)


@lab_app.command()
def sweep(
    prompt: str,
    system: str = typer.Option("You are a helpful assistant."),
    temperatures: str = typer.Option("0,0.5,1.0", help="Comma-separated, e.g. 0,0.5,1.0"),
    top_ps: str = typer.Option("0.9", help="Comma-separated, e.g. 0.9,1.0"),
) -> None:
    """Run the full parameter grid and journal every combination."""
    setup_logging()
    client, model = _client()
    temps, tops = _parse_floats(temperatures), _parse_floats(top_ps)
    console.print(f"Sweeping {len(temps)} x {len(tops)} = "
                  f"{len(temps) * len(tops)} runs...\n")
    for exp in sweep_grid(client, prompt, system, model, temps, tops):
        append_experiment(experiment_to_dict(exp))
        console.rule(f"temp={exp.temperature} top_p={exp.top_p} "
                     f"({exp.completion_tokens} tok, {exp.seconds}s)")
        console.print(exp.output)
    console.print(f"\n[green]Journaled {len(temps) * len(tops)} experiments.[/green]")


@lab_app.command()
def history(limit: int = typer.Option(10, help="How many experiments to show.")) -> None:
    """Render the last N experiments as a table."""
    records = read_history(limit)
    if not records:
        console.print("[yellow]No experiments yet. Run one first:[/yellow] "
                      "wb lab run \"Hello\"")
        raise typer.Exit()
    table = Table(title=f"Last {len(records)} experiments")
    table.add_column("Time (UTC)", style="dim")
    table.add_column("Prompt", max_width=40, overflow="ellipsis")
    table.add_column("Temp", justify="right")
    table.add_column("Tok", justify="right")
    table.add_column("Secs", justify="right")
    for r in records:
        table.add_row(
            r["ts"][:19].replace("T", " "),
            r["prompt"],
            str(r["temperature"]),
            str(r["completion_tokens"]),
            str(r["seconds"]),
        )
    console.print(table)


if __name__ == "__main__":
    lab_app()