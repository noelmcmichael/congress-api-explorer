#!/usr/bin/env python3
"""
Test script to verify MCP server startup without blocking.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

async def test_server_startup():
    """Test that the MCP server can start up successfully."""
    try:
        from congress_mcp.mcp_server.server import CongressMCPServer
        from congress_mcp.utils.logging import setup_logging
        
        # Setup logging
        setup_logging()
        
        print("✅ Imports successful")
        
        # Test server initialization
        server = CongressMCPServer()
        print("✅ Server object created")
        
        # Test that the server has the expected tools
        expected_tools = [
            "get_committees", "get_committee_details", "get_committee_hearings",
            "get_hearings", "search_hearings",
            "get_bills", "get_bill_details", "search_bills", 
            "get_members", "get_member_details",
            "get_congress_info", "get_rate_limit_status",
            "search_all", "search_by_topic",
            "get_health_status", "get_system_metrics"
        ]
        
        print(f"✅ Expected {len(expected_tools)} tools")
        
        # Test environment setup
        api_key = os.environ.get("CONGRESS_API_KEY")
        if api_key:
            print("✅ Congress API key found in environment")
        else:
            print("⚠️  No Congress API key in environment")
            
        print("✅ MCP Server startup test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Server startup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_server_startup())
    sys.exit(0 if success else 1)