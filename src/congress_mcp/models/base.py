"""
Base models for Congress API data structures.
"""

from datetime import datetime
from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field, ConfigDict


class BaseCongressModel(BaseModel):
    """Base model for all Congress API data structures."""
    
    model_config = ConfigDict(
        extra="allow",  # Allow extra fields for API evolution
        str_strip_whitespace=True,
        validate_assignment=True,
        arbitrary_types_allowed=True
    )


class RequestInfo(BaseCongressModel):
    """Information about the API request."""
    
    content_type: Optional[str] = Field(None, alias="contentType")
    format: Optional[str] = None


class PaginationInfo(BaseCongressModel):
    """Pagination information for API responses."""
    
    count: int = Field(..., description="Total number of items")
    next: Optional[str] = Field(None, description="URL for next page")
    previous: Optional[str] = Field(None, description="URL for previous page")


class ApiResponse(BaseCongressModel):
    """Base API response structure."""
    
    request: Optional[RequestInfo] = None
    pagination: Optional[PaginationInfo] = None
    
    def get_items(self) -> List[Any]:
        """Get the items from the response. Override in subclasses."""
        return []
    
    def get_total_count(self) -> int:
        """Get total count from pagination."""
        return self.pagination.count if self.pagination else 0


class CongressReference(BaseCongressModel):
    """Reference to a Congress."""
    
    number: int = Field(..., description="Congress number")
    name: Optional[str] = Field(None, description="Congress name")
    start_year: Optional[int] = Field(None, alias="startYear")
    end_year: Optional[int] = Field(None, alias="endYear")


class UrlReference(BaseCongressModel):
    """Reference with URL."""
    
    url: str = Field(..., description="API URL")
    
    
class NamedUrlReference(UrlReference):
    """Reference with URL and name."""
    
    name: str = Field(..., description="Name")


class SystemCodeReference(UrlReference):
    """Reference with system code."""
    
    system_code: str = Field(..., alias="systemCode", description="System code")
    name: Optional[str] = Field(None, description="Name")


class DateInfo(BaseCongressModel):
    """Date information with optional time."""
    
    date: Optional[str] = Field(None, description="Date in ISO format")
    time: Optional[str] = Field(None, description="Time information")
    
    
class UpdateInfo(BaseCongressModel):
    """Update information."""
    
    update_date: Optional[datetime] = Field(None, alias="updateDate")
    
    
class ActionInfo(BaseCongressModel):
    """Action information."""
    
    action_date: Optional[str] = Field(None, alias="actionDate")
    text: Optional[str] = Field(None, description="Action text")
    action_time: Optional[str] = Field(None, alias="actionTime")
    
    
class LatestAction(ActionInfo):
    """Latest action information."""
    
    url: Optional[str] = Field(None, description="URL to related item")


class Contact(BaseCongressModel):
    """Contact information."""
    
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None