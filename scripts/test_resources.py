#!/usr/bin/env python3
"""
Test script for MCP resources and health endpoints.
Validates all resource endpoints and health monitoring systems.
"""

import asyncio
import sys
import os
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

async def test_resources():
    """Test MCP resources and health monitoring."""
    try:
        from congress_mcp.mcp_server.server import CongressMCPServer
        from congress_mcp.api.client import CongressAPIClient
        from congress_mcp.api.search import CongressSearchEngine
        from congress_mcp.utils.logging import setup_logging
        
        # Setup logging (quiet for testing)
        setup_logging(level="WARNING")
        
        print("🚀 Testing MCP Resources and Health Systems...")
        print("=" * 60)
        
        # Initialize server
        server = CongressMCPServer()
        server.client = CongressAPIClient()
        server.search_engine = CongressSearchEngine(server.client)
        
        # Test resource URIs to check
        test_resources = [
            "congress://committees/current",
            "congress://committees/house",
            "congress://committees/senate", 
            "congress://hearings/recent",
            "congress://hearings/house",
            "congress://hearings/senate",
            "congress://bills/recent",
            "congress://bills/house",
            "congress://bills/senate",
            "congress://members/current",
            "congress://members/house",
            "congress://members/senate",
            "congress://status/current",
            "congress://status/rate-limits",
            "congress://status/health"
        ]
        
        passed_resources = 0
        failed_resources = 0
        
        print("🔧 Testing Resources...")
        for uri in test_resources:
            try:
                result = await server._read_resource(uri)
                if result and len(str(result)) > 10:
                    print(f"  ✅ {uri}: PASSED ({len(str(result))} chars)")
                    passed_resources += 1
                else:
                    print(f"  ⚠️  {uri}: EMPTY RESULT")
                    failed_resources += 1
            except Exception as e:
                print(f"  ❌ {uri}: FAILED - {str(e)}")
                failed_resources += 1
                
            # Small delay to respect rate limits
            await asyncio.sleep(0.1)
        
        print("\\n" + "=" * 60)
        
        # Test specific health endpoints
        print("🔧 Testing Health Monitoring...")
        
        # Test health status
        try:
            health_result = await server._call_tool("get_health_status", {})
            print(f"  ✅ Health Status: PASSED ({len(str(health_result))} chars)")
            health_passed = True
        except Exception as e:
            print(f"  ❌ Health Status: FAILED - {str(e)}")
            health_passed = False
        
        # Test system metrics
        try:
            metrics_result = await server._call_tool("get_system_metrics", {})
            print(f"  ✅ System Metrics: PASSED ({len(str(metrics_result))} chars)")
            metrics_passed = True
        except Exception as e:
            print(f"  ❌ System Metrics: FAILED - {str(e)}")
            metrics_passed = False
        
        # Test rate limiting
        try:
            rate_result = await server._call_tool("get_rate_limit_status", {})
            print(f"  ✅ Rate Limits: PASSED ({len(str(rate_result))} chars)")
            rate_passed = True
        except Exception as e:
            print(f"  ❌ Rate Limits: FAILED - {str(e)}")
            rate_passed = False
        
        print("\\n" + "=" * 60)
        print("📊 RESOURCE & HEALTH TEST SUMMARY")
        print(f"✅ RESOURCES PASSED: {passed_resources}")
        print(f"❌ RESOURCES FAILED: {failed_resources}")
        
        health_total = sum([health_passed, metrics_passed, rate_passed])
        print(f"✅ HEALTH CHECKS PASSED: {health_total}/3")
        
        total_tests = passed_resources + failed_resources + 3
        total_passed = passed_resources + health_total
        success_rate = (total_passed / total_tests) * 100
        
        print(f"📈 OVERALL SUCCESS RATE: {success_rate:.1f}%")
        
        # Test API connectivity and caching
        print("\\n🔧 Testing API Connectivity & Caching...")
        try:
            # Test API call
            committees = await server.client.get_committees(limit=2)
            print("  ✅ Congress API: CONNECTED")
            
            # Test cache functionality 
            if hasattr(server.client, '_cache'):
                print(f"  ✅ Cache: OPERATIONAL")
            else:
                print("  ⚠️  Cache: STATUS UNKNOWN")
                
        except Exception as e:
            print(f"  ❌ API/Cache Test: FAILED - {str(e)}")
        
        # Save results
        results = {
            "resource_tests": {
                "passed": passed_resources,
                "failed": failed_resources,
                "total": len(test_resources)
            },
            "health_tests": {
                "health_status": health_passed,
                "system_metrics": metrics_passed,
                "rate_limits": rate_passed
            },
            "overall": {
                "success_rate": success_rate,
                "total_tests": total_tests,
                "total_passed": total_passed
            }
        }
        
        results_file = project_root / "resource_test_results.json"
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\\n📁 Results saved to: {results_file}")
        
        return failed_resources == 0 and health_total == 3
        
    except Exception as e:
        print(f"❌ Resource testing failed: {e}")
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
    
    success = asyncio.run(test_resources())
    sys.exit(0 if success else 1)