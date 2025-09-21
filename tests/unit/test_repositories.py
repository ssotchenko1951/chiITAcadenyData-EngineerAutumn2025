import pytest
from datetime import datetime

from src.infrastructure.database.repositories import UserRepository, PostRepository, CommentRepository
from src.domain.entities import User, Post, Comment


class TestRepositories:
    """Test cases for repository implementations"""
    
    def test_user_repository_crud(self, test_db_connection):
        """Test User repository CRUD operations"""
        with test_db_connection.get_session() as session:
            repo = UserRepository(session)
            
            # Create user
            user = User(
                id=1,
                name="John Doe",
                username="johndoe",
                email="john@example.com",
                phone="1234567890",
                website="http://johndoe.com",
                address={"city": "New York"},
                company={"name": "Acme Corp"},
                created_at=datetime.utcnow()
            )
            
            # Add user
            added_user = repo.add(user)
            assert added_user.id == 1
            assert added_user.name == "John Doe"
            
            # Get user
            retrieved_user = repo.get(1)
            assert retrieved_user is not None
            assert retrieved_user.name == "John Doe"
            assert retrieved_user.email == "john@example.com"
            
            # Get by email
            user_by_email = repo.get_by_email("john@example.com")
            assert user_by_email is not None
            assert user_by_email.id == 1
            
            # Get by username
            user_by_username = repo.get_by_username("johndoe")
            assert user_by_username is not None
            assert user_by_username.id == 1
            
            # Update user
            retrieved_user.name = "John Smith"
            updated_user = repo.update(retrieved_user)
            assert updated_user.name == "John Smith"
            
            # Get all users
            all_users = repo.get_all()
            assert len(all_users) == 1
            assert all_users[0].name == "John Smith"
            
            # Delete user
            deleted = repo.delete(1)
            assert deleted is True
            
            # Verify deletion
            deleted_user = repo.get(1)
            assert deleted_user is None
    
    def test_post_repository_crud(self, test_db_connection):
        """Test Post repository CRUD operations"""
        with test_db_connection.get_session() as session:
            user_repo = UserRepository(session)
            post_repo = PostRepository(session)
            
            # First create a user
            user = User(
                id=1,
                name="John Doe",
                username="johndoe",
                email="john@example.com",
                phone="1234567890",
                website="http://johndoe.com",
                address={},
                company={},
                created_at=datetime.utcnow()
            )
            user_repo.add(user)
            
            # Create post
            post = Post(
                id=1,
                user_id=1,
                title="Test Post",
                body="This is a test post content",
                created_at=datetime.utcnow()
            )
            
            # Add post
            added_post = post_repo.add(post)
            assert added_post.id == 1
            assert added_post.title == "Test Post"
            
            # Get post
            retrieved_post = post_repo.get(1)
            assert retrieved_post is not None
            assert retrieved_post.title == "Test Post"
            assert retrieved_post.user_id == 1
            
            # Get posts by user ID
            user_posts = post_repo.get_by_user_id(1)
            assert len(user_posts) == 1
            assert user_posts[0].title == "Test Post"
            
            # Update post
            retrieved_post.title = "Updated Post Title"
            updated_post = post_repo.update(retrieved_post)
            assert updated_post.title == "Updated Post Title"
    
    def test_comment_repository_crud(self, test_db_connection):
        """Test Comment repository CRUD operations"""
        with test_db_connection.get_session() as session:
            user_repo = UserRepository(session)
            post_repo = PostRepository(session)
            comment_repo = CommentRepository(session)
            
            # Create user and post first
            user = User(
                id=1,
                name="John Doe",
                username="johndoe",
                email="john@example.com",
                phone="1234567890",
                website="http://johndoe.com",
                address={},
                company={},
                created_at=datetime.utcnow()
            )
            user_repo.add(user)
            
            post = Post(
                id=1,
                user_id=1,
                title="Test Post",
                body="This is a test post",
                created_at=datetime.utcnow()
            )
            post_repo.add(post)
            
            # Create comment
            comment = Comment(
                id=1,
                post_id=1,
                name="Great post!",
                email="commenter@example.com",
                body="This is a great post, thanks for sharing!",
                created_at=datetime.utcnow()
            )
            
            # Add comment
            added_comment = comment_repo.add(comment)
            assert added_comment.id == 1
            assert added_comment.name == "Great post!"
            
            # Get comment
            retrieved_comment = comment_repo.get(1)
            assert retrieved_comment is not None
            assert retrieved_comment.name == "Great post!"
            assert retrieved_comment.post_id == 1
            
            # Get comments by post ID
            post_comments = comment_repo.get_by_post_id(1)
            assert len(post_comments) == 1
            assert post_comments[0].name == "Great post!"
            
            # Update comment
            retrieved_comment.body = "Updated comment body"
            updated_comment = comment_repo.update(retrieved_comment)
            assert updated_comment.body == "Updated comment body"