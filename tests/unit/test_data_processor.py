import pytest
from datetime import datetime

from src.application.services.data_processor import DataProcessor


class TestDataProcessor:
    
    def test_process_users_success(self, data_processor, sample_users_data):
        """Test successful user processing"""
        processed_users = data_processor.process_users(sample_users_data)
        
        assert len(processed_users) == 1
        user = processed_users[0]
        
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.username == "johndoe"
        assert user.email == "john@example.com"
        assert user.phone == "1234567890"  # Phone should be cleaned
        assert user.website == "http://johndoe.com"  # Website should have http://
        assert isinstance(user.created_at, datetime)
        
        # Check address processing
        assert user.address["street"] == "123 Main St"
        assert user.address["geo"]["lat"] == 40.7128
        assert user.address["geo"]["lng"] == -74.0060
        
        # Check company processing
        assert user.company["name"] == "Doe Industries"
    
    def test_process_users_with_invalid_data(self, data_processor):
        """Test user processing with invalid data"""
        invalid_data = [
            {"id": None, "name": "Invalid User"},  # Invalid ID
            {},  # Empty object
        ]
        
        processed_users = data_processor.process_users(invalid_data)
        assert len(processed_users) == 0  # Should skip invalid records
    
    def test_process_posts_success(self, data_processor, sample_posts_data):
        """Test successful post processing"""
        processed_posts = data_processor.process_posts(sample_posts_data)
        
        assert len(processed_posts) == 1
        post = processed_posts[0]
        
        assert post.id == 1
        assert post.user_id == 1
        assert post.title == "Sample Post"
        assert post.body == "This is a sample post content."
        assert isinstance(post.created_at, datetime)
    
    def test_process_comments_success(self, data_processor, sample_comments_data):
        """Test successful comment processing"""
        processed_comments = data_processor.process_comments(sample_comments_data)
        
        assert len(processed_comments) == 1
        comment = processed_comments[0]
        
        assert comment.id == 1
        assert comment.post_id == 1
        assert comment.name == "Great post!"
        assert comment.email == "commenter@example.com"
        assert comment.body == "I really enjoyed reading this post."
        assert isinstance(comment.created_at, datetime)
    
    def test_clean_phone_number(self, data_processor):
        """Test phone number cleaning"""
        test_cases = [
            ("123-456-7890", "1234567890"),
            ("(123) 456-7890", "1234567890"),
            ("123.456.7890", "1234567890"),
            ("123 456 7890", "1234567890"),
            ("", ""),
        ]
        
        for input_phone, expected in test_cases:
            result = data_processor._clean_phone(input_phone)
            assert result == expected
    
    def test_clean_website(self, data_processor):
        """Test website URL cleaning"""
        test_cases = [
            ("example.com", "http://example.com"),
            ("http://example.com", "http://example.com"),
            ("https://example.com", "https://example.com"),
            ("", ""),
        ]
        
        for input_website, expected in test_cases:
            result = data_processor._clean_website(input_website)
            assert result == expected