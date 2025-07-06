"""
Member models for Congress API data structures.
"""

from typing import List, Optional, Dict, Any, Union
from pydantic import Field

from .base import (
    BaseCongressModel, 
    ApiResponse, 
    UrlReference,
    UpdateInfo,
    Contact
)


class MemberTerm(BaseCongressModel):
    """Member term information."""
    
    congress: Optional[int] = None
    chamber: Optional[str] = None
    start_year: Optional[int] = Field(None, alias="startYear")
    end_year: Optional[int] = Field(None, alias="endYear")
    state_code: Optional[str] = Field(None, alias="stateCode")
    state_name: Optional[str] = Field(None, alias="stateName")
    district: Optional[int] = None
    party_code: Optional[str] = Field(None, alias="partyCode")
    party_name: Optional[str] = Field(None, alias="partyName")
    member_type: Optional[str] = Field(None, alias="memberType")


class MemberLeadership(BaseCongressModel):
    """Member leadership position."""
    
    congress: Optional[int] = None
    current: Optional[bool] = None
    type: Optional[str] = None
    
    
class MemberCommittee(BaseCongressModel):
    """Member committee information."""
    
    url: Optional[str] = None
    system_code: Optional[str] = Field(None, alias="systemCode")
    name: Optional[str] = None
    chamber: Optional[str] = None
    rank: Optional[int] = None


class MemberSponsoredLegislation(BaseCongressModel):
    """Member sponsored legislation reference."""
    
    url: Optional[str] = None
    count: Optional[int] = None


class MemberCosponsoredLegislation(BaseCongressModel):
    """Member cosponsored legislation reference."""
    
    url: Optional[str] = None
    count: Optional[int] = None


class MemberDepiction(BaseCongressModel):
    """Member photo/image information."""
    
    attribution: Optional[str] = None
    image_url: Optional[str] = Field(None, alias="imageUrl")


class MemberName(BaseCongressModel):
    """Member name information."""
    
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    middle_name: Optional[str] = Field(None, alias="middleName")
    suffix: Optional[str] = None
    nickname: Optional[str] = None
    official_name: Optional[str] = Field(None, alias="officialName")


class MemberAddress(BaseCongressModel):
    """Member address information."""
    
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = Field(None, alias="zipCode")
    phone_number: Optional[str] = Field(None, alias="phoneNumber")


class Member(BaseCongressModel):
    """Member information."""
    
    url: Optional[str] = None
    bioguide_id: Optional[str] = Field(None, alias="bioguideId")
    district: Optional[int] = None
    first_name: Optional[str] = Field(None, alias="firstName")
    full_name: Optional[str] = Field(None, alias="fullName")
    last_name: Optional[str] = Field(None, alias="lastName")
    middle_name: Optional[str] = Field(None, alias="middleName")
    name: Optional[Union[str, MemberName]] = None  # Can be string or MemberName object
    party: Optional[str] = None
    state: Optional[str] = None
    terms: Optional[Dict[str, List[MemberTerm]]] = None  # Nested under 'item' key
    leadership: Optional[List[MemberLeadership]] = None
    committees: Optional[List[MemberCommittee]] = None
    sponsored_legislation: Optional[MemberSponsoredLegislation] = Field(None, alias="sponsoredLegislation")
    cosponsored_legislation: Optional[MemberCosponsoredLegislation] = Field(None, alias="cosponsoredLegislation")
    depiction: Optional[MemberDepiction] = None
    addresses: Optional[List[MemberAddress]] = None
    phone_number: Optional[str] = Field(None, alias="phoneNumber")
    
    # Additional biographical information
    birth_year: Optional[int] = Field(None, alias="birthYear")
    death_year: Optional[int] = Field(None, alias="deathYear")
    honorific_name: Optional[str] = Field(None, alias="honorificName")
    nicknames: Optional[List[str]] = None
    official_website_url: Optional[str] = Field(None, alias="officialWebsiteUrl")
    
    update_date: Optional[str] = Field(None, alias="updateDate")
    
    def get_display_name(self) -> str:
        """Get display name for member."""
        if self.full_name:
            return self.full_name
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.name:
            if isinstance(self.name, str):
                return self.name
            else:
                return self.name.official_name or f"{self.name.first_name} {self.name.last_name}"
        return "Unknown"
    
    def get_party_display(self) -> str:
        """Get party display name."""
        party_map = {
            "D": "Democrat",
            "R": "Republican", 
            "I": "Independent",
            "ID": "Independent Democrat",
            "L": "Libertarian"
        }
        return party_map.get(self.party, self.party or "Unknown")
    
    def get_state_display(self) -> str:
        """Get state display."""
        return self.state or "Unknown"
    
    def get_district_display(self) -> str:
        """Get district display."""
        if self.district:
            return f"District {self.district}"
        return "At Large"
    
    def get_current_term(self) -> Optional[MemberTerm]:
        """Get current term information."""
        if not self.terms:
            return None
        
        # Handle nested structure
        term_list = self.terms.get("item", []) if isinstance(self.terms, dict) else []
        if not term_list:
            return None
        
        # Return the most recent term
        return max(term_list, key=lambda t: t.congress or 0)
    
    def get_current_chamber(self) -> str:
        """Get current chamber."""
        current_term = self.get_current_term()
        if current_term:
            return current_term.chamber or "Unknown"
        return "Unknown"
    
    def get_committee_count(self) -> int:
        """Get number of committees."""
        return len(self.committees) if self.committees else 0
    
    def get_leadership_positions(self) -> List[str]:
        """Get list of leadership positions."""
        if not self.leadership:
            return []
        return [pos.type for pos in self.leadership if pos.type and pos.current]
    
    def has_photo(self) -> bool:
        """Check if member has photo."""
        return bool(self.depiction and self.depiction.image_url)
    
    def get_photo_url(self) -> Optional[str]:
        """Get photo URL."""
        return self.depiction.image_url if self.depiction else None
    
    def is_active(self) -> bool:
        """Check if member is currently active."""
        current_term = self.get_current_term()
        if not current_term:
            return False
        # This is a simple heuristic - in practice you'd want to check end dates
        return current_term.congress and current_term.congress >= 118  # Adjust as needed


