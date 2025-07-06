#!/bin/bash
# Congress API Explorer MCP Server Startup Script

# Set the project directory
PROJECT_DIR="/Users/noelmcmichael/Workspace/congress_api_explorer"

# Change to project directory
cd "$PROJECT_DIR"

# Activate virtual environment
source .venv/bin/activate

# Set environment variables
export CONGRESS_API_KEY="kF6SxbPbbXXjOGDd2FIFaYUkZRuYfQN2OsQtnj9G"
export CACHE_TYPE="memory"
export LOG_LEVEL="INFO"

# Run the MCP server
python scripts/run_mcp_server.py