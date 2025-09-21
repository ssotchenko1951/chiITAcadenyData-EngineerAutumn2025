from typing import Optional
from sqlalchemy.orm import Session
from contextlib import contextmanager

from src.domain.interfaces import UnitOfWorkInterface
from .connection import DatabaseConnection
from .repositories import (
    UserRepository, 
    PostRepository, 
    CommentRepository, 
    PipelineRunRepository
)


class UnitOfWork(UnitOfWorkInterface):
    """
    Unit of Work implementation for managing database transactions.
    
    This pattern ensures that all repository operations within a single
    business transaction are committed or rolled back together, maintaining
    data consistency and ACID properties.
    
    Benefits:
    - Atomic transactions across multiple repositories
    - Automatic session management
    - Consistent error handling and rollback
    - Reduced database connections
    - Clear transaction boundaries
    """
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection
        self.session: Optional[Session] = None
        self._users: Optional[UserRepository] = None
        self._posts: Optional[PostRepository] = None
        self._comments: Optional[CommentRepository] = None
        self._pipeline_runs: Optional[PipelineRunRepository] = None
    
    def __enter__(self):
        """Enter the runtime context for the Unit of Work"""
        self.session = self.db_connection.SessionLocal()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the runtime context, handling cleanup"""
        if exc_type is not None:
            self.rollback()
        else:
            try:
                self.commit()
            except Exception:
                self.rollback()
                raise
        finally:
            if self.session:
                self.session.close()
    
    def commit(self):
        """Commit the current transaction"""
        if self.session:
            self.session.commit()
    
    def rollback(self):
        """Rollback the current transaction"""
        if self.session:
            self.session.rollback()
    
    @property
    def users(self) -> UserRepository:
        """Get the User repository"""
        if self._users is None:
            self._users = UserRepository(self.session)
        return self._users
    
    @property
    def posts(self) -> PostRepository:
        """Get the Post repository"""
        if self._posts is None:
            self._posts = PostRepository(self.session)
        return self._posts
    
    @property
    def comments(self) -> CommentRepository:
        """Get the Comment repository"""
        if self._comments is None:
            self._comments = CommentRepository(self.session)
        return self._comments
    
    @property
    def pipeline_runs(self) -> PipelineRunRepository:
        """Get the PipelineRun repository"""
        if self._pipeline_runs is None:
            self._pipeline_runs = PipelineRunRepository(self.session)
        return self._pipeline_runs


@contextmanager
def get_unit_of_work(db_connection: DatabaseConnection):
    """Context manager for Unit of Work"""
    uow = UnitOfWork(db_connection)
    try:
        with uow:
            yield uow
    except Exception:
        raise