#!/usr/bin/env python3
"""
Comprehensive test script for all 16 MCP tools.
Tests each tool with realistic parameters and validates responses.
"""

import asyncio
import sys
import os
import json
from pathlib import Path
from typing import Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Test configuration
TEST_RESULTS = {}
PASSED_TESTS = 0
FAILED_TESTS = 0

async def run_tool_test(server, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single tool test and return results."""
    global PASSED_TESTS, FAILED_TESTS
    
    try:
        print(f"🔧 Testing {tool_name}...")
        
        # Use the server's _call_tool method
        result = await server._call_tool(tool_name, params)
        
        # Validate result is not empty
        if result and len(str(result)) > 10:
            print(f"  ✅ {tool_name}: PASSED ({len(str(result))} chars)")
            PASSED_TESTS += 1
            return {"status": "PASSED", "result_length": len(str(result)), "sample": str(result)[:100]}
        else:
            print(f"  ⚠️  {tool_name}: EMPTY RESULT")
            FAILED_TESTS += 1
            return {"status": "EMPTY", "result": result}
            
    except Exception as e:
        print(f"  ❌ {tool_name}: FAILED - {str(e)}")
        FAILED_TESTS += 1
        return {"status": "FAILED", "error": str(e)}

async def test_all_tools():
    """Test all 16 MCP tools with realistic parameters."""
    try:
        from congress_mcp.mcp_server.server import CongressMCPServer
        from congress_mcp.utils.logging import setup_logging
        
        # Setup logging (quiet for testing)
        setup_logging(level="WARNING")
        
        print("🚀 Starting comprehensive tool testing...")
        print("=" * 60)
        
        # Initialize server
        server = CongressMCPServer()
        
        # Initialize client manually (normally done by MCP framework)
        from congress_mcp.api.client import CongressAPIClient
        from congress_mcp.api.search import CongressSearchEngine
        
        server.client = CongressAPIClient()
        server.search_engine = CongressSearchEngine(server.client)
        
        # Test cases for each tool
        test_cases = [
            # Committee Tools
            ("get_committees", {"chamber": "house", "limit": 5}),
            ("get_committee_details", {"system_code": "hsag00"}),
            ("get_committee_hearings", {"chamber": "house", "committee": "hsag", "limit": 3}),
            
            # Hearing Tools
            ("get_hearings", {"limit": 5}),
            ("search_hearings", {"query": "budget", "limit": 3}),
            
            # Bill Tools
            ("get_bills", {"congress": 119, "limit": 5}),
            ("get_bill_details", {"congress": 119, "bill_type": "hr", "bill_number": 1}),
            ("search_bills", {"query": "infrastructure", "limit": 3}),
            
            # Member Tools
            ("get_members", {"congress": 119, "chamber": "house", "limit": 5}),
            ("get_member_details", {"bioguide_id": "P000197"}),
            
            # Utility Tools
            ("get_congress_info", {}),
            ("get_rate_limit_status", {}),
            
            # Search Tools
            ("search_all", {"query": "healthcare", "limit": 3}),
            ("search_by_topic", {"topic": "healthcare", "limit": 3}),
            
            # Health Tools
            ("get_health_status", {}),
            ("get_system_metrics", {}),
        ]
        
        # Run all tests
        for tool_name, params in test_cases:
            result = await run_tool_test(server, tool_name, params)
            TEST_RESULTS[tool_name] = result
            
            # Small delay between tests to respect rate limits
            await asyncio.sleep(0.1)
        
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print(f"✅ PASSED: {PASSED_TESTS}")
        print(f"❌ FAILED: {FAILED_TESTS}")
        print(f"📈 SUCCESS RATE: {(PASSED_TESTS / (PASSED_TESTS + FAILED_TESTS)) * 100:.1f}%")
        
        # Show any failures
        failed_tools = [tool for tool, result in TEST_RESULTS.items() if result["status"] != "PASSED"]
        if failed_tools:
            print(f"\n⚠️  FAILED TOOLS: {', '.join(failed_tools)}")
        
        # Save test results
        results_file = project_root / "test_results.json"
        with open(results_file, "w") as f:
            json.dump({
                "summary": {
                    "passed": PASSED_TESTS,
                    "failed": FAILED_TESTS,
                    "success_rate": (PASSED_TESTS / (PASSED_TESTS + FAILED_TESTS)) * 100
                },
                "details": TEST_RESULTS
            }, f, indent=2)
        
        print(f"\n📁 Detailed results saved to: {results_file}")
        
        return FAILED_TESTS == 0
        
    except Exception as e:
        print(f"❌ Testing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Ensure API key is set
    if not os.environ.get("CONGRESS_API_KEY"):
        print("⚠️  Setting Congress API key from .env file...")
        env_file = project_root / ".env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith("CONGRESS_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
                        os.environ["CONGRESS_API_KEY"] = api_key
                        break
    
    success = asyncio.run(test_all_tools())
    sys.exit(0 if success else 1)