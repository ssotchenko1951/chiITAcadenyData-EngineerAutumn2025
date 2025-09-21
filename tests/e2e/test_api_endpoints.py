import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch

from src.presentation.api.app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    return TestClient(app)


class TestAPIEndpoints:
    """End-to-end tests for API endpoints"""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["service"] == "data-pipeline-api"
    
    def test_analytics_summary_endpoint(self, client):
        """Test analytics summary endpoint"""
        mock_analytics = {
            "total_users": 10,
            "total_posts": 50,
            "total_comments": 150,
            "average_posts_per_user": 5.0,
            "most_active_user": "John Doe",
            "top_posts_by_engagement": []
        }
        
        with patch("src.application.services.dependency_injection.get_database_repository") as mock_get_db:
            mock_repository = MagicMock()
            mock_repository.get_analytics_data.return_value = mock_analytics
            mock_get_db.return_value = mock_repository
            
            response = client.get("/analytics/summary")
            
            assert response.status_code == 200
            data = response.json()
            assert data == mock_analytics
    
    def test_user_statistics_endpoint(self, client):
        """Test user statistics endpoint"""
        mock_analytics = {
            "total_users": 10,
            "average_posts_per_user": 5.0,
            "most_active_user": "John Doe"
        }
        
        with patch("src.application.services.dependency_injection.get_database_repository") as mock_get_db:
            mock_repository = MagicMock()
            mock_repository.get_analytics_data.return_value = mock_analytics
            mock_get_db.return_value = mock_repository
            
            response = client.get("/analytics/users/stats")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_users"] == 10
            assert data["average_posts_per_user"] == 5.0
            assert data["most_active_user"] == "John Doe"
    
    def test_engagement_metrics_endpoint(self, client):
        """Test engagement metrics endpoint"""
        mock_analytics = {
            "total_posts": 50,
            "total_comments": 150,
            "top_posts_by_engagement": [
                {"title": "Popular Post", "comment_count": 10, "author": "John Doe"}
            ]
        }
        
        with patch("src.application.services.dependency_injection.get_database_repository") as mock_get_db:
            mock_repository = MagicMock()
            mock_repository.get_analytics_data.return_value = mock_analytics
            mock_get_db.return_value = mock_repository
            
            response = client.get("/analytics/engagement")
            
            assert response.status_code == 200
            data = response.json()
            assert data["total_posts"] == 50
            assert data["total_comments"] == 150
            assert len(data["top_posts"]) == 1
    
    def test_pipeline_run_endpoint(self, client):
        """Test pipeline run endpoint"""
        with patch("src.application.services.dependency_injection.get_pipeline_orchestrator") as mock_get_orchestrator:
            mock_orchestrator = AsyncMock()
            mock_get_orchestrator.return_value = mock_orchestrator
            
            response = client.post("/pipeline/run")
            
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "task_id" in data
    
    def test_pipeline_runs_list_endpoint(self, client):
        """Test pipeline runs list endpoint"""
        from src.domain.entities import PipelineRun, PipelineStatus
        from datetime import datetime
        
        mock_runs = [
            PipelineRun(
                id=1,
                status=PipelineStatus.SUCCESS,
                started_at=datetime(2024, 1, 15, 10, 0, 0),
                completed_at=datetime(2024, 1, 15, 10, 30, 0),
                error_message=None,
                records_processed=100
            )
        ]
        
        with patch("src.application.services.dependency_injection.get_pipeline_orchestrator") as mock_get_orchestrator:
            mock_orchestrator = MagicMock()
            mock_orchestrator.database.get_pipeline_runs.return_value = mock_runs
            mock_get_orchestrator.return_value = mock_orchestrator
            
            response = client.get("/pipeline/runs")
            
            assert response.status_code == 200
            data = response.json()
            assert "runs" in data
            assert len(data["runs"]) == 1
            
            run_data = data["runs"][0]
            assert run_data["id"] == 1
            assert run_data["status"] == "success"
            assert run_data["records_processed"] == 100
    
    def test_reports_list_endpoint(self, client):
        """Test reports list endpoint"""
        mock_files = ["analytics_2024-01-15.json", "analytics_2024-01-15.csv"]
        
        with patch("src.application.services.dependency_injection.get_file_storage") as mock_get_storage:
            mock_storage = MagicMock()
            mock_storage.list_files.return_value = mock_files
            mock_storage.reports_dir = MagicMock()
            
            # Mock file stats
            mock_file_path = MagicMock()
            mock_file_path.exists.return_value = True
            mock_file_path.stat.return_value = MagicMock(st_size=1024, st_ctime=1705315200.0)
            mock_storage.reports_dir.__truediv__.return_value = mock_file_path
            
            mock_get_storage.return_value = mock_storage
            
            response = client.get("/reports/")
            
            assert response.status_code == 200
            data = response.json()
            assert "reports" in data
            assert len(data["reports"]) == 2