import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import tempfile
import os

from src.infrastructure.database.connection import Base
from src.infrastructure.database.repository import DatabaseRepository
from src.infrastructure.database.connection import DatabaseConnection
from src.application.services.data_processor import DataProcessor
from src.infrastructure.storage.file_storage import FileStorage


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_db_connection():
    """Create a test database connection"""
    # Use in-memory SQLite for testing
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    class TestDatabaseConnection:
        def __init__(self):
            self.engine = engine
            self.SessionLocal = SessionLocal
        
        def get_session(self):
            from contextlib import contextmanager
            @contextmanager
            def _get_session():
                session = self.SessionLocal()
                try:
                    yield session
                    session.commit()
                except Exception:
                    session.rollback()
                    raise
                finally:
                    session.close()
            return _get_session()
    
    return TestDatabaseConnection()


@pytest.fixture
def test_database_repository(test_db_connection):
    """Create a test database repository"""
    return DatabaseRepository(test_db_connection)


@pytest.fixture
def data_processor():
    """Create a data processor instance"""
    return DataProcessor()


@pytest.fixture
def temp_file_storage():
    """Create a temporary file storage instance"""
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ["DATA_DIR"] = temp_dir
        os.environ["REPORTS_DIR"] = os.path.join(temp_dir, "reports")
        yield FileStorage()


@pytest.fixture
def sample_users_data():
    """Sample users data for testing"""
    return [
        {
            "id": 1,
            "name": "John Doe",
            "username": "johndoe",
            "email": "john@example.com",
            "phone": "123-456-7890",
            "website": "johndoe.com",
            "address": {
                "street": "123 Main St",
                "suite": "Apt 1",
                "city": "Anytown",
                "zipcode": "12345",
                "geo": {"lat": "40.7128", "lng": "-74.0060"}
            },
            "company": {
                "name": "Doe Industries",
                "catchPhrase": "Making things happen",
                "bs": "synergistic solutions"
            }
        }
    ]


@pytest.fixture
def sample_posts_data():
    """Sample posts data for testing"""
    return [
        {
            "id": 1,
            "userId": 1,
            "title": "Sample Post",
            "body": "This is a sample post content."
        }
    ]


@pytest.fixture
def sample_comments_data():
    """Sample comments data for testing"""
    return [
        {
            "id": 1,
            "postId": 1,
            "name": "Great post!",
            "email": "commenter@example.com",
            "body": "I really enjoyed reading this post."
        }
    ]