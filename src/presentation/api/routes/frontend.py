from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from src.application.services.dependency_injection import get_unit_of_work

router = APIRouter()


@router.get("/users")
async def get_users():
    """Get all users for frontend"""
    with get_unit_of_work() as uow:
        users = uow.users.get_all()
        return {
            "users": [
                {
                    "id": user.id,
                    "name": user.name,
                    "username": user.username,
                    "email": user.email,
                    "phone": user.phone,
                    "website": user.website,
                    "address": user.address,
                    "company": user.company,
                    "created_at": user.created_at.isoformat() if user.created_at else None
                }
                for user in users
            ]
        }


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get specific user by ID"""
    with get_unit_of_work() as uow:
        user = uow.users.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "website": user.website,
            "address": user.address,
            "company": user.company,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }


@router.get("/posts")
async def get_posts():
    """Get all posts for frontend"""
    with get_unit_of_work() as uow:
        posts = uow.posts.get_all()
        return {
            "posts": [
                {
                    "id": post.id,
                    "user_id": post.user_id,
                    "title": post.title,
                    "body": post.body,
                    "created_at": post.created_at.isoformat() if post.created_at else None
                }
                for post in posts
            ]
        }


@router.get("/posts/{post_id}")
async def get_post(post_id: int):
    """Get specific post by ID"""
    with get_unit_of_work() as uow:
        post = uow.posts.get(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        return {
            "id": post.id,
            "user_id": post.user_id,
            "title": post.title,
            "body": post.body,
            "created_at": post.created_at.isoformat() if post.created_at else None
        }


@router.get("/posts/{post_id}/comments")
async def get_post_comments(post_id: int):
    """Get comments for a specific post"""
    with get_unit_of_work() as uow:
        # Verify post exists
        post = uow.posts.get(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        comments = uow.comments.get_by_post_id(post_id)
        return {
            "comments": [
                {
                    "id": comment.id,
                    "post_id": comment.post_id,
                    "name": comment.name,
                    "email": comment.email,
                    "body": comment.body,
                    "created_at": comment.created_at.isoformat() if comment.created_at else None
                }
                for comment in comments
            ]
        }


@router.get("/users/{user_id}/posts")
async def get_user_posts(user_id: int):
    """Get posts by a specific user"""
    with get_unit_of_work() as uow:
        # Verify user exists
        user = uow.users.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        posts = uow.posts.get_by_user_id(user_id)
        return {
            "posts": [
                {
                    "id": post.id,
                    "user_id": post.user_id,
                    "title": post.title,
                    "body": post.body,
                    "created_at": post.created_at.isoformat() if post.created_at else None
                }
                for post in posts
            ]
        }


@router.get("/comments")
async def get_comments():
    """Get all comments for frontend"""
    with get_unit_of_work() as uow:
        comments = uow.comments.get_all()
        return {
            "comments": [
                {
                    "id": comment.id,
                    "post_id": comment.post_id,
                    "name": comment.name,
                    "email": comment.email,
                    "body": comment.body,
                    "created_at": comment.created_at.isoformat() if comment.created_at else None
                }
                for comment in comments
            ]
        }


@router.get("/dashboard/stats")
async def get_dashboard_stats():
    """Get dashboard statistics for frontend"""
    with get_unit_of_work() as uow:
        users = uow.users.get_all()
        posts = uow.posts.get_all()
        comments = uow.comments.get_all()
        recent_runs = uow.pipeline_runs.get_recent(5)
        
        return {
            "total_users": len(users),
            "total_posts": len(posts),
            "total_comments": len(comments),
            "recent_pipeline_runs": [
                {
                    "id": run.id,
                    "status": run.status.value if hasattr(run.status, 'value') else run.status,
                    "started_at": run.started_at.isoformat() if run.started_at else None,
                    "completed_at": run.completed_at.isoformat() if run.completed_at else None,
                    "records_processed": run.records_processed
                }
                for run in recent_runs
            ]
        }