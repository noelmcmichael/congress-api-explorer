"""
MCP tools registration for Congress API Explorer.
"""

from typing import List, Dict, Any
from mcp.types import Tool


async def register_tools() -> List[Tool]:
    """Register all available MCP tools."""
    
    tools = [
        # Committee tools
        Tool(
            name="get_committees",
            description="Get list of congressional committees",
            inputSchema={
                "type": "object",
                "properties": {
                    "congress": {
                        "type": "integer",
                        "description": "Congress number (e.g., 118 for current)",
                        "minimum": 1
                    },
                    "chamber": {
                        "type": "string",
                        "enum": ["house", "senate", "joint"],
                        "description": "Chamber type"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "minimum": 1,
                        "maximum": 250,
                        "default": 20
                    }
                },
                "additionalProperties": False
            }
        ),
        
        Tool(
            name="get_committee_details",
            description="Get detailed information about a specific committee",
            inputSchema={
                "type": "object",
                "properties": {
                    "system_code": {
                        "type": "string",
                        "description": "Committee system code (e.g., 'hsif00')",
                        "pattern": "^[a-z]{2}[a-z0-9]{2}[0-9]{2}$"
                    }
                },
                "required": ["system_code"],
                "additionalProperties": False
            }
        ),
        
        Tool(
            name="get_committee_hearings",
            description="Get hearings for committees",
            inputSchema={
                "type": "object",
                "properties": {
                    "congress": {
                        "type": "integer",
                        "description": "Congress number",
                        "minimum": 1
                    },
                    "chamber": {
                        "type": "string",
                        "enum": ["house", "senate", "joint"],
                        "description": "Chamber type"
                    },
                    "committee": {
                        "type": "string",
                        "description": "Committee system code"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "minimum": 1,
                        "maximum": 250,
                        "default": 10
                    }
                },
                "additionalProperties": False
            }
        ),
        
        # Hearing tools
        Tool(
            name="get_hearings",
            description="Get congressional hearings",
            inputSchema={
                "type": "object",
                "properties": {
                    "congress": {
                        "type": "integer",
                        "description": "Congress number",
                        "minimum": 1
                    },
                    "chamber": {
                        "type": "string",
                        "enum": ["house", "senate", "joint"],
                        "description": "Chamber type"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "minimum": 1,
                        "maximum": 250,
                        "default": 10
                    }
                },
                "additionalProperties": False
            }
        ),
        
        Tool(
            name="search_hearings",
            description="Search hearings by title or content",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                        "minLength": 1
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "minimum": 1,
                        "maximum": 50,
                        "default": 10
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        ),
        
        # Bill tools
        Tool(
            name="get_bills",
            description="Get congressional bills and resolutions",
            inputSchema={
                "type": "object",
                "properties": {
                    "congress": {
                        "type": "integer",
                        "description": "Congress number",
                        "minimum": 1
                    },
                    "bill_type": {
                        "type": "string",
                        "enum": ["hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", "sres"],
                        "description": "Type of bill or resolution"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "minimum": 1,
                        "maximum": 250,
                        "default": 10
                    }
                },
                "additionalProperties": False
            }
        ),
        
        Tool(
            name="get_bill_details",
            description="Get detailed information about a specific bill",
            inputSchema={
                "type": "object",
                "properties": {
                    "congress": {
                        "type": "integer",
                        "description": "Congress number",
                        "minimum": 1
                    },
                    "bill_type": {
                        "type": "string",
                        "enum": ["hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", "sres"],
                        "description": "Type of bill or resolution"
                    },
                    "bill_number": {
                        "type": "integer",
                        "description": "Bill number",
                        "minimum": 1
                    }
                },
                "required": ["congress", "bill_type", "bill_number"],
                "additionalProperties": False
            }
        ),
        
        Tool(
            name="search_bills",
            description="Search bills by title or content",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                        "minLength": 1
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "minimum": 1,
                        "maximum": 50,
                        "default": 10
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        ),
        
        # Member tools
        Tool(
            name="get_members",
            description="Get congressional members",
            inputSchema={
                "type": "object",
                "properties": {
                    "congress": {
                        "type": "integer",
                        "description": "Congress number",
                        "minimum": 1
                    },
                    "chamber": {
                        "type": "string",
                        "enum": ["house", "senate"],
                        "description": "Chamber type"
                    },
                    "state": {
                        "type": "string",
                        "description": "State abbreviation (e.g., 'CA', 'NY')",
                        "pattern": "^[A-Z]{2}$"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "minimum": 1,
                        "maximum": 250,
                        "default": 10
                    }
                },
                "additionalProperties": False
            }
        ),
        
        Tool(
            name="get_member_details",
            description="Get detailed information about a specific member",
            inputSchema={
                "type": "object",
                "properties": {
                    "bioguide_id": {
                        "type": "string",
                        "description": "Member's bioguide ID",
                        "pattern": "^[A-Z][0-9]{6}$"
                    }
                },
                "required": ["bioguide_id"],
                "additionalProperties": False
            }
        ),
        
        # Utility tools
        Tool(
            name="get_congress_info",
            description="Get information about current Congress",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        ),
        
        Tool(
            name="get_rate_limit_status",
            description="Get current API rate limit status",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        ),
        
        # Enhanced search tools
        Tool(
            name="search_all",
            description="Search across all Congress data types (bills, hearings, committees, members)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                        "minLength": 1
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "minimum": 1,
                        "maximum": 50,
                        "default": 20
                    },
                    "include_types": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["bill", "hearing", "committee", "member"]
                        },
                        "description": "Types to include in search",
                        "default": ["bill", "hearing", "committee", "member"]
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        ),
        
        Tool(
            name="search_by_topic",
            description="Search for congressional items by topic (healthcare, economy, defense, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Topic to search for",
                        "enum": ["healthcare", "economy", "defense", "education", "environment", "immigration", "technology", "transportation"]
                    },
                    "item_types": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["bill", "hearing", "committee", "member"]
                        },
                        "description": "Types to include in search",
                        "default": ["bill", "hearing"]
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "minimum": 1,
                        "maximum": 50,
                        "default": 20
                    }
                },
                "required": ["topic"],
                "additionalProperties": False
            }
        ),
        
        # Health and monitoring tools
        Tool(
            name="get_health_status",
            description="Get comprehensive system health status",
            inputSchema={
                "type": "object",
                "properties": {
                    "force_refresh": {
                        "type": "boolean",
                        "description": "Force refresh of cached health status",
                        "default": False
                    }
                },
                "additionalProperties": False
            }
        ),
        
        Tool(
            name="get_system_metrics",
            description="Get system performance metrics and uptime",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        )
    ]
    
    return tools