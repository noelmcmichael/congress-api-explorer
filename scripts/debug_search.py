#!/usr/bin/env python3
"""
Debug search functionality.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from congress_mcp.api import CongressAPIClient, CongressSearchEngine
from congress_mcp.utils import logger


async def debug_search():
    """Debug search functionality."""
    logger.info("Debugging search functionality...")
    
    try:
        # Initialize client and search engine
        client = CongressAPIClient()
        search_engine = CongressSearchEngine(client)
        
        # Test bill search with debugging
        logger.info("Testing bill search with debugging...")
        results = await search_engine._search_bills("technical", limit=5)
        
        logger.info(f"Bill search results: {len(results)}")
        for result in results:
            logger.info(f"  • {result.title} - Score: {result.relevance_score:.1f}")
        
        # Test direct API call
        logger.info("Testing direct API call...")
        bills_data = await client.get_bills(limit=5)
        bills = bills_data.get("bills", [])
        
        logger.info(f"Direct API returned {len(bills)} bills")
        for bill in bills:
            title = bill.get("title", "")
            logger.info(f"  • {title}")
            
            # Check if 'technical' is in title
            if "technical" in title.lower():
                logger.info(f"    → Found 'technical' in title!")
        
        # Close client
        await client.close()
        
        logger.info("Debug search completed!")
        
    except Exception as e:
        logger.error(f"Error debugging search: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(debug_search())