"""
MCP resources registration for Congress API Explorer.
"""

from typing import List
from mcp.types import Resource


async def register_resources() -> List[Resource]:
    """Register all available MCP resources."""
    
    resources = [
        # Committee resources
        Resource(
            uri="congress://committees/current",
            name="Current Congress Committees",
            description="List of all committees in the current Congress",
            mimeType="text/plain"
        ),
        
        Resource(
            uri="congress://committees/house",
            name="House Committees",
            description="List of House committees in the current Congress",
            mimeType="text/plain"
        ),
        
        Resource(
            uri="congress://committees/senate",
            name="Senate Committees",
            description="List of Senate committees in the current Congress",
            mimeType="text/plain"
        ),
        
        Resource(
            uri="congress://committees/joint",
            name="Joint Committees",
            description="List of joint committees in the current Congress",
            mimeType="text/plain"
        ),
        
        # Hearing resources
        Resource(
            uri="congress://hearings/recent",
            name="Recent Hearings",
            description="Recent congressional hearings across all committees",
            mimeType="text/plain"
        ),
        
        Resource(
            uri="congress://hearings/today",
            name="Today's Hearings",
            description="Hearings scheduled for today",
            mimeType="text/plain"
        ),
        
        Resource(
            uri="congress://hearings/upcoming",
            name="Upcoming Hearings",
            description="Upcoming hearings in the next 30 days",
            mimeType="text/plain"
        ),
        
        # Bill resources
        Resource(
            uri="congress://bills/recent",
            name="Recent Bills",
            description="Recently introduced bills and resolutions",
            mimeType="text/plain"
        ),
        
        Resource(
            uri="congress://bills/enacted",
            name="Recently Enacted Bills",
            description="Bills recently enacted into law",
            mimeType="text/plain"
        ),
        
        Resource(
            uri="congress://bills/house",
            name="House Bills",
            description="Recent House bills and resolutions",
            mimeType="text/plain"
        ),
        
        Resource(
            uri="congress://bills/senate",
            name="Senate Bills",
            description="Recent Senate bills and resolutions",
            mimeType="text/plain"
        ),
        
        # Member resources
        Resource(
            uri="congress://members/house",
            name="House Members",
            description="Current House of Representatives members",
            mimeType="text/plain"
        ),
        
        Resource(
            uri="congress://members/senate",
            name="Senate Members",
            description="Current Senate members",
            mimeType="text/plain"
        ),
        
        Resource(
            uri="congress://members/leadership",
            name="Congressional Leadership",
            description="Current congressional leadership positions",
            mimeType="text/plain"
        ),
        
        # Status and info resources
        Resource(
            uri="congress://status/api",
            name="API Status",
            description="Current API rate limits and status",
            mimeType="text/plain"
        ),
        
        Resource(
            uri="congress://status/congress",
            name="Congress Information",
            description="Information about the current Congress",
            mimeType="text/plain"
        ),
        
        # Documentation resources
        Resource(
            uri="congress://docs/tools",
            name="Available Tools",
            description="Documentation of all available MCP tools",
            mimeType="text/markdown"
        ),
        
        Resource(
            uri="congress://docs/examples",
            name="Usage Examples",
            description="Examples of how to use the Congress API tools",
            mimeType="text/markdown"
        ),
        
        # Data export resources
        Resource(
            uri="congress://export/committees",
            name="Committee Data Export",
            description="Structured export of committee data",
            mimeType="application/json"
        ),
        
        Resource(
            uri="congress://export/hearings",
            name="Hearing Data Export",
            description="Structured export of hearing data",
            mimeType="application/json"
        ),
    ]
    
    return resources