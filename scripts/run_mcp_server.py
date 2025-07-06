#!/usr/bin/env python3
"""
Standalone MCP server runner for Congress API Explorer.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp.server.stdio import stdio_server
from congress_mcp.mcp_server import CongressMCPServer
from congress_mcp.utils import logger


async def main():
    """Run the MCP server."""
    logger.info("Starting Congress API MCP Server...")
    
    try:
        # Create server instance
        server = CongressMCPServer()
        
        # Run with stdio transport
        async with stdio_server() as (read_stream, write_stream):
            await server.serve(read_stream, write_stream)
            
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())