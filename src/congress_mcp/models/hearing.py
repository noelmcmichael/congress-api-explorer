"""
Hearing models for Congress API data structures.
"""

from typing import List, Optional, Dict, Any
from pydantic import Field

from .base import (
    BaseCongressModel, 
    ApiResponse, 
    UrlReference,
    SystemCodeReference,
    DateInfo,
    UpdateInfo
)


class HearingCommittee(BaseCongressModel):
    """Committee associated with a hearing."""
    
    url: Optional[str] = None
    system_code: Optional[str] = Field(None, alias="systemCode")
    name: Optional[str] = None


class HearingJacket(BaseCongressModel):
    """Hearing jacket information."""
    
    jacket_number: Optional[str] = Field(None, alias="jacketNumber")
    jacket_id: Optional[str] = Field(None, alias="jacketId")


class HearingFormat(BaseCongressModel):
    """Hearing format information."""
    
    type: Optional[str] = None
    name: Optional[str] = None


class HearingLocation(BaseCongressModel):
    """Hearing location information."""
    
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = Field(None, alias="zipCode")


class HearingWitness(BaseCongressModel):
    """Hearing witness information."""
    
    name: Optional[str] = None
    organization: Optional[str] = None
    title: Optional[str] = None
    biography: Optional[str] = None


class HearingDocument(BaseCongressModel):
    """Hearing document information."""
    
    name: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None


class HearingTranscript(BaseCongressModel):
    """Hearing transcript information."""
    
    jacket_number: Optional[str] = Field(None, alias="jacketNumber")
    url: Optional[str] = None


class HearingVideo(BaseCongressModel):
    """Hearing video information."""
    
    url: Optional[str] = None
    duration: Optional[str] = None
    format: Optional[str] = None


class HearingBill(BaseCongressModel):
    """Bill associated with a hearing."""
    
    congress: Optional[int] = None
    bill_type: Optional[str] = Field(None, alias="billType")
    bill_number: Optional[int] = Field(None, alias="billNumber")
    url: Optional[str] = None
    title: Optional[str] = None


class Hearing(BaseCongressModel):
    """Hearing information."""
    
    url: Optional[str] = None
    congress: Optional[int] = None
    chamber: Optional[str] = None
    jacket: Optional[HearingJacket] = None
    title: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    location: Optional[HearingLocation] = None
    committee: Optional[HearingCommittee] = None
    formats: Optional[List[HearingFormat]] = None
    witnesses: Optional[List[HearingWitness]] = None
    documents: Optional[List[HearingDocument]] = None
    transcripts: Optional[List[HearingTranscript]] = None
    videos: Optional[List[HearingVideo]] = None
    related_bills: Optional[List[HearingBill]] = Field(None, alias="relatedBills")
    update_date: Optional[str] = Field(None, alias="updateDate")
    
    def get_chamber_display(self) -> str:
        """Get display name for chamber."""
        chamber_map = {
            "house": "House",
            "senate": "Senate", 
            "joint": "Joint"
        }
        return chamber_map.get(self.chamber.lower() if self.chamber else "", self.chamber or "Unknown")
    
    def get_committee_name(self) -> str:
        """Get committee name."""
        return self.committee.name if self.committee else "Unknown"
    
    def get_date_display(self) -> str:
        """Get formatted date display."""
        if self.date:
            return self.date
        return "Unknown"
    
    def get_title_display(self) -> str:
        """Get display title."""
        return self.title or "Unknown"
    
    def has_video(self) -> bool:
        """Check if hearing has video."""
        return bool(self.videos and len(self.videos) > 0)
    
    def has_transcript(self) -> bool:
        """Check if hearing has transcript."""
        return bool(self.transcripts and len(self.transcripts) > 0)
    
    def get_witness_count(self) -> int:
        """Get number of witnesses."""
        return len(self.witnesses) if self.witnesses else 0
    
    def get_related_bills_count(self) -> int:
        """Get number of related bills."""
        return len(self.related_bills) if self.related_bills else 0


class HearingList(ApiResponse):
    """Hearing list response."""
    
    hearings: List[Hearing] = Field(default_factory=list)
    
    def get_items(self) -> List[Hearing]:
        """Get hearing items."""
        return self.hearings


class HearingDetails(ApiResponse):
    """Hearing details response."""
    
    hearing: Optional[Hearing] = None
    
    def get_items(self) -> List[Hearing]:
        """Get hearing as a list."""
        return [self.hearing] if self.hearing else []


class CommitteeMeeting(BaseCongressModel):
    """Committee meeting information."""
    
    url: Optional[str] = None
    congress: Optional[int] = None
    chamber: Optional[str] = None
    committee: Optional[HearingCommittee] = None
    date: Optional[str] = None
    time: Optional[str] = None
    location: Optional[HearingLocation] = None
    meeting_type: Optional[str] = Field(None, alias="meetingType")
    title: Optional[str] = None
    agenda: Optional[str] = None
    hearing_transcripts: Optional[List[HearingTranscript]] = Field(None, alias="hearingTranscripts")
    related_bills: Optional[List[HearingBill]] = Field(None, alias="relatedBills")
    update_date: Optional[str] = Field(None, alias="updateDate")
    
    def get_chamber_display(self) -> str:
        """Get display name for chamber."""
        chamber_map = {
            "house": "House",
            "senate": "Senate", 
            "joint": "Joint"
        }
        return chamber_map.get(self.chamber.lower() if self.chamber else "", self.chamber or "Unknown")
    
    def get_committee_name(self) -> str:
        """Get committee name."""
        return self.committee.name if self.committee else "Unknown"
    
    def get_meeting_type_display(self) -> str:
        """Get meeting type display."""
        return self.meeting_type or "Unknown"


class CommitteeMeetingList(ApiResponse):
    """Committee meeting list response."""
    
    committee_meetings: List[CommitteeMeeting] = Field(default_factory=list, alias="committeeMeetings")
    
    def get_items(self) -> List[CommitteeMeeting]:
        """Get meeting items."""
        return self.committee_meetings