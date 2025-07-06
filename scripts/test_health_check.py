#!/usr/bin/env python3
"""
Test health check functionality.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from congress_mcp.utils import health_checker
from congress_mcp.mcp_server.server import CongressMCPServer
from congress_mcp.utils import logger


async def test_health_check():
    """Test health check functionality."""
    logger.info("Testing health check functionality...")
    
    try:
        # Test direct health checker
        logger.info("Testing direct health checker...")
        health = await health_checker.check_health()
        
        logger.info(f"Overall health status: {health.status.value}")
        logger.info(f"Uptime: {health_checker.get_uptime_formatted()}")
        logger.info(f"Number of checks: {len(health.checks)}")
        
        for check in health.checks:
            logger.info(f"  • {check.name}: {check.status.value} - {check.message}")
        
        # Test health as dict
        health_dict = health.to_dict()
        logger.info(f"Health dict keys: {list(health_dict.keys())}")
        
        # Test MCP server health tools
        logger.info("Testing MCP server health tools...")
        server = CongressMCPServer()
        
        # Initialize for testing
        from congress_mcp.api import CongressAPIClient, CongressSearchEngine
        server.client = CongressAPIClient()
        server.search_engine = CongressSearchEngine(server.client)
        
        # Test health status tool
        logger.info("Testing get_health_status tool...")
        result = await server._get_health_status()
        logger.info(f"Health status result: {result[:300]}...")
        
        # Test system metrics tool
        logger.info("Testing get_system_metrics tool...")
        result = await server._get_system_metrics()
        logger.info(f"System metrics result: {result[:300]}...")
        
        # Test tools count
        from congress_mcp.mcp_server.tools import register_tools
        tools = await register_tools()
        logger.info(f"Total tools registered: {len(tools)}")
        
        # Close client
        await server.client.close()
        
        logger.info("Health check testing completed successfully!")
        
    except Exception as e:
        logger.error(f"Error testing health check: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(test_health_check())