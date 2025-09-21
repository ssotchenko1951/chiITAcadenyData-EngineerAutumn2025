import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock

from src.application.use_cases.pipeline_orchestrator import PipelineOrchestrator
from src.domain.entities import PipelineStatus


@pytest.mark.asyncio
class TestPipelineFlow:
    """End-to-end tests for the complete pipeline flow"""
    
    async def test_full_pipeline_success(self):
        """Test complete pipeline execution"""
        # Mock dependencies
        mock_api_client = AsyncMock()
        mock_data_processor = MagicMock()
        mock_file_storage = MagicMock()
        mock_database = MagicMock()
        mock_report_generator = MagicMock()
        
        # Setup mock data
        mock_raw_data = {
            "users": [{"id": 1, "name": "Test User", "email": "test@example.com"}],
            "posts": [{"id": 1, "userId": 1, "title": "Test Post", "body": "Content"}],
            "comments": [{"id": 1, "postId": 1, "name": "Test", "email": "test@example.com", "body": "Comment"}]
        }
        
        mock_api_client.extract_all_data.return_value = mock_raw_data
        
        # Mock processed data
        from src.domain.entities import User, Post, Comment
        from datetime import datetime
        
        mock_user = User(
            id=1, name="Test User", username="testuser", email="test@example.com",
            phone="123456789", website="http://test.com", address={}, company={},
            created_at=datetime.utcnow()
        )
        mock_post = Post(
            id=1, user_id=1, title="Test Post", body="Content",
            created_at=datetime.utcnow()
        )
        mock_comment = Comment(
            id=1, post_id=1, name="Test", email="test@example.com", body="Comment",
            created_at=datetime.utcnow()
        )
        
        mock_data_processor.process_users.return_value = [mock_user]
        mock_data_processor.process_posts.return_value = [mock_post]
        mock_data_processor.process_comments.return_value = [mock_comment]
        
        # Mock analytics
        mock_analytics_data = {
            "total_users": 1,
            "total_posts": 1,
            "total_comments": 1,
            "average_posts_per_user": 1.0,
            "most_active_user": "Test User",
            "top_posts_by_engagement": []
        }
        mock_database.get_analytics_data.return_value = mock_analytics_data
        
        from src.domain.entities import AnalyticsReport
        mock_report = AnalyticsReport(
            generated_at=datetime.utcnow(),
            total_users=1,
            total_posts=1,
            total_comments=1,
            average_posts_per_user=1.0,
            most_active_user="Test User",
            engagement_metrics=[]
        )
        mock_report_generator.generate_analytics_report.return_value = mock_report
        
        # Mock pipeline run creation and updates
        from src.domain.entities import PipelineRun
        mock_pipeline_run = PipelineRun(
            id=1,
            status=PipelineStatus.RUNNING,
            started_at=datetime.utcnow(),
            completed_at=None,
            error_message=None,
            records_processed=None
        )
        
        def mock_save_pipeline_run(run):
            if run.id is None:
                run.id = 1
            return run
        
        mock_database.save_pipeline_run.side_effect = mock_save_pipeline_run
        
        # Create orchestrator
        orchestrator = PipelineOrchestrator(
            api_client=mock_api_client,
            data_processor=mock_data_processor,
            file_storage=mock_file_storage,
            database=mock_database,
            report_generator=mock_report_generator
        )
        
        # Run pipeline
        result = await orchestrator.run_full_pipeline()
        
        # Verify all steps were called
        mock_api_client.extract_all_data.assert_called_once()
        mock_data_processor.process_users.assert_called_once()
        mock_data_processor.process_posts.assert_called_once()
        mock_data_processor.process_comments.assert_called_once()
        mock_database.save_users.assert_called_once()
        mock_database.save_posts.assert_called_once()
        mock_database.save_comments.assert_called_once()
        mock_database.get_analytics_data.assert_called_once()
        mock_report_generator.generate_analytics_report.assert_called_once()
        
        # Verify result
        assert result is not None
        assert "pipeline_run" in result
        assert "analytics_report" in result
        assert result["pipeline_run"].status == PipelineStatus.SUCCESS
    
    async def test_pipeline_failure_handling(self):
        """Test pipeline failure handling"""
        # Mock dependencies
        mock_api_client = AsyncMock()
        mock_data_processor = MagicMock()
        mock_file_storage = MagicMock()
        mock_database = MagicMock()
        mock_report_generator = MagicMock()
        
        # Mock API failure
        mock_api_client.extract_all_data.side_effect = Exception("API Error")
        
        # Mock pipeline run creation
        from src.domain.entities import PipelineRun
        from datetime import datetime
        
        def mock_save_pipeline_run(run):
            if run.id is None:
                run.id = 1
            return run
        
        mock_database.save_pipeline_run.side_effect = mock_save_pipeline_run
        
        # Create orchestrator
        orchestrator = PipelineOrchestrator(
            api_client=mock_api_client,
            data_processor=mock_data_processor,
            file_storage=mock_file_storage,
            database=mock_database,
            report_generator=mock_report_generator
        )
        
        # Run pipeline and expect failure
        with pytest.raises(Exception, match="API Error"):
            await orchestrator.run_full_pipeline()
        
        # Verify failure was recorded
        assert mock_database.save_pipeline_run.call_count == 2  # Initial + failure update
        
        # Get the final call to verify failure status
        final_call_args = mock_database.save_pipeline_run.call_args_list[-1]
        failed_run = final_call_args[0][0]
        assert failed_run.status == PipelineStatus.FAILED
        assert failed_run.error_message == "API Error"