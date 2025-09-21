from typing import List, Dict, Any
from datetime import datetime
import logging

from src.domain.entities import User, Post, Comment
from src.domain.interfaces import DataProcessorInterface

logger = logging.getLogger(__name__)


class DataProcessor(DataProcessorInterface):
    """Service for processing and transforming raw data"""
    
    def process_users(self, raw_users: List[Dict[str, Any]]) -> List[User]:
        """Process raw user data into User entities"""
        processed_users = []
        
        for raw_user in raw_users:
            try:
                user = User(
                    id=raw_user.get("id"),
                    name=raw_user.get("name", "").strip(),
                    username=raw_user.get("username", "").strip(),
                    email=raw_user.get("email", "").strip().lower(),
                    phone=self._clean_phone(raw_user.get("phone", "")),
                    website=self._clean_website(raw_user.get("website", "")),
                    address=self._process_address(raw_user.get("address", {})),
                    company=self._process_company(raw_user.get("company", {})),
                    created_at=datetime.utcnow()
                )
                processed_users.append(user)
                
            except Exception as e:
                logger.warning(f"Error processing user {raw_user.get('id', 'unknown')}: {e}")
                continue
        
        logger.info(f"Processed {len(processed_users)} users")
        return processed_users
    
    def process_posts(self, raw_posts: List[Dict[str, Any]]) -> List[Post]:
        """Process raw post data into Post entities"""
        processed_posts = []
        
        for raw_post in raw_posts:
            try:
                post = Post(
                    id=raw_post.get("id"),
                    user_id=raw_post.get("userId"),
                    title=self._clean_text(raw_post.get("title", "")),
                    body=self._clean_text(raw_post.get("body", "")),
                    created_at=datetime.utcnow()
                )
                processed_posts.append(post)
                
            except Exception as e:
                logger.warning(f"Error processing post {raw_post.get('id', 'unknown')}: {e}")
                continue
        
        logger.info(f"Processed {len(processed_posts)} posts")
        return processed_posts
    
    def process_comments(self, raw_comments: List[Dict[str, Any]]) -> List[Comment]:
        """Process raw comment data into Comment entities"""
        processed_comments = []
        
        for raw_comment in raw_comments:
            try:
                comment = Comment(
                    id=raw_comment.get("id"),
                    post_id=raw_comment.get("postId"),
                    name=self._clean_text(raw_comment.get("name", "")),
                    email=raw_comment.get("email", "").strip().lower(),
                    body=self._clean_text(raw_comment.get("body", "")),
                    created_at=datetime.utcnow()
                )
                processed_comments.append(comment)
                
            except Exception as e:
                logger.warning(f"Error processing comment {raw_comment.get('id', 'unknown')}: {e}")
                continue
        
        logger.info(f"Processed {len(processed_comments)} comments")
        return processed_comments
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text data"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize line breaks
        text = " ".join(text.split())
        
        # Basic text cleaning
        text = text.strip()
        
        return text
    
    def _clean_phone(self, phone: str) -> str:
        """Clean phone number"""
        if not phone:
            return ""
        
        # Remove common phone number formatting
        cleaned = phone.replace(" ", "").replace("-", "").replace(".", "")
        cleaned = cleaned.replace("(", "").replace(")", "")
        
        return cleaned
    
    def _clean_website(self, website: str) -> str:
        """Clean website URL"""
        if not website:
            return ""
        
        website = website.strip().lower()
        
        # Add http:// if no protocol specified
        if website and not website.startswith(('http://', 'https://')):
            website = f"http://{website}"
        
        return website
    
    def _process_address(self, address: Dict[str, Any]) -> Dict[str, Any]:
        """Process address data"""
        if not address:
            return {}
        
        processed_address = {
            "street": address.get("street", "").strip(),
            "suite": address.get("suite", "").strip(),
            "city": address.get("city", "").strip(),
            "zipcode": address.get("zipcode", "").strip(),
        }
        
        # Process geo coordinates if available
        geo = address.get("geo", {})
        if geo:
            try:
                processed_address["geo"] = {
                    "lat": float(geo.get("lat", 0)),
                    "lng": float(geo.get("lng", 0))
                }
            except (ValueError, TypeError):
                processed_address["geo"] = {"lat": 0.0, "lng": 0.0}
        
        return processed_address
    
    def _process_company(self, company: Dict[str, Any]) -> Dict[str, Any]:
        """Process company data"""
        if not company:
            return {}
        
        return {
            "name": company.get("name", "").strip(),
            "catchPhrase": company.get("catchPhrase", "").strip(),
            "bs": company.get("bs", "").strip()
        }