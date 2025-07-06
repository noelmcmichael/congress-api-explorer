"""
Congress API client with rate limiting and caching.
"""

import asyncio
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlencode

import httpx
from pydantic import BaseModel, Field

from ..utils.config import settings
from ..utils.logging import logger
from ..utils.cache import cache_manager
from .rate_limiter import rate_limiter


class CongressAPIError(Exception):
    """Base exception for Congress API errors."""
    pass


class CongressAPIClient:
    """
    Async client for the Congress API with rate limiting and caching.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.congress_api_key
        self.base_url = settings.congress_api_base_url
        self.session: Optional[httpx.AsyncClient] = None
        self._session_lock = asyncio.Lock()
    
    async def _get_session(self) -> httpx.AsyncClient:
        """Get or create HTTP session."""
        if self.session is None:
            async with self._session_lock:
                if self.session is None:
                    self.session = httpx.AsyncClient(
                        timeout=httpx.Timeout(30.0),
                        limits=httpx.Limits(
                            max_keepalive_connections=10,
                            max_connections=20
                        )
                    )
        return self.session
    
    async def close(self) -> None:
        """Close HTTP session."""
        if self.session:
            await self.session.aclose()
            self.session = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    def _build_url(self, endpoint: str, **params) -> str:
        """Build full URL with parameters."""
        # Ensure base URL ends with / for proper joining
        base_url = self.base_url.rstrip('/') + '/'
        url = urljoin(base_url, endpoint)
        
        # Add API key
        params["api_key"] = self.api_key
        
        # Add format if not specified
        if "format" not in params:
            params["format"] = "json"
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        if params:
            url += "?" + urlencode(params)
        
        return url
    
    async def _make_request(
        self,
        endpoint: str,
        cache_type: str = "default",
        use_cache: bool = True,
        **params
    ) -> Dict[str, Any]:
        """
        Make an API request with rate limiting and caching.
        
        Args:
            endpoint: API endpoint path
            cache_type: Cache category for TTL calculation
            use_cache: Whether to use caching
            **params: Query parameters
            
        Returns:
            API response data
            
        Raises:
            CongressAPIError: If request fails
        """
        
        # Check cache first
        if use_cache:
            cached_response = await cache_manager.get(
                cache_type, endpoint, **params
            )
            if cached_response:
                logger.debug(f"Cache hit for {endpoint}")
                return cached_response
        
        # Wait for rate limit
        await rate_limiter.wait_if_needed()
        
        # Build URL
        url = self._build_url(endpoint, **params)
        
        # Make request
        session = await self._get_session()
        
        try:
            logger.debug(f"Making request to: {endpoint}")
            response = await session.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            # Cache successful response
            if use_cache:
                await cache_manager.set(cache_type, data, endpoint, **params)
            
            logger.debug(f"Request successful for {endpoint}")
            return data
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error for {endpoint}: {e.response.status_code}")
            raise CongressAPIError(
                f"API request failed with status {e.response.status_code}: {e.response.text}"
            ) from e
        except httpx.RequestError as e:
            logger.error(f"Request error for {endpoint}: {e}")
            raise CongressAPIError(f"Request failed: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error for {endpoint}: {e}")
            raise CongressAPIError(f"Unexpected error: {e}") from e
    
    # Committee Methods
    
    async def get_committees(
        self,
        congress: Optional[int] = None,
        chamber: Optional[str] = None,
        limit: int = 250,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get committees information.
        
        Args:
            congress: Congress number (e.g., 118 for current)
            chamber: Chamber (house, senate, joint)
            limit: Number of results to return
            offset: Starting offset
            
        Returns:
            Committee data
        """
        endpoint = "committee"
        params = {
            "congress": congress,
            "chamber": chamber,
            "limit": limit,
            "offset": offset
        }
        
        return await self._make_request(endpoint, "committee", **params)
    
    async def get_committee_meetings(
        self,
        congress: Optional[int] = None,
        chamber: Optional[str] = None,
        committee: Optional[str] = None,
        limit: int = 250,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get committee meetings information.
        
        Args:
            congress: Congress number
            chamber: Chamber (house, senate, joint)
            committee: Committee code
            limit: Number of results to return
            offset: Starting offset
            
        Returns:
            Meeting data
        """
        endpoint = "committee-meeting"
        params = {
            "congress": congress,
            "chamber": chamber,
            "committee": committee,
            "limit": limit,
            "offset": offset
        }
        
        return await self._make_request(endpoint, "hearing", **params)
    
    async def get_committee_hearings(
        self,
        congress: Optional[int] = None,
        chamber: Optional[str] = None,
        committee: Optional[str] = None,
        limit: int = 250,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get committee hearings information.
        
        Args:
            congress: Congress number
            chamber: Chamber (house, senate, joint)
            committee: Committee code
            limit: Number of results to return
            offset: Starting offset
            
        Returns:
            Hearing data
        """
        endpoint = "hearing"
        params = {
            "congress": congress,
            "chamber": chamber,
            "committee": committee,
            "limit": limit,
            "offset": offset
        }
        
        return await self._make_request(endpoint, "hearing", **params)
    
    # Bill Methods
    
    async def get_bills(
        self,
        congress: Optional[int] = None,
        bill_type: Optional[str] = None,
        limit: int = 250,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get bills information.
        
        Args:
            congress: Congress number
            bill_type: Bill type (hr, s, hjres, sjres, hconres, sconres, hres, sres)
            limit: Number of results to return
            offset: Starting offset
            
        Returns:
            Bill data
        """
        endpoint = "bill"
        params = {
            "congress": congress,
            "type": bill_type,
            "limit": limit,
            "offset": offset
        }
        
        return await self._make_request(endpoint, "bill", **params)
    
    async def get_bill_details(
        self,
        congress: int,
        bill_type: str,
        bill_number: int
    ) -> Dict[str, Any]:
        """
        Get detailed information about a specific bill.
        
        Args:
            congress: Congress number
            bill_type: Bill type
            bill_number: Bill number
            
        Returns:
            Detailed bill data
        """
        endpoint = f"bill/{congress}/{bill_type}/{bill_number}"
        
        return await self._make_request(endpoint, "bill")
    
    # Member Methods
    
    async def get_members(
        self,
        congress: Optional[int] = None,
        chamber: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 250,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get members information.
        
        Args:
            congress: Congress number
            chamber: Chamber (house, senate)
            state: State abbreviation
            limit: Number of results to return
            offset: Starting offset
            
        Returns:
            Member data
        """
        endpoint = "member"
        params = {
            "congress": congress,
            "chamber": chamber,
            "state": state,
            "limit": limit,
            "offset": offset
        }
        
        return await self._make_request(endpoint, "member", **params)
    
    # Utility Methods
    
    async def get_current_congress(self) -> int:
        """
        Get current Congress number.
        
        Returns:
            Current Congress number
        """
        # Calculate current Congress based on year
        # 117th Congress: 2021-2022
        # 118th Congress: 2023-2024
        # 119th Congress: 2025-2026
        # etc.
        current_year = datetime.now().year
        # First Congress started in 1789
        # Each Congress is 2 years, starting in odd years
        if current_year % 2 == 0:
            # Even year - use previous year for calculation
            congress_year = current_year - 1
        else:
            # Odd year - use current year
            congress_year = current_year
        
        congress_number = ((congress_year - 1789) // 2) + 1
        
        return congress_number
    
    async def get_recent_hearings(
        self,
        days_back: int = 30,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get recent hearings from the last N days.
        
        Args:
            days_back: Number of days to look back
            limit: Maximum number of hearings to return
            
        Returns:
            List of recent hearings
        """
        current_congress = await self.get_current_congress()
        
        # Get hearings for current congress
        hearings_data = await self.get_committee_hearings(
            congress=current_congress,
            limit=limit
        )
        
        # Filter by date (this is a simplified implementation)
        # In a real implementation, you'd want to use date filtering parameters
        return hearings_data.get("hearings", [])
    
    def get_rate_limit_status(self) -> Dict[str, Dict[str, int]]:
        """Get current rate limit status."""
        return rate_limiter.get_rate_limit_status()


# Create a default client instance
async def create_client(api_key: Optional[str] = None) -> CongressAPIClient:
    """Create a new Congress API client."""
    return CongressAPIClient(api_key)