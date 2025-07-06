"""
Bill models for Congress API data structures.
"""

from typing import List, Optional, Dict, Any
from pydantic import Field

from .base import (
    BaseCongressModel, 
    ApiResponse, 
    UrlReference,
    SystemCodeReference,
    LatestAction,
    UpdateInfo
)


class BillSponsor(BaseCongressModel):
    """Bill sponsor information."""
    
    bioguide_id: Optional[str] = Field(None, alias="bioguideId")
    district: Optional[int] = None
    first_name: Optional[str] = Field(None, alias="firstName")
    full_name: Optional[str] = Field(None, alias="fullName")
    is_by_request: Optional[bool] = Field(None, alias="isByRequest")
    last_name: Optional[str] = Field(None, alias="lastName")
    middle_name: Optional[str] = Field(None, alias="middleName")
    party: Optional[str] = None
    state: Optional[str] = None
    url: Optional[str] = None


class BillCosponsor(BaseCongressModel):
    """Bill cosponsor information."""
    
    bioguide_id: Optional[str] = Field(None, alias="bioguideId")
    district: Optional[int] = None
    first_name: Optional[str] = Field(None, alias="firstName")
    full_name: Optional[str] = Field(None, alias="fullName")
    is_original_cosponsor: Optional[bool] = Field(None, alias="isOriginalCosponsor")
    last_name: Optional[str] = Field(None, alias="lastName")
    middle_name: Optional[str] = Field(None, alias="middleName")
    party: Optional[str] = None
    sponsorship_date: Optional[str] = Field(None, alias="sponsorshipDate")
    sponsorship_withdrawn_date: Optional[str] = Field(None, alias="sponsorshipWithdrawnDate")
    state: Optional[str] = None
    url: Optional[str] = None


class BillCommittee(BaseCongressModel):
    """Committee associated with a bill."""
    
    url: Optional[str] = None
    system_code: Optional[str] = Field(None, alias="systemCode")
    name: Optional[str] = None


class BillCommitteeActivity(BaseCongressModel):
    """Committee activity on a bill."""
    
    name: Optional[str] = None
    date: Optional[str] = None


class BillSubject(BaseCongressModel):
    """Bill subject information."""
    
    name: Optional[str] = None
    update_date: Optional[str] = Field(None, alias="updateDate")


class BillLaw(BaseCongressModel):
    """Law information for enacted bills."""
    
    number: Optional[str] = None
    type: Optional[str] = None


class BillSummary(BaseCongressModel):
    """Bill summary information."""
    
    action_date: Optional[str] = Field(None, alias="actionDate")
    action_desc: Optional[str] = Field(None, alias="actionDesc")
    text: Optional[str] = None
    update_date: Optional[str] = Field(None, alias="updateDate")
    version_code: Optional[str] = Field(None, alias="versionCode")


class BillTextVersion(BaseCongressModel):
    """Bill text version information."""
    
    date: Optional[str] = None
    type: Optional[str] = None
    formats: Optional[List[Dict[str, Any]]] = None


class BillAction(BaseCongressModel):
    """Bill action information."""
    
    action_code: Optional[str] = Field(None, alias="actionCode")
    action_date: Optional[str] = Field(None, alias="actionDate")
    action_time: Optional[str] = Field(None, alias="actionTime")
    committees: Optional[List[BillCommittee]] = None
    source_system: Optional[Dict[str, Any]] = Field(None, alias="sourceSystem")
    text: Optional[str] = None
    type: Optional[str] = None


class BillTitle(BaseCongressModel):
    """Bill title information."""
    
    bill_text_version_code: Optional[str] = Field(None, alias="billTextVersionCode")
    bill_text_version_name: Optional[str] = Field(None, alias="billTextVersionName")
    chamber_code: Optional[str] = Field(None, alias="chamberCode")
    chamber_name: Optional[str] = Field(None, alias="chamberName")
    title: Optional[str] = None
    title_type: Optional[str] = Field(None, alias="titleType")
    title_type_code: Optional[str] = Field(None, alias="titleTypeCode")
    update_date: Optional[str] = Field(None, alias="updateDate")


