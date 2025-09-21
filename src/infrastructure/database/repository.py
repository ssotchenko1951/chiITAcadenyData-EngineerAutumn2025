from typing import List, Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.domain.entities import User, Post, Comment, PipelineRun
from src.domain.interfaces import DatabaseInterface
from .connection import DatabaseConnection
from .models import UserModel, PostModel, CommentModel, PipelineRunModel


class DatabaseRepository(DatabaseInterface):
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection

    def save_users(self, users: List[User]) -> None:
        with self.db.get_session() as session:
            for user in users:
                # Check if user exists
                existing = session.query(UserModel).filter(UserModel.id == user.id).first()
                if existing:
                    # Update existing user
                    existing.name = user.name
                    existing.username = user.username
                    existing.email = user.email
                    existing.phone = user.phone
                    existing.website = user.website
                    existing.address = user.address
                    existing.company = user.company
                else:
                    # Create new user
                    user_model = UserModel(
                        id=user.id,
                        name=user.name,
                        username=user.username,
                        email=user.email,
                        phone=user.phone,
                        website=user.website,
                        address=user.address,
                        company=user.company
                    )
                    session.add(user_model)

    def save_posts(self, posts: List[Post]) -> None:
        with self.db.get_session() as session:
            for post in posts:
                existing = session.query(PostModel).filter(PostModel.id == post.id).first()
                if existing:
                    existing.title = post.title
                    existing.body = post.body
                else:
                    post_model = PostModel(
                        id=post.id,
                        user_id=post.user_id,
                        title=post.title,
                        body=post.body
                    )
                    session.add(post_model)

    def save_comments(self, comments: List[Comment]) -> None:
        with self.db.get_session() as session:
            for comment in comments:
                existing = session.query(CommentModel).filter(CommentModel.id == comment.id).first()
                if existing:
                    existing.name = comment.name
                    existing.email = comment.email
                    existing.body = comment.body
                else:
                    comment_model = CommentModel(
                        id=comment.id,
                        post_id=comment.post_id,
                        name=comment.name,
                        email=comment.email,
                        body=comment.body
                    )
                    session.add(comment_model)

    def save_pipeline_run(self, pipeline_run: PipelineRun) -> PipelineRun:
        with self.db.get_session() as session:
            if pipeline_run.id:
                # Update existing run
                existing = session.query(PipelineRunModel).filter(
                    PipelineRunModel.id == pipeline_run.id
                ).first()
                if existing:
                    existing.status = pipeline_run.status.value
                    existing.completed_at = pipeline_run.completed_at
                    existing.error_message = pipeline_run.error_message
                    existing.records_processed = pipeline_run.records_processed
                    existing.metadata = pipeline_run.metadata
                    session.flush()
                    pipeline_run.id = existing.id
            else:
                # Create new run
                run_model = PipelineRunModel(
                    status=pipeline_run.status.value,
                    started_at=pipeline_run.started_at,
                    completed_at=pipeline_run.completed_at,
                    error_message=pipeline_run.error_message,
                    records_processed=pipeline_run.records_processed,
                    metadata=pipeline_run.metadata
                )
                session.add(run_model)
                session.flush()
                pipeline_run.id = run_model.id
        
        return pipeline_run

    def get_analytics_data(self) -> Dict[str, Any]:
        with self.db.get_session() as session:
            # Total counts
            total_users = session.query(UserModel).count()
            total_posts = session.query(PostModel).count()
            total_comments = session.query(CommentModel).count()

            # Average posts per user
            avg_posts_query = text("""
                SELECT AVG(post_count) as avg_posts
                FROM (
                    SELECT user_id, COUNT(*) as post_count
                    FROM posts
                    GROUP BY user_id
                ) user_posts
            """)
            avg_posts_result = session.execute(avg_posts_query).fetchone()
            avg_posts_per_user = float(avg_posts_result[0]) if avg_posts_result[0] else 0.0

            # Most active user by posts
            most_active_user_query = text("""
                SELECT u.name, COUNT(p.id) as post_count
                FROM users u
                LEFT JOIN posts p ON u.id = p.user_id
                GROUP BY u.id, u.name
                ORDER BY post_count DESC
                LIMIT 1
            """)
            most_active_result = session.execute(most_active_user_query).fetchone()
            most_active_user = most_active_result[0] if most_active_result else None

            # Engagement metrics
            engagement_query = text("""
                SELECT 
                    p.title,
                    COUNT(c.id) as comment_count,
                    u.name as author
                FROM posts p
                LEFT JOIN comments c ON p.id = c.post_id
                LEFT JOIN users u ON p.user_id = u.id
                GROUP BY p.id, p.title, u.name
                ORDER BY comment_count DESC
                LIMIT 10
            """)
            engagement_results = session.execute(engagement_query).fetchall()
            top_posts = [
                {
                    "title": row[0],
                    "comment_count": row[1],
                    "author": row[2]
                }
                for row in engagement_results
            ]

            return {
                "total_users": total_users,
                "total_posts": total_posts,
                "total_comments": total_comments,
                "average_posts_per_user": avg_posts_per_user,
                "most_active_user": most_active_user,
                "top_posts_by_engagement": top_posts
            }

    def get_pipeline_runs(self, limit: int = 10) -> List[PipelineRun]:
        with self.db.get_session() as session:
            runs = session.query(PipelineRunModel)\
                         .order_by(PipelineRunModel.started_at.desc())\
                         .limit(limit)\
                         .all()
            
            return [
                PipelineRun(
                    id=run.id,
                    status=run.status,
                    started_at=run.started_at,
                    completed_at=run.completed_at,
                    error_message=run.error_message,
                    records_processed=run.records_processed,
                    metadata=run.metadata
                )
                for run in runs
            ]