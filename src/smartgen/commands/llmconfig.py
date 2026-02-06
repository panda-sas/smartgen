"""LLM configuration command."""
import typer
from typing import Optional

from smartgen.config import ConfigManager

llmconfig_app = typer.Typer(help="Configure LLM settings")


@llmconfig_app.command()
def set_config(
    default: str = typer.Option(
        ..., help="Default LLM provider (e.g., openai, anthropic)"
    ),
    api_key: str = typer.Option(..., help="API key for the LLM provider"),
) -> None:
    """
    Save LLM configuration.
    
    Example:
        smartgen llmconfig --default=openai --api-key <your-api-key>
    """
    try:
        ConfigManager.update_llm_config(default=default, api_key=api_key)
        typer.echo(
            typer.style("✓ ", fg=typer.colors.GREEN)
            + f"LLM config saved: provider={default}"
        )
    except Exception as e:
        typer.echo(
            typer.style("✗ ", fg=typer.colors.RED) + f"Error saving config: {e}",
            err=True,
        )
        raise typer.Exit(1)


@llmconfig_app.command()
def show() -> None:
    """Display current LLM configuration."""
    config = ConfigManager.get_llm_config()
    if not config:
        typer.echo("No LLM configuration found.")
        return

    default_provider = config.get("default", "Not set")
    typer.echo(f"Default provider: {default_provider}")

    providers = config.get("providers", {})
    if providers:
        typer.echo("\nConfigured providers:")
        for provider in providers:
            typer.echo(f"  - {provider}")
    else:
        typer.echo("No providers configured.")
