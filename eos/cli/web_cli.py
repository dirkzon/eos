import os
import subprocess
import sys
from pathlib import Path
from typing import Annotated

import typer

WEB_UI_DIR = Path(__file__).resolve().parents[2] / "web_ui"
IS_WINDOWS = os.name == "nt"


def _run_npm(*args: str, cwd: Path, env: dict[str, str] | None = None) -> int:
    return subprocess.call(["npm", *args], cwd=cwd, env=env, shell=IS_WINDOWS)  # noqa: S607


def start_web_ui(
    dev: Annotated[bool, typer.Option("--dev", "-d", help="Run the development server instead of production")] = False,
    build: Annotated[
        bool, typer.Option("--build", "-b", help="Force a rebuild even if a build already exists")
    ] = False,
    host: Annotated[str, typer.Option("--host", "-H", help="Host to bind to (default: 127.0.0.1)")] = "127.0.0.1",
) -> None:
    """Start the EOS web UI."""
    if not WEB_UI_DIR.is_dir():
        typer.echo(f"Error: web UI directory not found at {WEB_UI_DIR}", err=True)
        raise typer.Exit(1)

    if not (WEB_UI_DIR / "node_modules").is_dir():
        typer.echo("Error: node_modules not found. Run 'npm install' in the web_ui/ directory first.", err=True)
        raise typer.Exit(1)

    env = {**os.environ, "HOST": host}

    try:
        if dev:
            typer.echo("Starting web UI in development mode...")
            sys.exit(_run_npm("run", "dev", cwd=WEB_UI_DIR, env=env))
        else:
            needs_build = build or not (WEB_UI_DIR / ".next").is_dir()
            if needs_build:
                typer.echo("Building web UI...")
                result = _run_npm("run", "build", cwd=WEB_UI_DIR)
                if result != 0:
                    typer.echo("Error: build failed.", err=True)
                    raise typer.Exit(result)

            typer.echo("Starting web UI...")
            sys.exit(_run_npm("start", cwd=WEB_UI_DIR, env=env))
    except FileNotFoundError:
        typer.echo("Error: npm not found on PATH.", err=True)
        raise typer.Exit(1) from None
