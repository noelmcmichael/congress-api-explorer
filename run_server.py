#!/usr/bin/env python3
"""
Simple MCP server runner that can be used directly.
"""

import os
import sys
from pathlib import Path

# Set environment variables
os.environ.setdefault("CONGRESS_API_KEY", "kF6SxbPbbXXjOGDd2FIFaYUkZRuYfQN2OsQtnj9G")
os.environ.setdefault("CACHE_TYPE", "memory")
os.environ.setdefault("LOG_LEVEL", "INFO")

# Add src to path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir / "src"))

# Import and run the server
from scripts.run_mcp_server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())