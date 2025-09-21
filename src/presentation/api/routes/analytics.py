from fastapi import APIRouter

from src.application.services.dependency_injection import get_database_repository

router = APIRouter()


@router.get("/summary")
async def get_analytics_summary():
    """Get analytics summary"""
    database = get_database_repository()
    analytics_data = database.get_analytics_data()
    
    return analytics_data


@router.get("/users/stats")
async def get_user_statistics():
    """Get user-specific statistics"""
    database = get_database_repository()
    analytics_data = database.get_analytics_data()
    
    return {
        "total_users": analytics_data.get("total_users", 0),
        "average_posts_per_user": analytics_data.get("average_posts_per_user", 0.0),
        "most_active_user": analytics_data.get("most_active_user")
    }


@router.get("/engagement")
async def get_engagement_metrics():
    """Get engagement metrics"""
    database = get_database_repository()
    analytics_data = database.get_analytics_data()
    
    return {
        "total_posts": analytics_data.get("total_posts", 0),
        "total_comments": analytics_data.get("total_comments", 0),
        "top_posts": analytics_data.get("top_posts_by_engagement", [])
    }