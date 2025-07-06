# Congress API Explorer - Memex Integration Guide

## 🚀 Quick Start Integration

### Option 1: Direct MCP Server Setup

1. **Start the MCP Server**
   ```bash
   cd /Users/noelmcmichael/Workspace/congress_api_explorer
   source .venv/bin/activate
   python scripts/run_mcp_server.py
   ```

2. **Connect from Memex**
   - The server runs on stdio transport
   - Use the congress-api-explorer server name
   - All 16 tools will be available

### Option 2: Using the Shell Script

1. **Make the script executable**
   ```bash
   chmod +x /Users/noelmcmichael/Workspace/congress_api_explorer/scripts/run_mcp_server.sh
   ```

2. **Run the script**
   ```bash
   /Users/noelmcmichael/Workspace/congress_api_explorer/scripts/run_mcp_server.sh
   ```

### Option 3: Using UV (Recommended)

1. **Direct UV command**
   ```bash
   cd /Users/noelmcmichael/Workspace/congress_api_explorer
   uv run scripts/run_mcp_server.py
   ```

## 🔧 Environment Configuration

### Required Environment Variables
```bash
export CONGRESS_API_KEY="kF6SxbPbbXXjOGDd2FIFaYUkZRuYfQN2OsQtnj9G"
export CACHE_TYPE="memory"
export LOG_LEVEL="INFO"
```

### Optional Configuration
```bash
export CACHE_TTL_DEFAULT=3600
export RATE_LIMIT_REQUESTS_PER_HOUR=4500
export RATE_LIMIT_REQUESTS_PER_MINUTE=75
```

## 📋 Available Tools (16 Total)

### Committee Tools
- `get_committees` - List congressional committees
- `get_committee_details` - Detailed committee information
- `get_committee_hearings` - Committee hearings and meetings

### Hearing Tools
- `get_hearings` - Congressional hearings
- `search_hearings` - Search hearings by content

### Bill Tools
- `get_bills` - Bills and resolutions
- `get_bill_details` - Detailed bill information
- `search_bills` - Search bills by content

### Member Tools
- `get_members` - Congressional members
- `get_member_details` - Detailed member information

### Utility Tools
- `get_congress_info` - Current Congress information
- `get_rate_limit_status` - API usage status

### Enhanced Search Tools
- `search_all` - Cross-type search across all data
- `search_by_topic` - Topic-based search (healthcare, economy, etc.)

### Health Monitoring Tools
- `get_health_status` - System health status
- `get_system_metrics` - Performance metrics

## 🧪 Testing the Integration

### Quick Test Commands

1. **Test basic functionality**
   ```bash
   cd /Users/noelmcmichael/Workspace/congress_api_explorer
   source .venv/bin/activate
   python test_mcp_connection.py
   ```

2. **Run comprehensive demo**
   ```bash
   python scripts/comprehensive_demo.py
   ```

3. **Test individual tools**
   ```bash
   python scripts/test_enhanced_mcp.py
   ```

## 🔍 Example Usage in Memex

Once integrated, you can ask questions like:

- "What committees is Alexandria Ocasio-Cortez on?"
- "Show me recent healthcare bills"
- "What's the current status of the Infrastructure Investment Act?"
- "Find all hearings on artificial intelligence"
- "Search for bipartisan climate legislation"
- "Get the health status of the Congress API system"

## 📊 Performance Monitoring

### Health Check
The system includes comprehensive health monitoring:
- System resource usage
- API connectivity status
- Rate limiting status
- Cache performance
- Configuration validation

### Rate Limiting
- Conservative usage: 4500 requests/hour (90% of API limit)
- Minute-level throttling: 75 requests/minute
- Automatic backoff and retry logic

## 🛠️ Troubleshooting

### Common Issues

1. **API Key Not Working**
   - Verify the API key is set correctly
   - Check if the key has proper permissions

2. **Server Not Starting**
   - Ensure virtual environment is activated
   - Check that all dependencies are installed
   - Verify Python path is correct

3. **Rate Limiting Errors**
   - Check current usage with `get_rate_limit_status`
   - Wait for rate limit window to reset
   - Verify rate limiting configuration

4. **Cache Issues**
   - Check cache configuration (memory vs Redis)
   - Verify cache TTL settings
   - Clear cache if needed

### Debug Commands

```bash
# Check system health
python -c "import asyncio; from src.congress_mcp.utils import health_checker; print(asyncio.run(health_checker.check_health()))"

# Test API connectivity
python -c "import asyncio; from src.congress_mcp.api import CongressAPIClient; client = CongressAPIClient(); print(asyncio.run(client.get_current_congress())); asyncio.run(client.close())"

# Check tools registration
python -c "import asyncio; from src.congress_mcp.mcp_server.tools import register_tools; print(f'Tools: {len(asyncio.run(register_tools()))}')"
```

## 🎯 Next Steps

1. **Start the MCP Server** using one of the methods above
2. **Connect from Memex** to the congress-api-explorer server
3. **Test basic functionality** with simple queries
4. **Explore advanced features** like cross-type search
5. **Monitor performance** using health check tools

## 📞 Support

If you encounter issues:
1. Check the logs in `congress_api_explorer.log`
2. Run the health check tools
3. Verify environment variables are set correctly
4. Test individual components using the debug commands

The system is production-ready and fully functional with comprehensive error handling and monitoring.