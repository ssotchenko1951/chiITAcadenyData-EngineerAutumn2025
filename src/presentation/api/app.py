from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from src.config import get_settings
from src.application.services.dependency_injection import initialize_database
from .routes import health, pipeline, analytics, reports, frontend


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logging.basicConfig(level=logging.INFO)
    initialize_database()
    yield
    # Shutdown
    pass


def create_app() -> FastAPI:
    settings = get_settings()
    
    app = FastAPI(
        title="Data Engineering Pipeline API",
        description="A comprehensive data pipeline with clean architecture",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health.router, prefix="/health", tags=["Health"])
    app.include_router(pipeline.router, prefix="/pipeline", tags=["Pipeline"])
    app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
    app.include_router(reports.router, prefix="/reports", tags=["Reports"])
    app.include_router(frontend.router, prefix="/api", tags=["Frontend API"])
    
    return app


app = create_app()