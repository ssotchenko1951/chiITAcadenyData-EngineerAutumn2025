from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from .entities import User, Post, Comment, PipelineRun, AnalyticsReport


class UnitOfWorkInterface(ABC):
    """Interface for Unit of Work pattern"""
    
    @abstractmethod
    def __enter__(self):
        pass
    
    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    @abstractmethod
    def commit(self):
        pass
    
    @abstractmethod
    def rollback(self):
        pass
    
    @property
    @abstractmethod
    def users(self):
        pass
    
    @property
    @abstractmethod
    def posts(self):
        pass
    
    @property
    @abstractmethod
    def comments(self):
        pass
    
    @property
    @abstractmethod
    def pipeline_runs(self):
        pass


class RepositoryInterface(ABC):
    """Base interface for repositories"""
    
    @abstractmethod
    def add(self, entity):
        pass
    
    @abstractmethod
    def get(self, id):
        pass
    
    @abstractmethod
    def get_all(self):
        pass
    
    @abstractmethod
    def update(self, entity):
        pass
    
    @abstractmethod
    def delete(self, id):
        pass


class UserRepositoryInterface(RepositoryInterface):
    """Interface for User repository"""
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass


class PostRepositoryInterface(RepositoryInterface):
    """Interface for Post repository"""
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[Post]:
        pass


class CommentRepositoryInterface(RepositoryInterface):
    """Interface for Comment repository"""
    
    @abstractmethod
    def get_by_post_id(self, post_id: int) -> List[Comment]:
        pass


class PipelineRunRepositoryInterface(RepositoryInterface):
    """Interface for PipelineRun repository"""
    
    @abstractmethod
    def get_recent(self, limit: int = 10) -> List[PipelineRun]:
        pass


class DataExtractorInterface(ABC):
    """Interface for data extraction from external sources"""
    
    @abstractmethod
    async def extract_users(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def extract_posts(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def extract_comments(self) -> List[Dict[str, Any]]:
        pass


class DataProcessorInterface(ABC):
    """Interface for data processing and transformation"""
    
    @abstractmethod
    def process_users(self, raw_users: List[Dict[str, Any]]) -> List[User]:
        pass
    
    @abstractmethod
    def process_posts(self, raw_posts: List[Dict[str, Any]]) -> List[Post]:
        pass
    
    @abstractmethod
    def process_comments(self, raw_comments: List[Dict[str, Any]]) -> List[Comment]:
        pass


class FileStorageInterface(ABC):
    """Interface for file storage operations"""
    
    @abstractmethod
    def save_raw_data(self, data: Any, filename: str, date_partition: datetime) -> str:
        pass
    
    @abstractmethod
    def save_processed_data(self, data: Any, filename: str, date_partition: datetime) -> str:
        pass
    
    @abstractmethod
    def load_raw_data(self, filename: str, date_partition: datetime) -> Any:
        pass


class DatabaseInterface(ABC):
    """Interface for database operations"""
    
    @abstractmethod
    def save_users(self, users: List[User]) -> None:
        pass
    
    @abstractmethod
    def save_posts(self, posts: List[Post]) -> None:
        pass
    
    @abstractmethod
    def save_comments(self, comments: List[Comment]) -> None:
        pass
    
    @abstractmethod
    def save_pipeline_run(self, pipeline_run: PipelineRun) -> PipelineRun:
        pass
    
    @abstractmethod
    def get_analytics_data(self) -> Dict[str, Any]:
        pass


class ReportGeneratorInterface(ABC):
    """Interface for report generation"""
    
    @abstractmethod
    def generate_analytics_report(self, data: Dict[str, Any]) -> AnalyticsReport:
        pass
    
    @abstractmethod
    def export_to_csv(self, report: AnalyticsReport, filepath: str) -> None:
        pass
    
    @abstractmethod
    def export_to_json(self, report: AnalyticsReport, filepath: str) -> None:
        pass