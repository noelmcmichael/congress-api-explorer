# Congress API Explorer with MCP Integration

## Project Overview

This project explores the US Congress API (api.congress.gov) using Model Context Protocol (MCP) integration, focusing on committee hearings tracking and analysis. The primary goal is to create an intelligent congressional data access system that integrates with Memex as an MCP client.

## Architecture

### Project Structure
```
congress_api_explorer/
├── src/congress_mcp/
│   ├── api/                 # Congress API client + caching
│   ├── mcp_server/         # MCP protocol implementation
│   ├── utils/              # Config, logging, helpers
│   └── tests/              # Test suite
├── docs/                   # Documentation
├── examples/               # Usage examples
├── scripts/                # Utility scripts
└── .memex/                 # Development guidelines
```

### Key Components

1. **Congress API Client**: Handles API requests with rate limiting (5000/day limit)
2. **Smart Caching**: Multi-layer caching with different TTLs:
   - Committee data: 24 hours
   - Hearing schedules: 6 hours
   - Bill status: 2 hours
   - Member info: 7 days
3. **MCP Server**: Implements protocol for AI tool integration
4. **Committee Focus**: Prioritizes hearing data and committee information

## Technical Stack

- **Language**: Python 3.10+
- **Data Models**: Pydantic for type safety
- **API Client**: Async HTTP with retry logic
- **MCP**: Official Python SDK
- **Caching**: Redis-compatible (configurable)
- **Development**: Git version control, comprehensive testing

## Progress Tracker

### ✅ Step 1: Project Foundation
- [x] Created project structure
- [x] Initialized Git repository
- [x] Set up README with architecture overview
- [x] Established development guidelines

### ✅ Step 2: API Client Implementation (Complete)
- [x] Congress API client with rate limiting
- [x] Caching layer implementation (Memory + Redis support)
- [x] Error handling and retry logic
- [x] Configuration management
- [x] Rate limiter with hour/minute windows
- [x] Async HTTP client with proper session management
- [x] Tested with real API - successfully fetching committees and hearings

### ✅ Step 3: Data Models (Complete)
- [x] Pydantic models for API responses
- [x] Committee data structures with parent/subcommittee relationships
- [x] Hearing and meeting models with witness/document support
- [x] Bill and member models with comprehensive data fields
- [x] Type-safe models with validation and helper methods
- [x] Support for nested API response structures
- [x] Tested with real API data - all models parsing successfully

### ✅ Step 4: MCP Server (Complete)
- [x] Basic MCP server implementation with async support
- [x] Essential tools and resources (12 tools, 20 resources)
- [x] Protocol compliance with MCP specification
- [x] Error handling and proper response formatting
- [x] Comprehensive tool suite for committees, hearings, bills, members
- [x] Resource-based access to congressional data
- [x] Rate limit monitoring and status reporting
- [x] Tested successfully - all tools and resources working

### 🔄 Step 5: Committee Hearings Features (In Progress)
- [ ] Committee-specific tools
- [ ] Hearing tracking capabilities
- [ ] Witness and document access
- [ ] Related bill connections

### 📋 Step 6: Integration Testing (Planned)
- [ ] MCP client testing
- [ ] API integration tests
- [ ] Performance optimization
- [ ] Rate limit validation

## Configuration

### Environment Variables
- `CONGRESS_API_KEY`: API key for Congress API access
- `CACHE_TYPE`: Caching backend (redis/memory)
- `CACHE_TTL`: Default cache time-to-live
- `LOG_LEVEL`: Logging verbosity

## API Rate Limits

- **Congress API**: 5000 requests/hour, 250 max results per request
- **Strategy**: Smart caching and request prioritization
- **Monitoring**: Track usage to stay well under limits

## Getting Started

1. **Install Dependencies**:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

2. **Set API Key**:
   ```bash
   export CONGRESS_API_KEY="your-api-key-here"
   ```

3. **Run MCP Server**:
   ```bash
   python scripts/run_mcp_server.py
   ```

4. **Test API Client**:
   ```bash
   python scripts/test_api_client.py
   ```

## MCP Tools Available

### Committee Tools
- `get_committees` - List congressional committees with filtering
- `get_committee_details` - Detailed committee information
- `get_committee_hearings` - Committee hearings and meetings

### Hearing Tools  
- `get_hearings` - Congressional hearings across committees
- `search_hearings` - Search hearings by title/content

### Bill Tools
- `get_bills` - Bills and resolutions with filtering
- `get_bill_details` - Detailed bill information with actions
- `search_bills` - Search bills by title/content

### Member Tools
- `get_members` - Congressional members with filtering
- `get_member_details` - Detailed member information

### Utility Tools
- `get_congress_info` - Current Congress information
- `get_rate_limit_status` - API usage and rate limits

## MCP Resources Available

20+ resources including current committees, recent hearings, bills by chamber, member listings, and real-time status information.

## Development Guidelines

See `.memex/rules.md` for detailed development practices and coding standards.

## Contributing

This project follows conventional commit messages and maintains comprehensive test coverage.

## License

MIT License - see LICENSE file for details.