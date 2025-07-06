# 🚀 Start Congress API Explorer MCP Server

## Quick Start Commands

### Option 1: Simple Start (Recommended)
```bash
cd /Users/noelmcmichael/Workspace/congress_api_explorer
source .venv/bin/activate
export CONGRESS_API_KEY="kF6SxbPbbXXjOGDd2FIFaYUkZRuYfQN2OsQtnj9G"
python scripts/run_mcp_server.py
```

### Option 2: Using UV
```bash
cd /Users/noelmcmichael/Workspace/congress_api_explorer
export CONGRESS_API_KEY="kF6SxbPbbXXjOGDd2FIFaYUkZRuYfQN2OsQtnj9G"
uv run scripts/run_mcp_server.py
```

### Option 3: Using Shell Script
```bash
/Users/noelmcmichael/Workspace/congress_api_explorer/scripts/run_mcp_server.sh
```

## Server Details
- **Name**: congress-api-explorer
- **Transport**: stdio
- **Tools**: 16 available
- **Resources**: 20 available
- **Health Monitoring**: Included

## What You'll See
When the server starts successfully, you'll see:
```
2025-07-06 XX:XX:XX - congress_mcp - INFO - Starting Congress API MCP Server...
2025-07-06 XX:XX:XX - congress_mcp - INFO - Congress API MCP Server started successfully
```

The server will then wait for MCP protocol messages via stdin/stdout.

## Ready for Memex!
Once started, the server is ready to receive commands from Memex.