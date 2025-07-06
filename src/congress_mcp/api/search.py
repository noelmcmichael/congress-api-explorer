"""
Enhanced search capabilities for Congress API Explorer.
"""

import asyncio
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from ..utils.logging import logger
from .client import CongressAPIClient


@dataclass
class SearchResult:
    """Represents a search result with metadata."""
    
    item_type: str  # 'bill', 'hearing', 'committee', 'member'
    title: str
    description: str
    url: str = ""
    date: Optional[datetime] = None
    chamber: Optional[str] = None
    congress: Optional[int] = None
    relevance_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class CongressSearchEngine:
    """
    Enhanced search engine for Congress API data.
    """
    
    def __init__(self, client: CongressAPIClient):
        self.client = client
    
    async def search_all(
        self,
        query: str,
        limit: int = 20,
        include_types: Optional[List[str]] = None
    ) -> List[SearchResult]:
        """
        Search across all Congress data types.
        
        Args:
            query: Search query
            limit: Maximum number of results
            include_types: Types to include ('bill', 'hearing', 'committee', 'member')
            
        Returns:
            List of search results sorted by relevance
        """
        if include_types is None:
            include_types = ['bill', 'hearing', 'committee', 'member']
        
        logger.info(f"Searching for '{query}' across types: {include_types}")
        
        # Execute searches concurrently
        tasks = []
        
        if 'bill' in include_types:
            tasks.append(self._search_bills(query, limit // 4))
        if 'hearing' in include_types:
            tasks.append(self._search_hearings(query, limit // 4))
        if 'committee' in include_types:
            tasks.append(self._search_committees(query, limit // 4))
        if 'member' in include_types:
            tasks.append(self._search_members(query, limit // 4))
        
        # Wait for all searches to complete
        results = await asyncio.gather(*tasks)
        
        # Combine and sort results
        combined_results = []
        for result_list in results:
            combined_results.extend(result_list)
        
        # Sort by relevance score (descending)
        combined_results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        logger.info(f"Found {len(combined_results)} total results")
        return combined_results[:limit]
    
    async def _search_bills(
        self,
        query: str,
        limit: int = 10
    ) -> List[SearchResult]:
        """Search bills by title and content."""
        try:
            current_congress = await self.client.get_current_congress()
            
            # Get recent bills
            data = await self.client.get_bills(
                congress=current_congress,
                limit=limit * 2  # Get more to filter
            )
            
            bills = data.get("bills", [])
            results = []
            
            query_lower = query.lower()
            
            for bill in bills:
                title = bill.get("title", "")
                bill_type = bill.get("type", "")
                number = bill.get("number", "")
                latest_action = bill.get("latestAction", {}).get("text", "")
                
                # Calculate relevance score
                relevance = 0.0
                if query_lower in title.lower():
                    relevance += 2.0
                if query_lower in latest_action.lower():
                    relevance += 1.0
                
                # Add partial matches
                query_words = query_lower.split()
                for word in query_words:
                    if word in title.lower():
                        relevance += 0.5
                    if word in latest_action.lower():
                        relevance += 0.3
                
                if relevance > 0:
                    result = SearchResult(
                        item_type="bill",
                        title=f"{bill_type} {number}: {title}",
                        description=latest_action,
                        chamber=bill.get("chamber", ""),
                        congress=current_congress,
                        relevance_score=relevance,
                        metadata={
                            "bill_type": bill_type,
                            "number": number,
                            "congress": current_congress,
                            "latest_action": latest_action
                        }
                    )
                    results.append(result)
            
            # Sort by relevance and return top results
            results.sort(key=lambda x: x.relevance_score, reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Error searching bills: {e}")
            return []
    
    async def _search_hearings(
        self,
        query: str,
        limit: int = 10
    ) -> List[SearchResult]:
        """Search hearings by title and content."""
        try:
            current_congress = await self.client.get_current_congress()
            
            # Get recent hearings
            data = await self.client.get_committee_hearings(
                congress=current_congress,
                limit=limit * 2  # Get more to filter
            )
            
            hearings = data.get("hearings", [])
            results = []
            
            query_lower = query.lower()
            
            for hearing in hearings:
                title = hearing.get("title", "")
                chamber = hearing.get("chamber", "")
                committee_name = hearing.get("committee", {}).get("name", "")
                date_str = hearing.get("date", "")
                
                # Calculate relevance score
                relevance = 0.0
                if query_lower in title.lower():
                    relevance += 2.0
                if query_lower in committee_name.lower():
                    relevance += 1.5
                
                # Add partial matches
                query_words = query_lower.split()
                for word in query_words:
                    if word in title.lower():
                        relevance += 0.5
                    if word in committee_name.lower():
                        relevance += 0.3
                
                if relevance > 0:
                    result = SearchResult(
                        item_type="hearing",
                        title=title,
                        description=f"Committee: {committee_name}",
                        chamber=chamber,
                        congress=current_congress,
                        relevance_score=relevance,
                        metadata={
                            "committee": committee_name,
                            "date": date_str,
                            "congress": current_congress
                        }
                    )
                    results.append(result)
            
            # Sort by relevance and return top results
            results.sort(key=lambda x: x.relevance_score, reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Error searching hearings: {e}")
            return []
    
    async def _search_committees(
        self,
        query: str,
        limit: int = 10
    ) -> List[SearchResult]:
        """Search committees by name and code."""
        try:
            current_congress = await self.client.get_current_congress()
            
            # Get committees
            data = await self.client.get_committees(
                congress=current_congress,
                limit=limit * 2  # Get more to filter
            )
            
            committees = data.get("committees", [])
            results = []
            
            query_lower = query.lower()
            
            for committee in committees:
                name = committee.get("name", "")
                chamber = committee.get("chamber", "")
                system_code = committee.get("systemCode", "")
                
                # Calculate relevance score
                relevance = 0.0
                if query_lower in name.lower():
                    relevance += 2.0
                if query_lower in system_code.lower():
                    relevance += 1.0
                
                # Add partial matches
                query_words = query_lower.split()
                for word in query_words:
                    if word in name.lower():
                        relevance += 0.5
                
                if relevance > 0:
                    result = SearchResult(
                        item_type="committee",
                        title=name,
                        description=f"{chamber} Committee",
                        chamber=chamber,
                        congress=current_congress,
                        relevance_score=relevance,
                        metadata={
                            "system_code": system_code,
                            "congress": current_congress
                        }
                    )
                    results.append(result)
            
            # Sort by relevance and return top results
            results.sort(key=lambda x: x.relevance_score, reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Error searching committees: {e}")
            return []
    
    async def _search_members(
        self,
        query: str,
        limit: int = 10
    ) -> List[SearchResult]:
        """Search members by name and state."""
        try:
            current_congress = await self.client.get_current_congress()
            
            # Get members
            data = await self.client.get_members(
                congress=current_congress,
                limit=limit * 2  # Get more to filter
            )
            
            members = data.get("members", [])
            results = []
            
            query_lower = query.lower()
            
            for member in members:
                name = member.get("name", "")
                state = member.get("state", "")
                party = member.get("party", "")
                district = member.get("district", "")
                
                # Calculate relevance score
                relevance = 0.0
                if query_lower in name.lower():
                    relevance += 2.0
                if query_lower in state.lower():
                    relevance += 1.0
                if query_lower in party.lower():
                    relevance += 0.5
                
                # Add partial matches
                query_words = query_lower.split()
                for word in query_words:
                    if word in name.lower():
                        relevance += 0.5
                    if word in state.lower():
                        relevance += 0.3
                
                if relevance > 0:
                    district_text = f", District {district}" if district else ""
                    result = SearchResult(
                        item_type="member",
                        title=name,
                        description=f"{party} - {state}{district_text}",
                        congress=current_congress,
                        relevance_score=relevance,
                        metadata={
                            "state": state,
                            "party": party,
                            "district": district,
                            "congress": current_congress
                        }
                    )
                    results.append(result)
            
            # Sort by relevance and return top results
            results.sort(key=lambda x: x.relevance_score, reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Error searching members: {e}")
            return []
    
    async def search_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        item_types: Optional[List[str]] = None,
        limit: int = 20
    ) -> List[SearchResult]:
        """
        Search for items within a date range.
        
        Args:
            start_date: Start date
            end_date: End date
            item_types: Types to include
            limit: Maximum number of results
            
        Returns:
            List of search results
        """
        if item_types is None:
            item_types = ['bill', 'hearing']
        
        logger.info(f"Searching by date range: {start_date} to {end_date}")
        
        # For now, implement basic date filtering
        # In a real implementation, you'd use API date parameters
        results = []
        
        # This is a simplified implementation
        # The actual Congress API may have specific date filtering capabilities
        
        return results
    
    async def search_by_topic(
        self,
        topic: str,
        item_types: Optional[List[str]] = None,
        limit: int = 20
    ) -> List[SearchResult]:
        """
        Search for items by topic/subject.
        
        Args:
            topic: Topic to search for
            item_types: Types to include
            limit: Maximum number of results
            
        Returns:
            List of search results
        """
        # Map common topics to search terms
        topic_mapping = {
            "healthcare": ["health", "medicare", "medicaid", "affordable care"],
            "economy": ["economic", "budget", "tax", "finance", "trade"],
            "defense": ["defense", "military", "national security", "veterans"],
            "education": ["education", "school", "student", "college"],
            "environment": ["climate", "environment", "energy", "renewable"],
            "immigration": ["immigration", "border", "visa", "refugee"],
            "technology": ["technology", "cyber", "internet", "digital"],
            "transportation": ["transportation", "infrastructure", "highway", "transit"]
        }
        
        # Use mapped terms or the topic itself
        search_terms = topic_mapping.get(topic.lower(), [topic])
        
        # Search for each term and combine results
        all_results = []
        
        for term in search_terms:
            term_results = await self.search_all(
                query=term,
                limit=limit // len(search_terms),
                include_types=item_types
            )
            all_results.extend(term_results)
        
        # Remove duplicates and sort by relevance
        unique_results = []
        seen_titles = set()
        
        for result in all_results:
            if result.title not in seen_titles:
                seen_titles.add(result.title)
                unique_results.append(result)
        
        unique_results.sort(key=lambda x: x.relevance_score, reverse=True)
        return unique_results[:limit]