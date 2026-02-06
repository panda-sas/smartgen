"""Generate command for creating project artifacts."""
from pathlib import Path
import typer
from rich import print as rich_print
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from smartgen.services.domain_generator import DomainGeneratorService, GeneratorError
from smartgen.services.layout_generator import LayoutGeneratorService, LayoutGeneratorError

generate_app = typer.Typer(help="Generate project artifacts")


@generate_app.command("domain")
def generate_domain(
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode to show all inputs/outputs")
) -> None:
    """Generate domain elements based on SRS and DDD policy."""
    project_dir = Path.cwd()
    
    try:
        service = DomainGeneratorService(debug=debug)
        
        # Show progress spinner while generating
        progress = Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            transient=True,
        )
        
        with progress:
            task_id = progress.add_task("Generating domain layer...", start=True)
            result = service.generate_domain(project_dir)
            progress.update(task_id, description="Domain layer generated!")
        
        typer.echo(
            typer.style("✓ ", fg=typer.colors.GREEN)
            + f"Domain elements generated using provider '{result.provider_name}'."
        )
        
        typer.echo(
            typer.style("✓ ", fg=typer.colors.GREEN)
            + f"Generated {len(result.generated_files)} file(s):"
        )
        
        for file_path in result.generated_files:
            typer.echo(f"  - {file_path.relative_to(project_dir)}")
        
        rich_print(
            Panel.fit(
                "Domain layer has been generated successfully.\n"
                "Review the generated files and adjust as needed.",
                title="Success",
                border_style="green",
            )
        )
        
    except GeneratorError as exc:
        typer.echo(typer.style("✗ ", fg=typer.colors.RED) + str(exc), err=True)
        raise typer.Exit(1)
    except Exception as exc:
        typer.echo(
            typer.style("✗ ", fg=typer.colors.RED) + f"Unexpected error: {exc}",
            err=True
        )
        raise typer.Exit(1)


@generate_app.command("layout")
def generate_layout(
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode to show all inputs/outputs")
) -> None:
    """Generate application layout structure based on SRS and policy."""
    project_dir = Path.cwd()
    
    try:
        service = LayoutGeneratorService(debug=debug)
        
        # Show progress spinner while generating
        progress = Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            transient=True,
        )
        
        with progress:
            task_id = progress.add_task("Generating application layout...", start=True)
            result = service.generate_layout(project_dir)
            progress.update(task_id, description="Application layout generated!")
        
        typer.echo(
            typer.style("✓ ", fg=typer.colors.GREEN)
            + f"Layout structure generated using provider '{result.provider_name}'."
        )
        
        typer.echo(
            typer.style("✓ ", fg=typer.colors.GREEN)
            + f"Generated {len(result.generated_files)} file(s):"
        )
        
        for file_path in result.generated_files:
            typer.echo(f"  - {file_path.relative_to(project_dir)}")
        
        rich_print(
            Panel.fit(
                "Application layout has been generated successfully.\n"
                "Review the generated files and adjust as needed.",
                title="Success",
                border_style="green",
            )
        )
        
    except LayoutGeneratorError as exc:
        typer.echo(typer.style("✗ ", fg=typer.colors.RED) + str(exc), err=True)
        raise typer.Exit(1)
    except Exception as exc:
        typer.echo(
            typer.style("✗ ", fg=typer.colors.RED) + f"Unexpected error: {exc}",
            err=True
        )
        raise typer.Exit(1)