class Bill(BaseCongressModel):
    """Bill information."""
    
    url: Optional[str] = None
    congress: Optional[int] = None
    bill_type: Optional[str] = Field(None, alias="type")
    bill_number: Optional[int] = Field(None, alias="number")
    origin_chamber: Optional[str] = Field(None, alias="originChamber")
    origin_chamber_code: Optional[str] = Field(None, alias="originChamberCode")
    title: Optional[str] = None
    introduced_date: Optional[str] = Field(None, alias="introducedDate")
    sponsors: Optional[List[BillSponsor]] = None
    cosponsors: Optional[List[BillCosponsor]] = None
    committees: Optional[List[BillCommittee]] = None
    committee_activities: Optional[List[BillCommitteeActivity]] = Field(None, alias="committeeActivities")
    subjects: Optional[List[BillSubject]] = None
    laws: Optional[List[BillLaw]] = None
    summaries: Optional[List[BillSummary]] = None
    text_versions: Optional[List[BillTextVersion]] = Field(None, alias="textVersions")
    actions: Optional[List[BillAction]] = None
    titles: Optional[List[BillTitle]] = None
    latest_action: Optional[LatestAction] = Field(None, alias="latestAction")
    update_date: Optional[str] = Field(None, alias="updateDate")
    
    def get_bill_identifier(self) -> str:
        """Get bill identifier string."""
        if self.bill_type and self.bill_number:
            return f"{self.bill_type} {self.bill_number}"
        return "Unknown"
    
    def get_chamber_display(self) -> str:
        """Get display name for origin chamber."""
        chamber_map = {
            "house": "House",
            "senate": "Senate"
        }
        return chamber_map.get(self.origin_chamber.lower() if self.origin_chamber else "", self.origin_chamber or "Unknown")
    
    def get_sponsor_name(self) -> str:
        """Get primary sponsor name."""
        if self.sponsors and len(self.sponsors) > 0:
            sponsor = self.sponsors[0]
            return sponsor.full_name or f"{sponsor.first_name} {sponsor.last_name}"
        return "Unknown"
    
    def get_cosponsor_count(self) -> int:
        """Get number of cosponsors."""
        return len(self.cosponsors) if self.cosponsors else 0
    
    def get_committee_count(self) -> int:
        """Get number of committees."""
        return len(self.committees) if self.committees else 0
    
    def is_enacted(self) -> bool:
        """Check if bill is enacted into law."""
        return bool(self.laws and len(self.laws) > 0)
    
    def get_latest_action_text(self) -> str:
        """Get latest action text."""
        return self.latest_action.text if self.latest_action else "Unknown"
    
    def get_latest_action_date(self) -> str:
        """Get latest action date."""
        return self.latest_action.action_date if self.latest_action else "Unknown"


class BillList(ApiResponse):
    """Bill list response."""
    
    bills: List[Bill] = Field(default_factory=list)
    
    def get_items(self) -> List[Bill]:
        """Get bill items."""
        return self.bills


class BillDetails(ApiResponse):
    """Bill details response."""
    
    bill: Optional[Bill] = None
    
    def get_items(self) -> List[Bill]:
        """Get bill as a list."""
        return [self.bill] if self.bill else []


class BillAmendment(BaseCongressModel):
    """Bill amendment information."""
    
    url: Optional[str] = None
    congress: Optional[int] = None
    number: Optional[int] = None
    type: Optional[str] = None
    description: Optional[str] = None
    purpose: Optional[str] = None
    sponsors: Optional[List[BillSponsor]] = None
    cosponsors: Optional[List[BillCosponsor]] = None
    latest_action: Optional[LatestAction] = Field(None, alias="latestAction")
    update_date: Optional[str] = Field(None, alias="updateDate")


class BillAmendmentList(ApiResponse):
    """Bill amendment list response."""
    
    amendments: List[BillAmendment] = Field(default_factory=list)
    
    def get_items(self) -> List[BillAmendment]:
        """Get amendment items."""
        return self.amendments