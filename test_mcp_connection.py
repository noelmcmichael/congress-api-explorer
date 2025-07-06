#!/usr/bin/env python3
"""
Test MCP server connection directly.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from congress_mcp.mcp_server.server import CongressMCPServer
from congress_mcp.api import CongressAPIClient, CongressSearchEngine


async def test_mcp_connection():
    """Test MCP server connection and tools."""
    print("Testing MCP server connection...")
    
    try:
        # Initialize server
        server = CongressMCPServer()
        
        # Test basic functionality
        print("✅ Server initialized successfully")
        print(f"✅ Server name: {server.server.name}")
        
        # Initialize client for testing
        server.client = CongressAPIClient()
        server.search_engine = CongressSearchEngine(server.client)
        
        # Test a simple tool
        result = await server._get_congress_info()
        print(f"✅ Tool test successful: {result[:100]}...")
        
        # Test health check
        health_result = await server._get_health_status()
        print(f"✅ Health check successful: {health_result[:100]}...")
        
        await server.client.close()
        print("✅ MCP server is fully functional and ready for integration!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_mcp_connection())
    sys.exit(0 if success else 1)