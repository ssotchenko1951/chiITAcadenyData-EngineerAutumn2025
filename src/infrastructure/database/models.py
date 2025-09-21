from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from .connection import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(50))
    website = Column(String(100))
    address = Column(JSON)
    company = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    posts = relationship("PostModel", back_populates="user", cascade="all, delete-orphan")


class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("UserModel", back_populates="posts")
    comments = relationship("CommentModel", back_populates="post", cascade="all, delete-orphan")


class CommentModel(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("PostModel", back_populates="comments")


class PipelineRunModel(Base):
    __tablename__ = "pipeline_runs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(String(20), nullable=False)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    records_processed = Column(Integer)
    metadata = Column(JSON)