#!/usr/bin/env python3
"""
Demo script showcasing Congress API + MCP integration.
"""

import asyncio
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from congress_mcp.api import CongressAPIClient
from congress_mcp.models import CommitteeList, HearingList, BillList
from congress_mcp.mcp_server import CongressMCPServer
from congress_mcp.utils import logger


async def demo_api_client():
    """Demonstrate the API client functionality."""
    logger.info("🏛️  Congress API Client Demo")
    logger.info("=" * 50)
    
    async with CongressAPIClient() as client:
        # Get current Congress info
        current_congress = await client.get_current_congress()
        logger.info(f"📊 Current Congress: {current_congress} (2025-2026)")
        
        # Show rate limits
        status = client.get_rate_limit_status()
        logger.info(f"⚡ Rate Limits: {status['hour']['remaining']}/4500 hourly, {status['minute']['remaining']}/75 per minute")
        
        # Get committees with models
        logger.info(f"\\n🏛️  Fetching House Committees...")
        committees_data = await client.get_committees(congress=118, chamber="house", limit=3)
        committees = CommitteeList(**committees_data)
        
        for committee in committees.committees:
            logger.info(f"  • {committee.name}")
            logger.info(f"    Type: {committee.get_type_display()}")
            logger.info(f"    Subcommittees: {committee.get_subcommittee_count()}")
        
        # Get recent bills
        logger.info(f"\\n📜 Recent Bills...")
        bills_data = await client.get_bills(congress=118, limit=2)
        bills = BillList(**bills_data)
        
        for bill in bills.bills:
            logger.info(f"  • {bill.get_bill_identifier()}: {bill.title}")
            logger.info(f"    Latest Action: {bill.get_latest_action_text()}")
            logger.info(f"    Enacted: {'Yes' if bill.is_enacted() else 'No'}")


async def demo_mcp_server():
    """Demonstrate the MCP server functionality."""
    logger.info(f"\\n🔧 MCP Server Demo")
    logger.info("=" * 50)
    
    server = CongressMCPServer()
    server.client = CongressAPIClient()
    
    try:
        # Demo various tools
        logger.info("🛠️  Available Tools:")
        
        # Congress info tool
        result = await server._call_tool("get_congress_info", {})
        logger.info("📊 Congress Info:")
        for line in result.split('\\n')[:3]:  # First 3 lines
            logger.info(f"    {line}")
        
        # Committee tool
        result = await server._call_tool("get_committees", {"limit": 2, "chamber": "senate"})
        logger.info("\\n🏛️  Senate Committees:")
        lines = result.split('\\n')
        for line in lines[:6]:  # First few lines
            if line.strip():
                logger.info(f"    {line}")
        
        # Rate limit tool
        result = await server._call_tool("get_rate_limit_status", {})
        logger.info("\\n⚡ Rate Limit Status:")
        for line in result.split('\\n')[:5]:  # First 5 lines
            if line.strip():
                logger.info(f"    {line}")
        
        # Demo resource reading
        logger.info("\\n📚 Resources:")
        result = await server._read_resource("congress://status/api")
        logger.info(f"    Status: {result[:50]}...")
        
    finally:
        await server.client.close()


async def main():
    """Run the full demonstration."""
    logger.info("🚀 Congress API + MCP Integration Demo")
    logger.info("🔗 Exploring US Congressional Data with Modern MCP Protocol")
    logger.info("=" * 70)
    
    try:
        # Demo API client
        await demo_api_client()
        
        # Demo MCP server
        await demo_mcp_server()
        
        logger.info("\\n" + "=" * 70)
        logger.info("✅ Demo completed successfully!")
        logger.info("🎯 Ready for integration with Memex and other MCP clients")
        logger.info("📊 Rate-limited and cached for responsible API usage")
        logger.info("🏛️  Comprehensive congressional data access via MCP protocol")
        
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())