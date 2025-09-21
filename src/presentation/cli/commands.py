import click
import asyncio
import uvicorn
from rich.console import Console
from rich.progress import track
import logging

from src.config import get_settings
from src.application.services.dependency_injection import (
    get_pipeline_orchestrator, 
    initialize_database
)

console = Console()
logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Data Pipeline CLI"""
    logging.basicConfig(level=logging.INFO)


@cli.group()
def db():
    """Database commands"""
    pass


@db.command()
def migrate():
    """Initialize/migrate database"""
    console.print("Initializing database...", style="blue")
    try:
        initialize_database()
        console.print("✅ Database initialized successfully", style="green")
    except Exception as e:
        console.print(f"❌ Database initialization failed: {e}", style="red")


@cli.group()
def pipeline():
    """Pipeline commands"""
    pass


@pipeline.command()
def run():
    """Run the data pipeline"""
    console.print("Starting data pipeline...", style="blue")
    
    async def run_pipeline():
        orchestrator = get_pipeline_orchestrator()
        try:
            result = await orchestrator.run_full_pipeline()
            console.print("✅ Pipeline completed successfully", style="green")
            console.print(f"📊 Records processed: {result['pipeline_run'].records_processed}")
            return result
        except Exception as e:
            console.print(f"❌ Pipeline failed: {e}", style="red")
            raise
    
    asyncio.run(run_pipeline())


@cli.group()
def api():
    """API server commands"""
    pass


@api.command()
@click.option('--host', default='0.0.0.0', help='Host to bind')
@click.option('--port', default=8000, help='Port to bind')
@click.option('--reload', is_flag=True, help='Enable auto-reload')
def start(host: str, port: int, reload: bool):
    """Start the API server"""
    console.print(f"Starting API server on {host}:{port}", style="blue")
    
    uvicorn.run(
        "src.presentation.api.app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


@cli.command()
def status():
    """Show system status"""
    console.print("📊 System Status", style="bold blue")
    
    settings = get_settings()
    console.print(f"Environment: {settings.environment}")
    console.print(f"Database: {settings.database.type}")
    console.print(f"Data directory: {settings.data_dir}")
    console.print(f"Reports directory: {settings.reports_dir}")


if __name__ == "__main__":
    cli()