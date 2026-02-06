"""Main CLI entry point for smartgen."""
import typer

from smartgen.commands.init import init_command
from smartgen.commands.llmconfig import llmconfig_app
from smartgen.commands.generate import generate_app

app = typer.Typer()
app.add_typer(llmconfig_app, name="llmconfig")
app.add_typer(generate_app, name="generate")
app.command("init")(init_command)


def main() -> None:
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()