"""Project initialization command."""
from pathlib import Path
from typing import Any, Callable
import typer
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.panel import Panel
from rich import print as rich_print

from smartgen.services.llm_init import (
    LLMInitError,
    MissingApiKeyError,
    MissingConfigError,
    UnsupportedLocalProviderError,
    LLMInitService,
)


def init_command(
    language: str = typer.Option("python", help="Project language"),
    pattern: str = typer.Option("ddd", help="Project architecture pattern"),
    app: str = typer.Option("api", help="Application type"),
) -> None:
    """Initialize smartgen in the current directory."""
    progress = Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        BarColumn(),
        TextColumn("{task.fields[percent_text]}"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        transient=True,
    )

    def _build_progress_callback(progress_obj: Progress, task_id: int) -> Callable[[dict[str, Any]], None]:
        digest_totals: dict[str, int] = {}
        digest_completed: dict[str, int] = {}

        def _callback(payload: dict[str, Any]) -> None:
            total = payload.get("total")
            completed = payload.get("completed")
            status = payload.get("status")
            digest = payload.get("digest")

            if digest and isinstance(total, int):
                digest_totals[digest] = total
            if digest and isinstance(completed, int):
                digest_completed[digest] = completed

            sum_total = sum(digest_totals.values())
            sum_completed = sum(digest_completed.values())

            update_kwargs: dict[str, Any] = {}
            if sum_total > 0:
                update_kwargs["total"] = sum_total
                update_kwargs["completed"] = min(sum_completed, sum_total)
            if status:
                update_kwargs["description"] = f"Pulling Ollama model ({status})"
            if sum_total > 0:
                percent = (sum_completed / sum_total) * 100
                update_kwargs["percent_text"] = f"{percent:>3.0f}%"
            else:
                update_kwargs["percent_text"] = " --%"

            if update_kwargs:
                progress_obj.update(task_id, **update_kwargs)
            else:
                progress_obj.update(task_id, description="Pulling Ollama model")

        return _callback

    try:
        with progress:
            task_id = progress.add_task(
                "Pulling Ollama model",
                total=None,
                percent_text=" --%",
            )
            progress_callback = _build_progress_callback(progress, task_id)
            service = LLMInitService(
                ollama_progress_callback=progress_callback,
            )
            result = service.initialize(
                Path.cwd(),
                language=language,
                pattern=pattern,
                app=app,
            )
    except MissingApiKeyError as exc:
        typer.echo(typer.style("✗ ", fg=typer.colors.RED) + str(exc), err=True)
        raise typer.Exit(1)
    except (MissingConfigError, UnsupportedLocalProviderError) as exc:
        typer.echo(typer.style("✗ ", fg=typer.colors.RED) + str(exc), err=True)
        raise typer.Exit(1)
    except LLMInitError as exc:
        typer.echo(typer.style("✗ ", fg=typer.colors.RED) + str(exc), err=True)
        raise typer.Exit(1)

    typer.echo(
        typer.style("✓ ", fg=typer.colors.GREEN)
        + f"Initialized with provider '{result.provider_name}'."
    )

    if result.pull_response:
        typer.echo(
            typer.style("✓ ", fg=typer.colors.GREEN)
            + "Ollama model pulled successfully."
        )

    typer.echo(
        typer.style("✓ ", fg=typer.colors.GREEN)
        + f"Created {result.yaml_path.name} in {result.yaml_path.parent}"
    )

    rich_print(
        Panel.fit(
            "Blank Software Requirements Specification created at "
            f"{result.srs_path.name}.\n"
            "Please provide the initial requirement to get started.",
            title="Next step",
            border_style="yellow",
        )
    )
