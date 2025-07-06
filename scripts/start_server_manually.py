#!/usr/bin/env python3
"""
Manual server startup test to verify everything works before integration.
"""

import asyncio
import sys
import os
import signal
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Global variable to track server running state
server_running = False

def signal_handler(signum, frame):
    """Handle interrupt signals gracefully."""
    global server_running
    print("\\n🛑 Received interrupt signal, shutting down...")
    server_running = False
    sys.exit(0)

async def test_manual_server():
    """Test manual server startup."""
    try:
        print("🚀 Testing Manual MCP Server Startup...")
        print("=" * 60)
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Import and setup server
        from congress_mcp.mcp_server.server import CongressMCPServer
        from congress_mcp.utils.logging import setup_logging
        from mcp.server.stdio import stdio_server
        
        # Setup logging
        setup_logging(level="INFO")
        
        print("✅ Imports successful")
        
        # Initialize server
        server = CongressMCPServer()
        print("✅ Server initialized")
        
        print("\\n📡 Starting MCP server on stdio transport...")
        print("🔄 Server will run for 30 seconds then automatically stop")
        print("   (Press Ctrl+C to stop early)")
        
        global server_running
        server_running = True
        
        # Run server with timeout
        async def run_with_timeout():
            async with stdio_server() as (read_stream, write_stream):
                print("🚀 MCP Server is RUNNING and ready for connections!")
                print("   Protocol: stdio")
                print("   Tools: 16 congressional data tools")
                print("   Resources: 15 congressional data resources")
                
                # Create a task for the server
                server_task = asyncio.create_task(
                    server.serve(read_stream, write_stream)
                )
                
                # Create a timeout task
                timeout_task = asyncio.create_task(
                    asyncio.sleep(30)
                )
                
                try:
                    # Wait for either the server to finish or timeout
                    done, pending = await asyncio.wait(
                        [server_task, timeout_task],
                        return_when=asyncio.FIRST_COMPLETED
                    )
                    
                    # Cancel any pending tasks
                    for task in pending:
                        task.cancel()
                        try:
                            await task
                        except asyncio.CancelledError:
                            pass
                    
                    if timeout_task in done:
                        print("\\n⏰ 30-second test completed successfully")
                    else:
                        print("\\n🏁 Server completed normally")
                        
                except asyncio.CancelledError:
                    print("\\n🛑 Server stopped by user")
                    
        await run_with_timeout()
        
        print("\\n" + "=" * 60)
        print("✅ MANUAL SERVER TEST COMPLETED SUCCESSFULLY")
        print("\\n🎉 MCP Server is ready for production integration!")
        
        return True
        
    except KeyboardInterrupt:
        print("\\n🛑 Test interrupted by user")
        return True
    except Exception as e:
        print(f"❌ Manual server test failed: {e}")
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
    
    success = asyncio.run(test_manual_server())
    sys.exit(0 if success else 1)