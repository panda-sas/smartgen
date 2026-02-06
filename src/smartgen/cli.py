"""Main CLI entry point for smartgen."""
import typer

from smartgen.commands.llmconfig import llmconfig_app

app = typer.Typer()
app.add_typer(llmconfig_app, name="llmconfig")


def main() -> None:
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()