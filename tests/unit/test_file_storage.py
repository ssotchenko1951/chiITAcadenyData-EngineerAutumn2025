import pytest
from datetime import datetime
import json
import pandas as pd


class TestFileStorage:
    
    def test_save_and_load_raw_data(self, temp_file_storage):
        """Test saving and loading raw data"""
        test_data = {"test": "data", "number": 123}
        test_date = datetime(2024, 1, 15)
        
        # Save data
        filepath = temp_file_storage.save_raw_data(
            data=test_data,
            filename="test_data",
            date_partition=test_date
        )
        
        assert filepath is not None
        assert "2024-01-15" in filepath
        assert "test_data.json" in filepath
        
        # Load data
        loaded_data = temp_file_storage.load_raw_data(
            filename="test_data",
            date_partition=test_date
        )
        
        assert loaded_data == test_data
    
    def test_save_processed_data_list(self, temp_file_storage):
        """Test saving processed data as list"""
        test_data = [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Jane"}
        ]
        test_date = datetime(2024, 1, 15)
        
        filepath = temp_file_storage.save_processed_data(
            data=test_data,
            filename="users",
            date_partition=test_date
        )
        
        assert filepath is not None
        assert "users.parquet" in filepath
        
        # Load and verify
        loaded_df = temp_file_storage.load_processed_data(
            filename="users",
            date_partition=test_date
        )
        
        assert len(loaded_df) == 2
        assert list(loaded_df.columns) == ["id", "name"]
    
    def test_save_report_json(self, temp_file_storage):
        """Test saving report in JSON format"""
        report_data = {
            "total_users": 10,
            "total_posts": 50,
            "generated_at": "2024-01-15T10:00:00"
        }
        
        filepath = temp_file_storage.save_report(
            data=report_data,
            filename="analytics_report",
            format="json"
        )
        
        assert filepath is not None
        assert "analytics_report.json" in filepath
        
        # Verify file exists and contains correct data
        with open(filepath, 'r') as f:
            loaded_data = json.load(f)
        
        assert loaded_data == report_data
    
    def test_save_report_csv(self, temp_file_storage):
        """Test saving report in CSV format"""
        report_data = [
            {"user_id": 1, "post_count": 5},
            {"user_id": 2, "post_count": 3}
        ]
        
        filepath = temp_file_storage.save_report(
            data=report_data,
            filename="user_stats",
            format="csv"
        )
        
        assert filepath is not None
        assert "user_stats.csv" in filepath
        
        # Verify file exists and contains correct data
        loaded_df = pd.read_csv(filepath)
        assert len(loaded_df) == 2
        assert "user_id" in loaded_df.columns
        assert "post_count" in loaded_df.columns
    
    def test_list_files(self, temp_file_storage):
        """Test listing files"""
        # Save some test files
        test_date = datetime(2024, 1, 15)
        
        temp_file_storage.save_raw_data({"test": 1}, "file1", test_date)
        temp_file_storage.save_raw_data({"test": 2}, "file2", test_date)
        temp_file_storage.save_report({"report": 1}, "report1", "json")
        
        # List raw files
        raw_files = temp_file_storage.list_files("raw", test_date)
        assert len(raw_files) == 2
        assert "file1.json" in raw_files
        assert "file2.json" in raw_files
        
        # List report files
        report_files = temp_file_storage.list_files("reports")
        assert len(report_files) == 1
        assert "report1.json" in report_files