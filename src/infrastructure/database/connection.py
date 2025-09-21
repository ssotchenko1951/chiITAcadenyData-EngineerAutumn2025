from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from typing import Generator

from src.config import get_settings

Base = declarative_base()


class DatabaseConnection:
    def __init__(self):
        self.settings = get_settings()
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine
        )

    def _create_engine(self) -> Engine:
        database_url = self.settings.database.get_url()
        
        if database_url.startswith("sqlite"):
            engine = create_engine(
                database_url,
                connect_args={"check_same_thread": False}
            )
        else:
            engine = create_engine(
                database_url,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True
            )
        
        return engine

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(bind=self.engine)