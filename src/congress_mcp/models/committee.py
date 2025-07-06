"""
Committee models for Congress API data structures.
"""

from typing import List, Optional, Dict, Any
from pydantic import Field

from .base import (
    BaseCongressModel, 
    ApiResponse, 
    SystemCodeReference, 
    UrlReference,
    UpdateInfo
)


class CommitteeParent(BaseCongressModel):
    """Parent committee information."""
    
    url: Optional[str] = None
    system_code: Optional[str] = Field(None, alias="systemCode")
    name: Optional[str] = None


class CommitteeSubcommittee(BaseCongressModel):
    """Subcommittee information."""
    
    url: Optional[str] = None
    system_code: Optional[str] = Field(None, alias="systemCode")
    name: Optional[str] = None


class CommitteeHistory(BaseCongressModel):
    """Committee history information."""
    
    end_date: Optional[str] = Field(None, alias="endDate")
    official_name: Optional[str] = Field(None, alias="officialName")
    library_of_congress_name: Optional[str] = Field(None, alias="libraryOfCongressName")
    start_date: Optional[str] = Field(None, alias="startDate")
    committee_type_code: Optional[str] = Field(None, alias="committeeTypeCode")
    establishing_authority: Optional[str] = Field(None, alias="establishingAuthority")
    loc_linked_data_id: Optional[str] = Field(None, alias="locLinkedDataId")
    superintendent_document_number: Optional[str] = Field(None, alias="superintendentDocumentNumber")
    nara_id: Optional[str] = Field(None, alias="naraId")


class CommitteeReports(BaseCongressModel):
    """Committee reports reference."""
    
    url: Optional[str] = None
    count: Optional[int] = None


class CommitteeCommunications(BaseCongressModel):
    """Committee communications reference."""
    
    url: Optional[str] = None
    count: Optional[int] = None


class CommitteeBills(BaseCongressModel):
    """Committee bills reference."""
    
    url: Optional[str] = None
    count: Optional[int] = None


class CommitteeNominations(BaseCongressModel):
    """Committee nominations reference."""
    
    url: Optional[str] = None
    count: Optional[int] = None


class Committee(BaseCongressModel):
    """Committee information."""
    
    url: Optional[str] = None
    system_code: Optional[str] = Field(None, alias="systemCode")
    name: Optional[str] = None
    chamber: Optional[str] = None
    committee_type_code: Optional[str] = Field(None, alias="committeeTypeCode")
    parent: Optional[CommitteeParent] = None
    subcommittees: Optional[List[CommitteeSubcommittee]] = None
    is_current: Optional[bool] = Field(None, alias="isCurrent")
    
    # Additional fields for detailed view
    update_date: Optional[str] = Field(None, alias="updateDate")
    reports: Optional[CommitteeReports] = None
    communications: Optional[CommitteeCommunications] = None
    bills: Optional[CommitteeBills] = None
    nominations: Optional[CommitteeNominations] = None
    history: Optional[List[CommitteeHistory]] = None
    type: Optional[str] = None
    
    def get_chamber_display(self) -> str:
        """Get display name for chamber."""
        chamber_map = {
            "house": "House",
            "senate": "Senate", 
            "joint": "Joint"
        }
        return chamber_map.get(self.chamber.lower() if self.chamber else "", self.chamber or "Unknown")
    
    def get_type_display(self) -> str:
        """Get display name for committee type."""
        return self.committee_type_code or self.type or "Unknown"
    
    def is_subcommittee(self) -> bool:
        """Check if this is a subcommittee."""
        return self.parent is not None
    
    def get_subcommittee_count(self) -> int:
        """Get number of subcommittees."""
        return len(self.subcommittees) if self.subcommittees else 0


class CommitteeList(ApiResponse):
    """Committee list response."""
    
    committees: List[Committee] = Field(default_factory=list)
    
    def get_items(self) -> List[Committee]:
        """Get committee items."""
        return self.committees


class CommitteeDetails(ApiResponse):
    """Committee details response."""
    
    committee: Optional[Committee] = None
    
    def get_items(self) -> List[Committee]:
        """Get committee as a list."""
        return [self.committee] if self.committee else []


class CommitteeReport(BaseCongressModel):
    """Committee report information."""
    
    citation: Optional[str] = None
    url: Optional[str] = None
    update_date: Optional[str] = Field(None, alias="updateDate")
    congress: Optional[int] = None
    chamber: Optional[str] = None
    type: Optional[str] = None
    number: Optional[int] = None
    part: Optional[int] = None


class CommitteeReportsList(ApiResponse):
    """Committee reports list response."""
    
    reports: List[CommitteeReport] = Field(default_factory=list)
    
    def get_items(self) -> List[CommitteeReport]:
        """Get report items."""
        return self.reports


class CommitteeBill(BaseCongressModel):
    """Committee bill information."""
    
    congress: Optional[int] = None
    bill_type: Optional[str] = Field(None, alias="billType")
    bill_number: Optional[int] = Field(None, alias="billNumber")
    relationship_type: Optional[str] = Field(None, alias="relationshipType")
    action_date: Optional[str] = Field(None, alias="actionDate")
    update_date: Optional[str] = Field(None, alias="updateDate")
    
    def get_bill_identifier(self) -> str:
        """Get bill identifier string."""
        if self.bill_type and self.bill_number:
            return f"{self.bill_type} {self.bill_number}"
        return "Unknown"


class CommitteeBillsList(ApiResponse):
    """Committee bills list response."""
    
    committee_bills: Optional[Dict[str, Any]] = Field(None, alias="committee-bills")
    bills: Optional[List[CommitteeBill]] = None
    
    def get_items(self) -> List[CommitteeBill]:
        """Get bill items."""
        if self.bills:
            return self.bills
        elif self.committee_bills and "bills" in self.committee_bills:
            # Handle nested structure
            bills_data = self.committee_bills["bills"]
            if isinstance(bills_data, list):
                return [CommitteeBill(**bill) for bill in bills_data]
        return []