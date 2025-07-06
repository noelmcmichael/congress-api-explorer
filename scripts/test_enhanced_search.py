#!/usr/bin/env python3
"""
Test enhanced search functionality.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from congress_mcp.api import CongressAPIClient, CongressSearchEngine
from congress_mcp.utils import logger


async def test_enhanced_search():
    """Test enhanced search functionality."""
    logger.info("Testing enhanced search functionality...")
    
    try:
        # Initialize client and search engine
        client = CongressAPIClient()
        search_engine = CongressSearchEngine(client)
        
        # Test 1: Search all
        logger.info("Testing search_all with query 'healthcare'...")
        results = await search_engine.search_all(
            query="healthcare",
            limit=10
        )
        logger.info(f"Found {len(results)} results for 'healthcare'")
        
        for result in results[:3]:  # Show first 3 results
            logger.info(f"  • {result.title} ({result.item_type}) - Score: {result.relevance_score:.1f}")
        
        # Test 2: Search by topic
        logger.info("Testing search_by_topic with topic 'economy'...")
        results = await search_engine.search_by_topic(
            topic="economy",
            limit=10
        )
        logger.info(f"Found {len(results)} results for topic 'economy'")
        
        for result in results[:3]:  # Show first 3 results
            logger.info(f"  • {result.title} ({result.item_type}) - Score: {result.relevance_score:.1f}")
        
        # Test 3: Search specific types
        logger.info("Testing search_all with bills only...")
        results = await search_engine.search_all(
            query="budget",
            include_types=["bill"],
            limit=5
        )
        logger.info(f"Found {len(results)} bill results for 'budget'")
        
        for result in results:
            logger.info(f"  • {result.title} - Score: {result.relevance_score:.1f}")
        
        # Close client
        await client.close()
        
        logger.info("Enhanced search testing completed successfully!")
        
    except Exception as e:
        logger.error(f"Error testing enhanced search: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(test_enhanced_search())