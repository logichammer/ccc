"""
{{PROJECT_NAME}} - A {{PROJECT_TYPE}} project
Created: {{DATE}}

Main entry point for the application.
"""

import logging
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.logging import RichHandler

# Set up logging with Rich
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger(__name__)
console = Console()


def setup_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.getLogger().setLevel(level)


@click.command()
@click.option(
    "--verbose", "-v", 
    is_flag=True, 
    help="Enable verbose logging"
)
@click.option(
    "--config", "-c",
    type=click.Path(exists=True),
    help="Path to configuration file"
)
def main(verbose: bool, config: Optional[str]) -> None:
    """
    {{PROJECT_NAME}} - A {{PROJECT_TYPE}} application.
    
    This is the main entry point for your application.
    Customize this function to implement your specific functionality.
    """
    setup_logging(verbose)
    
    console.print(f"[bold green]🚀 Starting {{PROJECT_NAME}}[/bold green]")
    
    if config:
        console.print(f"[yellow]📄 Using config file: {config}[/yellow]")
    
    # Your application logic goes here
    console.print("[blue]✨ Application initialized successfully![/blue]")
    
    # Example: Basic functionality template
    try:
        # Add your main application logic here
        console.print("[green]🎯 Running main application logic...[/green]")
        
        # Placeholder for actual functionality
        result = run_application()
        
        if result:
            console.print("[green]✅ Application completed successfully![/green]")
        else:
            console.print("[red]❌ Application encountered an error[/red]")
            
    except Exception as e:
        logger.error(f"Application error: {e}")
        console.print(f"[red]💥 Error: {e}[/red]")
        raise click.Abort()


def run_application() -> bool:
    """
    Main application logic.
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Implement your application logic here
    logger.info("Application logic executed")
    return True


if __name__ == "__main__":
    main()