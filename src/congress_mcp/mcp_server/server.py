"""
Main MCP server implementation for Congress API Explorer.
"""

import asyncio
from typing import Any, List, Optional, Dict
from contextlib import asynccontextmanager

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    CallToolResult, 
    ListResourcesResult, 
    ListToolsResult, 
    ReadResourceResult,
    TextContent,
    Tool,
    Resource
)

from ..api import CongressAPIClient, CongressAPIError, CongressSearchEngine
from ..utils import logger, settings
from .tools import register_tools
from .resources import register_resources


class CongressMCPServer:
    """Congress API MCP Server implementation."""
    
    def __init__(self):
        self.server = Server("congress-api-explorer")
        self.client: Optional[CongressAPIClient] = None
        self.search_engine: Optional[CongressSearchEngine] = None
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up MCP server handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """List available tools."""
            tools = await register_tools()
            logger.debug(f"Listed {len(tools)} tools")
            return ListToolsResult(tools=tools)
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Optional[Dict[str, Any]] = None) -> CallToolResult:
            """Handle tool calls."""
            try:
                logger.info(f"Tool called: {name} with args: {arguments}")
                
                # Ensure client is available
                if not self.client:
                    self.client = CongressAPIClient()
                    self.search_engine = CongressSearchEngine(self.client)
                
                # Route tool calls to appropriate handlers
                result = await self._call_tool(name, arguments or {})
                
                logger.debug(f"Tool {name} completed successfully")
                return CallToolResult(
                    content=[TextContent(type="text", text=result)]
                )
                
            except Exception as e:
                error_msg = f"Error calling tool {name}: {str(e)}"
                logger.error(error_msg)
                return CallToolResult(
                    content=[TextContent(type="text", text=error_msg)],
                    isError=True
                )
        
        @self.server.list_resources()
        async def handle_list_resources() -> ListResourcesResult:
            """List available resources."""
            resources = await register_resources()
            logger.debug(f"Listed {len(resources)} resources")
            return ListResourcesResult(resources=resources)
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> ReadResourceResult:
            """Handle resource reading."""
            try:
                logger.info(f"Resource requested: {uri}")
                
                # Ensure client is available
                if not self.client:
                    self.client = CongressAPIClient()
                    self.search_engine = CongressSearchEngine(self.client)
                
                # Route resource reads to appropriate handlers
                content = await self._read_resource(uri)
                
                logger.debug(f"Resource {uri} read successfully")
                return ReadResourceResult(
                    contents=[TextContent(type="text", text=content)]
                )
                
            except Exception as e:
                error_msg = f"Error reading resource {uri}: {str(e)}"
                logger.error(error_msg)
                return ReadResourceResult(
                    contents=[TextContent(type="text", text=error_msg)]
                )
    
    async def _call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """Route tool calls to appropriate handlers."""
        
        # Committee tools
        if name == "get_committees":
            return await self._get_committees(**arguments)
        elif name == "get_committee_details":
            return await self._get_committee_details(**arguments)
        elif name == "get_committee_hearings":
            return await self._get_committee_hearings(**arguments)
        
        # Hearing tools
        elif name == "get_hearings":
            return await self._get_hearings(**arguments)
        elif name == "search_hearings":
            return await self._search_hearings(**arguments)
        
        # Bill tools
        elif name == "get_bills":
            return await self._get_bills(**arguments)
        elif name == "get_bill_details":
            return await self._get_bill_details(**arguments)
        elif name == "search_bills":
            return await self._search_bills(**arguments)
        
        # Member tools
        elif name == "get_members":
            return await self._get_members(**arguments)
        elif name == "get_member_details":
            return await self._get_member_details(**arguments)
        
        # Utility tools
        elif name == "get_congress_info":
            return await self._get_congress_info(**arguments)
        elif name == "get_rate_limit_status":
            return await self._get_rate_limit_status(**arguments)
        
        # Enhanced search tools
        elif name == "search_all":
            return await self._search_all(**arguments)
        elif name == "search_by_topic":
            return await self._search_by_topic(**arguments)
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    async def _read_resource(self, uri: str) -> str:
        """Route resource reads to appropriate handlers."""
        
        # Parse URI to determine resource type (expect congress://type/subtype format)
        if not uri.startswith("congress://"):
            raise ValueError(f"Invalid resource URI scheme: {uri}")
        
        # Remove scheme and split
        path = uri[11:]  # Remove "congress://"
        parts = path.split("/")
        
        if len(parts) < 1:
            raise ValueError(f"Invalid resource URI: {uri}")
        
        resource_type = parts[0]
        
        if resource_type == "committees":
            return await self._read_committees_resource(parts)
        elif resource_type == "hearings":
            return await self._read_hearings_resource(parts)
        elif resource_type == "bills":
            return await self._read_bills_resource(parts)
        elif resource_type == "members":
            return await self._read_members_resource(parts)
        elif resource_type == "status":
            return await self._read_status_resource(parts)
        else:
            raise ValueError(f"Unknown resource type: {resource_type}")
    
    # Committee tool implementations
    
    async def _get_committees(
        self, 
        congress: Optional[int] = None, 
        chamber: Optional[str] = None,
        limit: int = 20
    ) -> str:
        """Get committees."""
        data = await self.client.get_committees(
            congress=congress,
            chamber=chamber,
            limit=limit
        )
        
        committees = data.get("committees", [])
        
        result = f"Found {len(committees)} committees:\\n\\n"
        
        for committee in committees:
            name = committee.get("name", "Unknown")
            chamber_name = committee.get("chamber", "Unknown")
            system_code = committee.get("systemCode", "Unknown")
            result += f"• {name} ({chamber_name})\\n"
            result += f"  System Code: {system_code}\\n\\n"
        
        return result
    
    async def _get_committee_details(self, system_code: str) -> str:
        """Get committee details."""
        # This would need to be implemented with specific committee endpoint
        return f"Committee details for {system_code} (endpoint implementation needed)"
    
    async def _get_committee_hearings(
        self,
        congress: Optional[int] = None,
        chamber: Optional[str] = None,
        committee: Optional[str] = None,
        limit: int = 10
    ) -> str:
        """Get committee hearings."""
        data = await self.client.get_committee_hearings(
            congress=congress,
            chamber=chamber,
            committee=committee,
            limit=limit
        )
        
        hearings = data.get("hearings", [])
        
        result = f"Found {len(hearings)} hearings:\\n\\n"
        
        for hearing in hearings:
            title = hearing.get("title", "Unknown")
            date = hearing.get("date", "Unknown")
            chamber_name = hearing.get("chamber", "Unknown")
            result += f"• {title}\\n"
            result += f"  Date: {date}\\n"
            result += f"  Chamber: {chamber_name}\\n\\n"
        
        return result
    
    # Hearing tool implementations
    
    async def _get_hearings(
        self,
        congress: Optional[int] = None,
        chamber: Optional[str] = None,
        limit: int = 10
    ) -> str:
        """Get hearings."""
        data = await self.client.get_committee_hearings(
            congress=congress,
            chamber=chamber,
            limit=limit
        )
        
        hearings = data.get("hearings", [])
        
        result = f"Found {len(hearings)} hearings:\\n\\n"
        
        for hearing in hearings:
            title = hearing.get("title", "Unknown")
            date = hearing.get("date", "Unknown")
            committee_name = hearing.get("committee", {}).get("name", "Unknown")
            result += f"• {title}\\n"
            result += f"  Date: {date}\\n"
            result += f"  Committee: {committee_name}\\n\\n"
        
        return result
    
    async def _search_hearings(self, query: str, limit: int = 10) -> str:
        """Search hearings by title/content."""
        # This would implement search functionality
        return f"Search results for '{query}' (search implementation needed)"
    
    # Bill tool implementations
    
    async def _get_bills(
        self,
        congress: Optional[int] = None,
        bill_type: Optional[str] = None,
        limit: int = 10
    ) -> str:
        """Get bills."""
        data = await self.client.get_bills(
            congress=congress,
            bill_type=bill_type,
            limit=limit
        )
        
        bills = data.get("bills", [])
        
        result = f"Found {len(bills)} bills:\\n\\n"
        
        for bill in bills:
            bill_type = bill.get("type", "Unknown")
            number = bill.get("number", "Unknown")
            title = bill.get("title", "Unknown")
            latest_action = bill.get("latestAction", {}).get("text", "Unknown")
            
            result += f"• {bill_type} {number}: {title}\\n"
            result += f"  Latest Action: {latest_action}\\n\\n"
        
        return result
    
    async def _get_bill_details(self, congress: int, bill_type: str, bill_number: int) -> str:
        """Get bill details."""
        data = await self.client.get_bill_details(congress, bill_type, bill_number)
        
        bill = data.get("bill", {})
        title = bill.get("title", "Unknown")
        sponsor = bill.get("sponsors", [{}])[0].get("fullName", "Unknown") if bill.get("sponsors") else "Unknown"
        latest_action = bill.get("latestAction", {}).get("text", "Unknown")
        
        result = f"Bill Details: {bill_type} {bill_number}\\n\\n"
        result += f"Title: {title}\\n"
        result += f"Sponsor: {sponsor}\\n"
        result += f"Latest Action: {latest_action}\\n"
        
        return result
    
    async def _search_bills(self, query: str, limit: int = 10) -> str:
        """Search bills by title/content."""
        # This would implement search functionality
        return f"Search results for '{query}' (search implementation needed)"
    
    # Member tool implementations
    
    async def _get_members(
        self,
        congress: Optional[int] = None,
        chamber: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 10
    ) -> str:
        """Get members."""
        data = await self.client.get_members(
            congress=congress,
            chamber=chamber,
            state=state,
            limit=limit
        )
        
        members = data.get("members", [])
        
        result = f"Found {len(members)} members:\\n\\n"
        
        for member in members:
            name = member.get("name", "Unknown")
            state = member.get("state", "Unknown")
            party = member.get("party", "Unknown")
            district = member.get("district", "At Large")
            
            result += f"• {name} ({party})\\n"
            result += f"  State: {state}, District: {district}\\n\\n"
        
        return result
    
    async def _get_member_details(self, bioguide_id: str) -> str:
        """Get member details."""
        # This would need to be implemented with specific member endpoint
        return f"Member details for {bioguide_id} (endpoint implementation needed)"
    
    # Utility tool implementations
    
    async def _get_congress_info(self) -> str:
        """Get current Congress information."""
        current_congress = await self.client.get_current_congress()
        
        result = f"Current Congress Information:\\n\\n"
        result += f"Congress Number: {current_congress}\\n"
        result += f"Years: {2023 + (current_congress - 118) * 2}-{2024 + (current_congress - 118) * 2}\\n"
        
        return result
    
    async def _get_rate_limit_status(self) -> str:
        """Get rate limit status."""
        status = self.client.get_rate_limit_status()
        
        result = "Rate Limit Status:\\n\\n"
        
        for window, info in status.items():
            result += f"{window.title()} Window:\\n"
            result += f"  Used: {info['used']}/{info['limit']}\\n"
            result += f"  Remaining: {info['remaining']}\\n"
            result += f"  Reset in: {info['reset_in']} seconds\\n\\n"
        
        return result
    
    # Enhanced search tool implementations
    
    async def _search_all(
        self,
        query: str,
        limit: int = 20,
        include_types: Optional[List[str]] = None
    ) -> str:
        """Search across all Congress data types."""
        results = await self.search_engine.search_all(
            query=query,
            limit=limit,
            include_types=include_types
        )
        
        if not results:
            return f"No results found for '{query}'"
        
        result = f"Search Results for '{query}' ({len(results)} found):\\n\\n"
        
        for item in results:
            result += f"• {item.title} ({item.item_type})\\n"
            result += f"  {item.description}\\n"
            if item.chamber:
                result += f"  Chamber: {item.chamber}\\n"
            result += f"  Relevance: {item.relevance_score:.1f}\\n\\n"
        
        return result
    
    async def _search_by_topic(
        self,
        topic: str,
        item_types: Optional[List[str]] = None,
        limit: int = 20
    ) -> str:
        """Search for congressional items by topic."""
        results = await self.search_engine.search_by_topic(
            topic=topic,
            item_types=item_types,
            limit=limit
        )
        
        if not results:
            return f"No results found for topic '{topic}'"
        
        result = f"Topic Search Results for '{topic}' ({len(results)} found):\\n\\n"
        
        for item in results:
            result += f"• {item.title} ({item.item_type})\\n"
            result += f"  {item.description}\\n"
            if item.chamber:
                result += f"  Chamber: {item.chamber}\\n"
            result += f"  Relevance: {item.relevance_score:.1f}\\n\\n"
        
        return result
    
    # Resource implementations
    
    async def _read_committees_resource(self, parts: List[str]) -> str:
        """Read committees resource."""
        return "Committees resource (implementation needed)"
    
    async def _read_hearings_resource(self, parts: List[str]) -> str:
        """Read hearings resource."""
        return "Hearings resource (implementation needed)"
    
    async def _read_bills_resource(self, parts: List[str]) -> str:
        """Read bills resource."""
        return "Bills resource (implementation needed)"
    
    async def _read_members_resource(self, parts: List[str]) -> str:
        """Read members resource."""
        return "Members resource (implementation needed)"
    
    async def _read_status_resource(self, parts: List[str]) -> str:
        """Read status resource."""
        rate_status = self.client.get_rate_limit_status() if self.client else {}
        return f"Congress API Explorer Status:\\n\\nRate Limits: {rate_status}"
    
    @asynccontextmanager
    async def serve(self, transport):
        """Serve the MCP server."""
        logger.info("Starting Congress API MCP Server...")
        
        try:
            # Initialize client
            self.client = CongressAPIClient()
            self.search_engine = CongressSearchEngine(self.client)
            
            # Start server
            async with self.server.run(
                transport, 
                InitializationOptions(
                    server_name="congress-api-explorer",
                    server_version="0.1.0"
                )
            ):
                logger.info("Congress API MCP Server started successfully")
                yield
                
        finally:
            # Cleanup
            if self.client:
                await self.client.close()
                self.client = None
            logger.info("Congress API MCP Server stopped")


# Create server instance
congress_server = CongressMCPServer()