import pytest
from datetime import datetime

from src.domain.entities import User, Post, Comment, PipelineRun, PipelineStatus


class TestDatabaseRepository:
    
    def test_save_and_retrieve_users(self, test_database_repository, sample_users_data, data_processor):
        """Test saving and retrieving users"""
        # Process the sample data
        users = data_processor.process_users(sample_users_data)
        
        # Save users
        test_database_repository.save_users(users)
        
        # Get analytics data to verify users were saved
        analytics = test_database_repository.get_analytics_data()
        assert analytics["total_users"] == 1
    
    def test_save_pipeline_run(self, test_database_repository):
        """Test saving pipeline run"""
        pipeline_run = PipelineRun(
            id=None,
            status=PipelineStatus.RUNNING,
            started_at=datetime.utcnow(),
            completed_at=None,
            error_message=None,
            records_processed=None
        )
        
        # Save pipeline run
        saved_run = test_database_repository.save_pipeline_run(pipeline_run)
        
        assert saved_run.id is not None
        assert saved_run.status == PipelineStatus.RUNNING
        
        # Update the run
        saved_run.status = PipelineStatus.SUCCESS
        saved_run.completed_at = datetime.utcnow()
        saved_run.records_processed = 100
        
        updated_run = test_database_repository.save_pipeline_run(saved_run)
        
        assert updated_run.status == PipelineStatus.SUCCESS
        assert updated_run.completed_at is not None
        assert updated_run.records_processed == 100
    
    def test_get_analytics_data_empty_database(self, test_database_repository):
        """Test analytics with empty database"""
        analytics = test_database_repository.get_analytics_data()
        
        assert analytics["total_users"] == 0
        assert analytics["total_posts"] == 0
        assert analytics["total_comments"] == 0
        assert analytics["average_posts_per_user"] == 0.0
        assert analytics["most_active_user"] is None
        assert analytics["top_posts_by_engagement"] == []
    
    def test_full_data_flow(self, test_database_repository, data_processor, 
                           sample_users_data, sample_posts_data, sample_comments_data):
        """Test complete data flow"""
        # Process all data
        users = data_processor.process_users(sample_users_data)
        posts = data_processor.process_posts(sample_posts_data)
        comments = data_processor.process_comments(sample_comments_data)
        
        # Save all data
        test_database_repository.save_users(users)
        test_database_repository.save_posts(posts)
        test_database_repository.save_comments(comments)
        
        # Get analytics
        analytics = test_database_repository.get_analytics_data()
        
        assert analytics["total_users"] == 1
        assert analytics["total_posts"] == 1
        assert analytics["total_comments"] == 1
        assert analytics["average_posts_per_user"] == 1.0
        assert analytics["most_active_user"] == "John Doe"
        assert len(analytics["top_posts_by_engagement"]) == 1