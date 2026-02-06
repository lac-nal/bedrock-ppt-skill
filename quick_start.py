#!/usr/bin/env python3
"""
Quick Start Script
Demonstrates A2A Agent and Orchestrator setup
"""
import asyncio
import sys
import time
from multiprocessing import Process
import requests


def start_agent_server():
    """Start the A2A agent server"""
    from a2a_agent_server import run_server
    run_server(host="127.0.0.1", port=9009)


def wait_for_agent(max_wait=10):
    """Wait for agent to be ready"""
    print("Waiting for agent to start...")
    for i in range(max_wait):
        try:
            response = requests.get("http://localhost:9009/health", timeout=1)
            if response.status_code == 200:
                print("✓ Agent is ready!")
                return True
        except:
            pass
        time.sleep(1)
        print(f"  Waiting... ({i+1}/{max_wait})")
    return False


async def run_orchestrator_demo():
    """Run orchestrator demo"""
    from orchestrator import Orchestrator
    
    orchestrator = Orchestrator(agent_url="http://localhost:9009")
    
    # Start and verify connection
    started = await orchestrator.start()
    if not started:
        print("Error: Could not connect to agent")
        return False
    
    # Run demo tasks
    print("\nRunning demo tasks...\n")
    
    await orchestrator.run_task(
        query="Hello, A2A Strands Agent!",
        context={"demo": True, "task": "greeting"}
    )
    
    await orchestrator.run_task(
        query="Analyze data and provide insights",
        context={"data": [10, 20, 30, 40, 50], "operation": "analysis"}
    )
    
    # Close
    await orchestrator.close()
    return True


def main():
    """Main function"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║         A2A Strands Agent - Quick Start                   ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    print("Step 1: Starting A2A Agent Server on port 9009...")
    print("-" * 60)
    
    # Start agent server in separate process
    agent_process = Process(target=start_agent_server, daemon=True)
    agent_process.start()
    
    # Wait for agent to be ready
    if not wait_for_agent():
        print("\n✗ Agent failed to start")
        agent_process.terminate()
        return 1
    
    print("\n" + "="*60)
    print("Step 2: Running Orchestrator Demo")
    print("="*60)
    
    try:
        # Run orchestrator
        success = asyncio.run(run_orchestrator_demo())
        
        if success:
            print("\n" + "="*60)
            print("✓ Demo completed successfully!")
            print("="*60)
            print("\nNext steps:")
            print("  1. Review the code in a2a_agent_server.py")
            print("  2. Review the code in orchestrator.py")
            print("  3. Customize agent capabilities for your use case")
            print("  4. See README.md for more details")
            return 0
        else:
            print("\n✗ Demo failed")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
        return 0
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Cleanup
        agent_process.terminate()
        agent_process.join(timeout=2)
        print("\n✓ Cleanup complete")


if __name__ == "__main__":
    sys.exit(main())
