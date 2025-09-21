from functools import lru_cache

from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.database.repository import DatabaseRepository
from src.infrastructure.database.unit_of_work import UnitOfWork
from src.infrastructure.database.mock_data import seed_mock_data
from src.infrastructure.api.client import APIClient
from src.infrastructure.storage.file_storage import FileStorage
from src.infrastructure.reporting.report_generator import ReportGenerator
from src.application.services.data_processor import DataProcessor
from src.application.use_cases.pipeline_orchestrator import PipelineOrchestrator


@lru_cache()
def get_database_connection():
    return DatabaseConnection()


@lru_cache()
def get_unit_of_work():
    db_connection = get_database_connection()
    return UnitOfWork(db_connection)
@lru_cache()
def get_database_repository():
    db_connection = get_database_connection()
    return DatabaseRepository(db_connection)


@lru_cache()
def get_api_client():
    return APIClient()


@lru_cache()
def get_file_storage():
    return FileStorage()


@lru_cache()
def get_data_processor():
    return DataProcessor()


@lru_cache()
def get_report_generator():
    return ReportGenerator()


@lru_cache()
def get_pipeline_orchestrator():
    return PipelineOrchestrator(
        api_client=get_api_client(),
        data_processor=get_data_processor(),
        file_storage=get_file_storage(),
        database=get_database_repository(),
        report_generator=get_report_generator()
    )


def initialize_database():
    """Initialize database tables"""
    db_connection = get_database_connection()
    db_connection.create_tables()
    
    # Seed mock data for frontend development
    try:
        seed_mock_data(db_connection)
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to seed mock data: {e}")