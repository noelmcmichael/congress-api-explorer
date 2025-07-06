#!/usr/bin/env python3
"""
Test script for Pydantic models with real API data.
"""

import asyncio
import json
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from congress_mcp.api import CongressAPIClient
from congress_mcp.models import (
    CommitteeList, 
    HearingList, 
    BillList, 
    MemberList
)
from congress_mcp.utils import logger


async def test_models():
    """Test the Pydantic models with real API data."""
    
    api_key = "kF6SxbPbbXXjOGDd2FIFaYUkZRuYfQN2OsQtnj9G"
    
    logger.info("Testing Pydantic models with Congress API data...")
    
    async with CongressAPIClient(api_key) as client:
        try:
            # Test Congress number
            test_congress = 118
            
            # Test Committee models
            logger.info("Testing Committee models...")
            committees_data = await client.get_committees(
                congress=test_congress,
                limit=3
            )
            
            committees = CommitteeList(**committees_data)
            logger.info(f"Parsed {len(committees.committees)} committees")
            
            for committee in committees.committees[:2]:
                logger.info(f"  - {committee.name} ({committee.get_chamber_display()})")
                logger.info(f"    System Code: {committee.system_code}")
                logger.info(f"    Type: {committee.get_type_display()}")
                logger.info(f"    Subcommittees: {committee.get_subcommittee_count()}")
            
            # Test Hearing models
            logger.info("Testing Hearing models...")
            hearings_data = await client.get_committee_hearings(
                congress=test_congress,
                limit=3
            )
            
            hearings = HearingList(**hearings_data)
            logger.info(f"Parsed {len(hearings.hearings)} hearings")
            
            for hearing in hearings.hearings[:2]:
                logger.info(f"  - {hearing.get_title_display()}")
                logger.info(f"    Date: {hearing.get_date_display()}")
                logger.info(f"    Chamber: {hearing.get_chamber_display()}")
                logger.info(f"    Committee: {hearing.get_committee_name()}")
                logger.info(f"    Has Video: {hearing.has_video()}")
                logger.info(f"    Has Transcript: {hearing.has_transcript()}")
            
            # Test Bill models
            logger.info("Testing Bill models...")
            bills_data = await client.get_bills(
                congress=test_congress,
                limit=3
            )
            
            bills = BillList(**bills_data)
            logger.info(f"Parsed {len(bills.bills)} bills")
            
            for bill in bills.bills[:2]:
                logger.info(f"  - {bill.get_bill_identifier()}: {bill.title}")
                logger.info(f"    Sponsor: {bill.get_sponsor_name()}")
                logger.info(f"    Chamber: {bill.get_chamber_display()}")
                logger.info(f"    Cosponsors: {bill.get_cosponsor_count()}")
                logger.info(f"    Committees: {bill.get_committee_count()}")
                logger.info(f"    Enacted: {bill.is_enacted()}")
                logger.info(f"    Latest Action: {bill.get_latest_action_text()}")
            
            # Test Member models
            logger.info("Testing Member models...")
            members_data = await client.get_members(
                congress=test_congress,
                limit=3
            )
            
            members = MemberList(**members_data)
            logger.info(f"Parsed {len(members.members)} members")
            
            for member in members.members[:2]:
                logger.info(f"  - {member.get_display_name()}")
                logger.info(f"    Party: {member.get_party_display()}")
                logger.info(f"    State: {member.get_state_display()}")
                logger.info(f"    District: {member.get_district_display()}")
                logger.info(f"    Chamber: {member.get_current_chamber()}")
                logger.info(f"    Committees: {member.get_committee_count()}")
                logger.info(f"    Leadership: {member.get_leadership_positions()}")
                logger.info(f"    Has Photo: {member.has_photo()}")
                logger.info(f"    Active: {member.is_active()}")
            
            logger.info("Model testing completed successfully!")
            
        except Exception as e:
            logger.error(f"Error during model testing: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(test_models())