import httpx
from typing import List, Dict, Any
import asyncio
from datetime import datetime
import logging

from src.domain.interfaces import DataExtractorInterface
from src.config import get_settings

logger = logging.getLogger(__name__)


class APIClient(DataExtractorInterface):
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.api.base_url
        self.timeout = self.settings.api.timeout
        self.retries = self.settings.api.retries

    async def _make_request(self, endpoint: str) -> List[Dict[str, Any]]:
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(self.retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    logger.info(f"Making request to {url} (attempt {attempt + 1})")
                    response = await client.get(url)
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPError as e:
                logger.warning(f"HTTP error on attempt {attempt + 1}: {e}")
                if attempt == self.retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise

    async def extract_users(self) -> List[Dict[str, Any]]:
        return await self._make_request("/users")

    async def extract_posts(self) -> List[Dict[str, Any]]:
        return await self._make_request("/posts")

    async def extract_comments(self) -> List[Dict[str, Any]]:
        return await self._make_request("/comments")

    async def extract_all_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Extract all data concurrently"""
        users_task = asyncio.create_task(self.extract_users())
        posts_task = asyncio.create_task(self.extract_posts())
        comments_task = asyncio.create_task(self.extract_comments())

        users, posts, comments = await asyncio.gather(
            users_task, posts_task, comments_task
        )

        return {
            "users": users,
            "posts": posts,
            "comments": comments
        }