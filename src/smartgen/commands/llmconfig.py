"""LLM configuration command."""
import typer
from typing import Optional

from smartgen.config import ConfigManager

llmconfig_app = typer.Typer(help="Configure LLM settings")


@llmconfig_app.command()
def set_config(
    default: Optional[str] = typer.Option(
        None, help="Default LLM provider (e.g., openai, anthropic)"
    ),
    api_key: Optional[str] = typer.Option(
        None, help="API key for cloud provider"
    ),
    add: Optional[str] = typer.Option(
        None, help="Add a provider (cloud or local name)"
    ),
    model: Optional[str] = typer.Option(
        None, help="Model name (for local LLMs, default: deepseek-coder-v2)"
    ),
    url: Optional[str] = typer.Option(
        None, help="URL (for local LLMs, default: http://localhost:11434)"
    ),
) -> None:
    """
    Save LLM configuration.
    
    Examples:
        # Cloud provider
        smartgen llmconfig set-config --default=openai --api-key <key>
        
        # Local LLM (Ollama)
        smartgen llmconfig set-config --add ollama --model qwen --url http://localhost:11434
        smartgen llmconfig set-config --add ollama  # Uses defaults
    """
    try:
        if add:
            # Determine if it's cloud or local based on common names
            provider_type = "local" if add.lower() in ["ollama", "lm-studio", "local"] else "cloud"
            ConfigManager.add_provider(
                name=add,
                provider_type=provider_type,
                api_key=api_key,
                model=model,
                url=url,
            )
            typer.echo(
                typer.style("✓ ", fg=typer.colors.GREEN)
                + f"Provider '{add}' saved (type: {provider_type})"
            )
        elif default and api_key:
            # Legacy cloud provider setup
            ConfigManager.add_provider(
                name=default,
                provider_type="cloud",
                api_key=api_key,
            )
            typer.echo(
                typer.style("✓ ", fg=typer.colors.GREEN)
                + f"LLM config saved: provider={default}"
            )
        else:
            typer.echo(
                typer.style("✗ ", fg=typer.colors.RED)
                + "Please provide either --add or (--default + --api-key)",
                err=True,
            )
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(
            typer.style("✗ ", fg=typer.colors.RED) + f"Error saving config: {e}",
            err=True,
        )
        raise typer.Exit(1)


@llmconfig_app.command()
def set_default(
    provider: str = typer.Argument(..., help="Provider name to set as default")
) -> None:
    """Set the default LLM provider."""
    try:
        ConfigManager.set_default_provider(provider)
        typer.echo(
            typer.style("✓ ", fg=typer.colors.GREEN)
            + f"Default provider set to: {provider}"
        )
    except ValueError as e:
        typer.echo(
            typer.style("✗ ", fg=typer.colors.RED) + f"Error: {e}",
            err=True,
        )
        raise typer.Exit(1)


@llmconfig_app.command()
def remove(
    provider: str = typer.Argument(..., help="Provider name to remove")
) -> None:
    """Remove an LLM provider configuration."""
    try:
        ConfigManager.remove_provider(provider)
        typer.echo(
            typer.style("✓ ", fg=typer.colors.GREEN)
            + f"Provider '{provider}' removed"
        )
    except ValueError as e:
        typer.echo(
            typer.style("✗ ", fg=typer.colors.RED) + f"Error: {e}",
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
    typer.echo(f"Default provider: {typer.style(default_provider, bold=True)}")

    providers = config.get("providers", {})
    if providers:
        typer.echo("\nConfigured providers:")
        for provider_name, provider_config in providers.items():
            provider_type = provider_config.get("type", "unknown")
            model = provider_config.get("model", "N/A")
            url = provider_config.get("url", "N/A")
            has_key = "api_key" in provider_config

            typer.echo(f"  {provider_name}:")
            typer.echo(f"    Type: {provider_type}")
            typer.echo(f"    Model: {model}")
            if provider_type == "local":
                typer.echo(f"    URL: {url}")
            if has_key:
                typer.echo(f"    API Key: {'*' * 8} (set)")
    else:
        typer.echo("No providers configured.")

