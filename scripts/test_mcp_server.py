#!/usr/bin/env python3
"""
Test script for MCP server functionality.
"""

import asyncio
import json
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from congress_mcp.mcp_server import CongressMCPServer
from congress_mcp.api import CongressAPIClient
from congress_mcp.utils import logger


async def test_mcp_server():
    """Test the MCP server functionality."""
    
    logger.info("Testing Congress MCP Server functionality...")
    
    # Create server instance
    server = CongressMCPServer()
    
    try:
        # Test tool and resource registration
        logger.info("Testing tool registration...")
        from congress_mcp.mcp_server.tools import register_tools
        tools = await register_tools()
        logger.info(f"Registered {len(tools)} tools:")
        for tool in tools[:5]:  # Show first 5
            logger.info(f"  - {tool.name}: {tool.description}")
        
        logger.info("Testing resource registration...")
        from congress_mcp.mcp_server.resources import register_resources
        resources = await register_resources()
        logger.info(f"Registered {len(resources)} resources:")
        for resource in resources[:5]:  # Show first 5
            logger.info(f"  - {resource.name}: {resource.description}")
        
        # Test individual tool methods directly
        logger.info("Testing tool implementations...")
        
        # Initialize client for testing
        server.client = CongressAPIClient()
        
        # Test get_congress_info
        logger.info("Testing get_congress_info...")
        result = await server._call_tool("get_congress_info", {})
        logger.info(f"Congress info: {result}")
        
        # Test get_rate_limit_status
        logger.info("Testing get_rate_limit_status...")
        result = await server._call_tool("get_rate_limit_status", {})
        logger.info(f"Rate limit status: {result}")
        
        # Test get_committees with limited results
        logger.info("Testing get_committees...")
        result = await server._call_tool("get_committees", {"limit": 3})
        logger.info(f"Committees result: {result[:200]}...")
        
        # Test resource reading
        logger.info("Testing resource reading...")
        result = await server._read_resource("congress://status/api")
        logger.info(f"Status resource: {result}")
        
        logger.info("MCP server testing completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during MCP server testing: {e}")
        raise
    
    finally:
        # Cleanup
        if server.client:
            await server.client.close()


if __name__ == "__main__":
    asyncio.run(test_mcp_server())