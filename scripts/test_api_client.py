#!/usr/bin/env python3
"""
Test script for Congress API client.
"""

import asyncio
import os
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from congress_mcp.api import CongressAPIClient
from congress_mcp.utils import logger


async def test_api_client():
    """Test the Congress API client."""
    
    # Set API key if not in environment
    api_key = "kF6SxbPbbXXjOGDd2FIFaYUkZRuYfQN2OsQtnj9G"
    
    logger.info("Testing Congress API client...")
    
    async with CongressAPIClient(api_key) as client:
        try:
            # Test rate limit status
            logger.info("Rate limit status:")
            status = client.get_rate_limit_status()
            for window, info in status.items():
                logger.info(f"  {window}: {info['used']}/{info['limit']} (remaining: {info['remaining']})")
            
            # Test getting current congress
            current_congress = await client.get_current_congress()
            logger.info(f"Current Congress: {current_congress}")
            
            # Test getting committees (limited results)
            logger.info("Fetching committees...")
            # Use 118th Congress for testing (2023-2024, has data)
            test_congress = 118
            committees = await client.get_committees(
                congress=test_congress,
                limit=5
            )
            
            if "committees" in committees:
                logger.info(f"Found {len(committees['committees'])} committees")
                for committee in committees["committees"][:3]:  # Show first 3
                    name = committee.get("name", "Unknown")
                    chamber = committee.get("chamber", "Unknown")
                    logger.info(f"  - {name} ({chamber})")
            else:
                logger.info("No committees found or unexpected response format")
                logger.info(f"Response keys: {list(committees.keys())}")
            
            # Test getting recent hearings (limited results)
            logger.info("Fetching recent hearings...")
            hearings = await client.get_committee_hearings(
                congress=test_congress,
                limit=3
            )
            
            if "hearings" in hearings:
                logger.info(f"Found {len(hearings['hearings'])} hearings")
                for hearing in hearings["hearings"][:2]:  # Show first 2
                    title = hearing.get("title", "Unknown")
                    date = hearing.get("date", "Unknown")
                    logger.info(f"  - {title} ({date})")
            else:
                logger.info("No hearings found or unexpected response format")
                logger.info(f"Response keys: {list(hearings.keys())}")
            
            # Final rate limit check
            logger.info("Final rate limit status:")
            status = client.get_rate_limit_status()
            for window, info in status.items():
                logger.info(f"  {window}: {info['used']}/{info['limit']} (remaining: {info['remaining']})")
            
        except Exception as e:
            logger.error(f"Error during API testing: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(test_api_client())