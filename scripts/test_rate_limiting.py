#!/usr/bin/env python3
"""
Test script to validate API rate limiting and caching behavior.
"""

import asyncio
import sys
import os
import time
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

async def test_rate_limiting():
    """Test rate limiting and caching behavior."""
    try:
        from congress_mcp.api.client import CongressAPIClient
        from congress_mcp.utils.logging import setup_logging
        
        # Setup logging
        setup_logging(level="INFO")
        
        print("🚀 Testing Rate Limiting and Caching...")
        print("=" * 60)
        
        # Initialize client
        client = CongressAPIClient()
        
        print("🔧 Initial Rate Limit Status:")
        initial_status = client.get_rate_limit_status()
        print(f"  Hour Window: {initial_status['hour']['used']}/{initial_status['hour']['limit']}")
        print(f"  Minute Window: {initial_status['minute']['used']}/{initial_status['minute']['limit']}")
        
        # Test multiple requests to same endpoint (should use cache)
        print("\\n🔧 Testing Caching Behavior...")
        start_time = time.time()
        
        # First request
        result1 = await client.get_committees(limit=5)
        first_request_time = time.time() - start_time
        
        # Second request (should be cached)
        start_time2 = time.time()
        result2 = await client.get_committees(limit=5)
        second_request_time = time.time() - start_time2
        
        print(f"  First request time: {first_request_time:.3f}s")
        print(f"  Second request time: {second_request_time:.3f}s")
        
        if second_request_time < first_request_time / 2:
            print("  ✅ Caching appears to be working (faster second request)")
        else:
            print("  ⚠️  Caching may not be working as expected")
        
        # Test rate limit increments
        print("\\n🔧 Testing Rate Limit Tracking...")
        
        # Make several different requests
        test_requests = [
            ("get_committees", lambda: client.get_committees(limit=2)),
            ("get_bills", lambda: client.get_bills(congress=119, limit=2)),
            ("get_members", lambda: client.get_members(congress=119, limit=2)),
        ]
        
        for name, request_func in test_requests:
            try:
                await request_func()
                print(f"  ✅ {name}: Request successful")
                await asyncio.sleep(0.2)  # Small delay between requests
            except Exception as e:
                print(f"  ❌ {name}: Failed - {str(e)}")
        
        # Check final rate limit status
        print("\\n🔧 Final Rate Limit Status:")
        final_status = client.get_rate_limit_status()
        print(f"  Hour Window: {final_status['hour']['used']}/{final_status['hour']['limit']}")
        print(f"  Minute Window: {final_status['minute']['used']}/{final_status['minute']['limit']}")
        
        # Calculate usage
        hour_usage_increase = final_status['hour']['used'] - initial_status['hour']['used']
        minute_usage_increase = final_status['minute']['used'] - initial_status['minute']['used']
        
        print(f"\\n📊 Rate Limit Usage During Test:")
        print(f"  Hour window increase: {hour_usage_increase}")
        print(f"  Minute window increase: {minute_usage_increase}")
        
        # Validate rate limiting is working
        if hour_usage_increase > 0:
            print("  ✅ Rate limiting tracking is working")
        else:
            print("  ⚠️  Rate limiting tracking may not be working")
        
        # Test rate limit safety
        hour_remaining = final_status['hour']['remaining']
        minute_remaining = final_status['minute']['remaining']
        
        print(f"\\n🛡️  Rate Limit Safety Check:")
        print(f"  Hour remaining: {hour_remaining}")
        print(f"  Minute remaining: {minute_remaining}")
        
        if hour_remaining > 4000:  # Should have plenty left
            print("  ✅ Well within hourly rate limits")
        else:
            print("  ⚠️  Approaching hourly rate limit")
            
        if minute_remaining > 50:  # Should have plenty left
            print("  ✅ Well within minute rate limits")
        else:
            print("  ⚠️  Approaching minute rate limit")
        
        print("\\n" + "=" * 60)
        print("✅ Rate Limiting and Caching Test Completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Rate limiting test failed: {e}")
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
    
    success = asyncio.run(test_rate_limiting())
    sys.exit(0 if success else 1)