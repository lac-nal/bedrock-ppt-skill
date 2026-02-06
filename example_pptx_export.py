"""
Example: PPTX Export with A2A Strands Agent

This example demonstrates how to use the A2A agent to generate PowerPoint presentations.
"""
import asyncio
import httpx
import json


async def generate_simple_presentation():
    """Generate a simple presentation"""
    print("\n" + "="*70)
    print("Example 1: Simple Presentation")
    print("="*70)
    
    agent_url = "http://localhost:9009"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Request data
        request_data = {
            "query": "Create a simple presentation",
            "context": {
                "title": "Welcome to A2A Agent",
                "subtitle": "PowerPoint Export Demo",
                "slides": [
                    {
                        "type": "bullet",
                        "title": "Key Features",
                        "bullets": [
                            "Agent-to-Agent communication",
                            "PowerPoint generation",
                            "REST API interface",
                            "Python-based implementation"
                        ]
                    },
                    {
                        "type": "text",
                        "title": "About This Demo",
                        "content": "This presentation was generated automatically by the A2A Strands Agent using the PPTX export capability."
                    }
                ]
            }
        }
        
        # Send request
        print(f"\n📤 Sending request to {agent_url}/invoke...")
        response = await client.post(
            f"{agent_url}/invoke",
            json=request_data
        )
        
        result = response.json()
        print(f"\n✓ Response received:")
        print(f"Status: {result.get('status')}")
        print(f"\nResult:")
        print(result.get('result'))


async def generate_report_presentation():
    """Generate a report-style presentation"""
    print("\n" + "="*70)
    print("Example 2: Report Presentation")
    print("="*70)
    
    agent_url = "http://localhost:9009"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Request data for a report
        request_data = {
            "query": "Generate quarterly report presentation",
            "context": {
                "title": "Q1 2024 Report",
                "subtitle": "Performance Analysis",
                "slides": [
                    {
                        "type": "bullet",
                        "title": "Executive Summary",
                        "bullets": [
                            "Revenue increased by 15%",
                            "Customer base grew by 20%",
                            "New product launched successfully",
                            "Market share expanded to 25%"
                        ]
                    },
                    {
                        "type": "table",
                        "title": "Key Metrics",
                        "data": [
                            ["Metric", "Q1 2023", "Q1 2024", "Change"],
                            ["Revenue", "$1.2M", "$1.38M", "+15%"],
                            ["Customers", "500", "600", "+20%"],
                            ["Market Share", "20%", "25%", "+5%"],
                            ["NPS Score", "72", "78", "+6"]
                        ]
                    },
                    {
                        "type": "bullet",
                        "title": "Next Steps",
                        "bullets": [
                            "Expand to new markets",
                            "Launch marketing campaign",
                            "Hire additional team members",
                            "Improve customer support"
                        ]
                    }
                ]
            }
        }
        
        # Send request
        print(f"\n📤 Sending request to {agent_url}/invoke...")
        response = await client.post(
            f"{agent_url}/invoke",
            json=request_data
        )
        
        result = response.json()
        print(f"\n✓ Response received:")
        print(f"Status: {result.get('status')}")
        print(f"\nResult:")
        print(result.get('result'))


async def generate_custom_presentation():
    """Generate a custom presentation with user input"""
    print("\n" + "="*70)
    print("Example 3: Custom Presentation")
    print("="*70)
    
    agent_url = "http://localhost:9009"
    
    # Get user input
    print("\nEnter presentation details:")
    title = input("Title (or press Enter for default): ").strip()
    if not title:
        title = "My Custom Presentation"
    
    # Create slides
    slides = []
    
    print("\nAdd slides (enter blank title to finish):")
    while True:
        slide_title = input(f"\nSlide {len(slides) + 1} title: ").strip()
        if not slide_title:
            break
        
        print("Enter bullet points (one per line, blank line to finish):")
        bullets = []
        while True:
            bullet = input("  • ").strip()
            if not bullet:
                break
            bullets.append(bullet)
        
        if bullets:
            slides.append({
                "type": "bullet",
                "title": slide_title,
                "bullets": bullets
            })
    
    if not slides:
        print("\nNo slides added. Using default content.")
        slides = [
            {
                "type": "text",
                "title": "Content",
                "content": "This is a custom presentation generated by the A2A agent."
            }
        ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Request data
        request_data = {
            "query": "Generate custom presentation",
            "context": {
                "title": title,
                "slides": slides
            }
        }
        
        # Send request
        print(f"\n📤 Sending request to {agent_url}/invoke...")
        response = await client.post(
            f"{agent_url}/invoke",
            json=request_data
        )
        
        result = response.json()
        print(f"\n✓ Response received:")
        print(f"Status: {result.get('status')}")
        print(f"\nResult:")
        print(result.get('result'))


async def check_agent_capabilities():
    """Check if agent has PPTX capability"""
    print("\n" + "="*70)
    print("Checking Agent Capabilities")
    print("="*70)
    
    agent_url = "http://localhost:9009"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Check health
            print(f"\n📡 Connecting to {agent_url}...")
            health_response = await client.get(f"{agent_url}/health")
            
            if health_response.status_code == 200:
                print("✓ Agent is healthy and responding")
            else:
                print("✗ Agent health check failed")
                return False
            
            # Get agent card
            card_response = await client.get(f"{agent_url}/card")
            card = card_response.json()
            
            print(f"\n📋 Agent Information:")
            print(f"Name: {card.get('name')}")
            print(f"Version: {card.get('version')}")
            print(f"Description: {card.get('description')}")
            print(f"\nCapabilities:")
            for cap in card.get('capabilities', []):
                icon = "✓" if "pptx" in cap.lower() else "•"
                print(f"  {icon} {cap}")
            
            # Check for PPTX capability
            has_pptx = any("pptx" in cap.lower() for cap in card.get('capabilities', []))
            
            if has_pptx:
                print("\n✓ Agent has PPTX export capability!")
                return True
            else:
                print("\n✗ Agent does not have PPTX capability")
                return False
                
    except Exception as e:
        print(f"\n✗ Error connecting to agent: {e}")
        print("\nMake sure the agent server is running:")
        print("  python a2a_agent_server.py")
        return False


async def main():
    """Main example runner"""
    print("\n" + "="*70)
    print("A2A Strands Agent - PPTX Export Examples")
    print("="*70)
    
    # Check agent capabilities
    has_capability = await check_agent_capabilities()
    
    if not has_capability:
        print("\n⚠️  Agent is not running or doesn't have PPTX capability.")
        print("\nPlease start the agent server:")
        print("  python a2a_agent_server.py")
        return
    
    # Run examples
    print("\n" + "="*70)
    print("Running Examples")
    print("="*70)
    
    print("\nSelect an example to run:")
    print("1. Simple Presentation")
    print("2. Report Presentation")
    print("3. Custom Presentation (interactive)")
    print("4. All Examples")
    print("0. Exit")
    
    choice = input("\nEnter choice (0-4): ").strip()
    
    if choice == "1":
        await generate_simple_presentation()
    elif choice == "2":
        await generate_report_presentation()
    elif choice == "3":
        await generate_custom_presentation()
    elif choice == "4":
        await generate_simple_presentation()
        await generate_report_presentation()
    elif choice == "0":
        print("\nExiting...")
        return
    else:
        print("\nInvalid choice")
        return
    
    print("\n" + "="*70)
    print("✓ Examples completed!")
    print("="*70)
    print("\nGenerated PPTX files are saved in the 'output' directory.")
    print("You can open them with Microsoft PowerPoint or compatible software.")


if __name__ == "__main__":
    asyncio.run(main())