class MemberList(ApiResponse):
    """Member list response."""
    
    members: List[Member] = Field(default_factory=list)
    
    def get_items(self) -> List[Member]:
        """Get member items."""
        return self.members


class MemberDetails(ApiResponse):
    """Member details response."""
    
    member: Optional[Member] = None
    
    def get_items(self) -> List[Member]:
        """Get member as a list."""
        return [self.member] if self.member else []


class MemberSponsoredBill(BaseCongressModel):
    """Member sponsored bill information."""
    
    congress: Optional[int] = None
    bill_type: Optional[str] = Field(None, alias="type")
    bill_number: Optional[int] = Field(None, alias="number")
    url: Optional[str] = None
    title: Optional[str] = None
    introduced_date: Optional[str] = Field(None, alias="introducedDate")
    policy_area: Optional[str] = Field(None, alias="policyArea")
    latest_action: Optional[str] = Field(None, alias="latestAction")
    
    def get_bill_identifier(self) -> str:
        """Get bill identifier string."""
        if self.bill_type and self.bill_number:
            return f"{self.bill_type} {self.bill_number}"
        return "Unknown"


class MemberSponsoredBillList(ApiResponse):
    """Member sponsored bill list response."""
    
    sponsored_legislation: List[MemberSponsoredBill] = Field(default_factory=list, alias="sponsoredLegislation")
    
    def get_items(self) -> List[MemberSponsoredBill]:
        """Get sponsored bill items."""
        return self.sponsored_legislation


class MemberCosponsoredBill(BaseCongressModel):
    """Member cosponsored bill information."""
    
    congress: Optional[int] = None
    bill_type: Optional[str] = Field(None, alias="type")
    bill_number: Optional[int] = Field(None, alias="number")
    url: Optional[str] = None
    title: Optional[str] = None
    sponsorship_date: Optional[str] = Field(None, alias="sponsorshipDate")
    policy_area: Optional[str] = Field(None, alias="policyArea")
    latest_action: Optional[str] = Field(None, alias="latestAction")
    
    def get_bill_identifier(self) -> str:
        """Get bill identifier string."""
        if self.bill_type and self.bill_number:
            return f"{self.bill_type} {self.bill_number}"
        return "Unknown"


class MemberCosponsoredBillList(ApiResponse):
    """Member cosponsored bill list response."""
    
    cosponsored_legislation: List[MemberCosponsoredBill] = Field(default_factory=list, alias="cosponsoredLegislation")
    
    def get_items(self) -> List[MemberCosponsoredBill]:
        """Get cosponsored bill items."""
        return self.cosponsored_legislation