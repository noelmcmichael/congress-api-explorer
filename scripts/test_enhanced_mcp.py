#!/usr/bin/env python3
"""
Test enhanced MCP server with search capabilities.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from congress_mcp.mcp_server.server import CongressMCPServer
from congress_mcp.utils import logger


async def test_enhanced_mcp():
    """Test enhanced MCP server functionality."""
    logger.info("Testing enhanced MCP server with search capabilities...")
    
    try:
        # Create server instance
        server = CongressMCPServer()
        
        # Initialize client manually for testing
        from congress_mcp.api import CongressAPIClient, CongressSearchEngine
        server.client = CongressAPIClient()
        server.search_engine = CongressSearchEngine(server.client)
        
        # Test enhanced search tools
        logger.info("Testing search_all tool...")
        result = await server._search_all(
            query="technical",
            limit=5
        )
        logger.info(f"search_all result: {result[:200]}...")
        
        logger.info("Testing search_by_topic tool...")
        result = await server._search_by_topic(
            topic="healthcare",
            limit=5
        )
        logger.info(f"search_by_topic result: {result[:200]}...")
        
        # Test tools count
        from congress_mcp.mcp_server.tools import register_tools
        tools = await register_tools()
        logger.info(f"Total tools registered: {len(tools)}")
        
        # List tool names
        tool_names = [tool.name for tool in tools]
        logger.info(f"Tool names: {tool_names}")
        
        # Close client
        await server.client.close()
        
        logger.info("Enhanced MCP server testing completed successfully!")
        
    except Exception as e:
        logger.error(f"Error testing enhanced MCP server: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(test_enhanced_mcp())