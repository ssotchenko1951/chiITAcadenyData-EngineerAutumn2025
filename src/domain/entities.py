from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class PipelineStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class User:
    id: int
    name: str
    username: str
    email: str
    phone: str
    website: str
    address: Dict[str, Any]
    company: Dict[str, Any]
    created_at: Optional[datetime] = None


@dataclass
class Post:
    id: int
    user_id: int
    title: str
    body: str
    created_at: Optional[datetime] = None


@dataclass
class Comment:
    id: int
    post_id: int
    name: str
    email: str
    body: str
    created_at: Optional[datetime] = None


@dataclass
class PipelineRun:
    id: Optional[int]
    status: PipelineStatus
    started_at: datetime
    completed_at: Optional[datetime]
    error_message: Optional[str]
    records_processed: Optional[int]
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class AnalyticsReport:
    generated_at: datetime
    total_users: int
    total_posts: int
    total_comments: int
    average_posts_per_user: float
    most_active_user: Optional[str]
    engagement_metrics: Dict[str, Any]