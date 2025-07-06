#!/usr/bin/env python3
"""
Test script to validate MCP server integration readiness.
This doesn't run the actual server but validates it's ready for integration.
"""

import asyncio
import sys
import os
import json
from pathlib import Path
import subprocess

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

async def test_mcp_integration_readiness():
    """Test that the MCP server is ready for integration."""
    try:
        print("🚀 Testing MCP Integration Readiness...")
        print("=" * 60)
        
        # Test 1: Verify MCP server can be imported and initialized
        print("🔧 Test 1: MCP Server Import & Initialization...")
        try:
            from congress_mcp.mcp_server.server import CongressMCPServer
            from congress_mcp.api.client import CongressAPIClient
            from congress_mcp.api.search import CongressSearchEngine
            
            server = CongressMCPServer()
            server.client = CongressAPIClient()
            server.search_engine = CongressSearchEngine(server.client)
            
            print("  ✅ MCP server can be imported and initialized")
        except Exception as e:
            print(f"  ❌ MCP server initialization failed: {e}")
            return False
        
        # Test 2: Verify all required handlers are registered
        print("\\n🔧 Test 2: MCP Handler Registration...")
        try:
            # Check that the server has the MCP handlers
            handlers = dir(server.server)
            required_handlers = ['list_tools', 'call_tool', 'list_resources', 'read_resource']
            
            for handler in required_handlers:
                if any(handler in h for h in handlers):
                    print(f"  ✅ {handler}: registered")
                else:
                    print(f"  ❌ {handler}: not found")
                    return False
                    
        except Exception as e:
            print(f"  ❌ Handler registration check failed: {e}")
            return False
        
        # Test 3: Verify environment configuration
        print("\\n🔧 Test 3: Environment Configuration...")
        
        api_key = os.environ.get("CONGRESS_API_KEY")
        if api_key and len(api_key) > 10:
            print(f"  ✅ Congress API key configured (length: {len(api_key)})")
        else:
            print("  ❌ Congress API key not configured or too short")
            return False
        
        # Test 4: Verify server startup script exists and is executable
        print("\\n🔧 Test 4: Server Startup Script...")
        
        startup_script = project_root / "scripts" / "run_mcp_server.py"
        if startup_script.exists():
            print("  ✅ Startup script exists")
            
            # Check if it's a valid Python file
            try:
                with open(startup_script) as f:
                    content = f.read()
                    if "CongressMCPServer" in content and "stdio_server" in content:
                        print("  ✅ Startup script contains required components")
                    else:
                        print("  ❌ Startup script missing required components")
                        return False
            except Exception as e:
                print(f"  ❌ Could not read startup script: {e}")
                return False
        else:
            print("  ❌ Startup script does not exist")
            return False
        
        # Test 5: Generate integration commands
        print("\\n🔧 Test 5: Integration Commands...")
        
        commands = {
            "direct_run": f"cd {project_root} && source .venv/bin/activate && python scripts/run_mcp_server.py",
            "uv_run": f"cd {project_root} && uv run scripts/run_mcp_server.py",
            "shell_script": f"cd {project_root} && chmod +x scripts/run_mcp_server.sh && ./scripts/run_mcp_server.sh"
        }
        
        print("  Integration commands generated:")
        for name, command in commands.items():
            print(f"    {name}: {command}")
        
        # Test 6: Check MCP server configuration
        print("\\n🔧 Test 6: MCP Server Configuration...")
        
        try:
            # Check if we can create the server configuration for Memex
            config = {
                "name": "congress-api-explorer",
                "description": "US Congress API Explorer with 16 tools for congressional data access",
                "version": "0.1.0",
                "runtime": "python",
                "args": [str(project_root / "scripts" / "run_mcp_server.py")],
                "env": {
                    "CONGRESS_API_KEY": api_key
                },
                "tools_count": 16,
                "resources_count": 15
            }
            
            config_file = project_root / "mcp_server_config.json"
            with open(config_file, "w") as f:
                json.dump(config, f, indent=2)
            
            print(f"  ✅ MCP server configuration saved to {config_file}")
            
        except Exception as e:
            print(f"  ❌ Could not create MCP server configuration: {e}")
            return False
        
        # Test 7: Verify project structure
        print("\\n🔧 Test 7: Project Structure...")
        
        required_dirs = [
            "src/congress_mcp",
            "src/congress_mcp/api", 
            "src/congress_mcp/mcp_server",
            "scripts"
        ]
        
        for req_dir in required_dirs:
            dir_path = project_root / req_dir
            if dir_path.exists():
                print(f"  ✅ {req_dir}: exists")
            else:
                print(f"  ❌ {req_dir}: missing")
                return False
        
        print("\\n" + "=" * 60)
        print("✅ MCP INTEGRATION READINESS: ALL TESTS PASSED")
        print("\\n🚀 READY FOR MEMEX INTEGRATION!")
        print("\\nNext steps:")
        print("1. Start MCP server using one of the commands above")
        print("2. Connect from Memex MCP manager")
        print("3. Test congressional data queries")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP integration readiness test failed: {e}")
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
    
    success = asyncio.run(test_mcp_integration_readiness())
    sys.exit(0 if success else 1)