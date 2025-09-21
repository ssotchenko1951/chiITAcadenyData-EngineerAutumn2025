import pytest
from datetime import datetime
from unittest.mock import MagicMock

from src.infrastructure.database.unit_of_work import UnitOfWork
from src.domain.entities import User, Post, Comment, PipelineRun, PipelineStatus


class TestUnitOfWork:
    """Test cases for Unit of Work pattern"""
    
    def test_unit_of_work_context_manager(self, test_db_connection):
        """Test Unit of Work as context manager"""
        with UnitOfWork(test_db_connection) as uow:
            assert uow.session is not None
            assert uow.users is not None
            assert uow.posts is not None
            assert uow.comments is not None
            assert uow.pipeline_runs is not None
    
    def test_unit_of_work_commit_success(self, test_db_connection):
        """Test successful commit"""
        user = User(
            id=1,
            name="Test User",
            username="testuser",
            email="test@example.com",
            phone="1234567890",
            website="http://test.com",
            address={},
            company={},
            created_at=datetime.utcnow()
        )
        
        with UnitOfWork(test_db_connection) as uow:
            added_user = uow.users.add(user)
            assert added_user.id == 1
            assert added_user.name == "Test User"
        
        # Verify data was committed
        with UnitOfWork(test_db_connection) as uow:
            retrieved_user = uow.users.get(1)
            assert retrieved_user is not None
            assert retrieved_user.name == "Test User"
    
    def test_unit_of_work_rollback_on_exception(self, test_db_connection):
        """Test rollback on exception"""
        user = User(
            id=1,
            name="Test User",
            username="testuser",
            email="test@example.com",
            phone="1234567890",
            website="http://test.com",
            address={},
            company={},
            created_at=datetime.utcnow()
        )
        
        try:
            with UnitOfWork(test_db_connection) as uow:
                uow.users.add(user)
                # Simulate an error
                raise Exception("Simulated error")
        except Exception:
            pass
        
        # Verify data was rolled back
        with UnitOfWork(test_db_connection) as uow:
            retrieved_user = uow.users.get(1)
            assert retrieved_user is None
    
    def test_unit_of_work_multiple_repositories(self, test_db_connection):
        """Test working with multiple repositories in one transaction"""
        user = User(
            id=1,
            name="Test User",
            username="testuser",
            email="test@example.com",
            phone="1234567890",
            website="http://test.com",
            address={},
            company={},
            created_at=datetime.utcnow()
        )
        
        post = Post(
            id=1,
            user_id=1,
            title="Test Post",
            body="This is a test post",
            created_at=datetime.utcnow()
        )
        
        comment = Comment(
            id=1,
            post_id=1,
            name="Test Comment",
            email="commenter@example.com",
            body="This is a test comment",
            created_at=datetime.utcnow()
        )
        
        with UnitOfWork(test_db_connection) as uow:
            # Add all entities in one transaction
            uow.users.add(user)
            uow.posts.add(post)
            uow.comments.add(comment)
        
        # Verify all data was committed
        with UnitOfWork(test_db_connection) as uow:
            retrieved_user = uow.users.get(1)
            retrieved_post = uow.posts.get(1)
            retrieved_comment = uow.comments.get(1)
            
            assert retrieved_user is not None
            assert retrieved_post is not None
            assert retrieved_comment is not None
            assert retrieved_post.user_id == retrieved_user.id
            assert retrieved_comment.post_id == retrieved_post.id
    
    def test_repository_lazy_initialization(self, test_db_connection):
        """Test that repositories are lazily initialized"""
        uow = UnitOfWork(test_db_connection)
        
        # Repositories should be None initially
        assert uow._users is None
        assert uow._posts is None
        assert uow._comments is None
        assert uow._pipeline_runs is None
        
        # Accessing properties should initialize repositories
        users_repo = uow.users
        assert uow._users is not None
        assert users_repo is uow.users  # Should return same instance
        
        posts_repo = uow.posts
        assert uow._posts is not None
        assert posts_repo is uow.posts