"""
Orchestrator - A2A Agent Client
Calls the A2A Strands Agent running on port 9009
"""
import asyncio
import os
import sys
from typing import Any, Dict, Optional
import httpx
from pydantic import BaseModel, Field


class AgentInput(BaseModel):
    """Input model for the agent"""
    query: str = Field(..., description="The query or task for the agent")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class AgentOutput(BaseModel):
    """Output model from the agent"""
    result: str
    status: str
    metadata: Optional[Dict[str, Any]] = None


class A2AOrchestratorClient:
    """
    Orchestrator client for calling A2A Strands Agent
    """
    
    def __init__(self, agent_url: str = "http://localhost:9009"):
        """
        Initialize the orchestrator client
        
        Args:
            agent_url: Base URL of the A2A agent server
        """
        self.agent_url = agent_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    async def check_health(self) -> bool:
        """
        Check if the agent server is healthy
        
        Returns:
            bool: True if healthy, False otherwise
        """
        try:
            response = await self.client.get(f"{self.agent_url}/health")
            return response.status_code == 200
        except Exception as e:
            print(f"Health check failed: {e}")
            return False
    
    async def get_agent_card(self) -> Optional[Dict[str, Any]]:
        """
        Get the agent card describing capabilities
        
        Returns:
            Dict with agent metadata and capabilities, or None if failed
        """
        try:
            response = await self.client.get(f"{self.agent_url}/card")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get agent card: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting agent card: {e}")
            return None
    
    async def invoke_agent(
        self, 
        query: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[AgentOutput]:
        """
        Invoke the A2A agent with a query
        
        Args:
            query: The query or task for the agent
            context: Optional additional context
            
        Returns:
            AgentOutput: Result from the agent, or None if failed
        """
        try:
            agent_input = AgentInput(query=query, context=context)
            
            response = await self.client.post(
                f"{self.agent_url}/invoke",
                json=agent_input.model_dump()
            )
            
            if response.status_code == 200:
                data = response.json()
                return AgentOutput(**data)
            else:
                print(f"Agent invocation failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error invoking agent: {e}")
            return None
    
    async def execute_task(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[AgentOutput]:
        """
        Execute a task on the A2A agent
        Alias for invoke_agent using /execute endpoint
        
        Args:
            query: The query or task for the agent
            context: Optional additional context
            
        Returns:
            AgentOutput: Result from the agent, or None if failed
        """
        try:
            agent_input = AgentInput(query=query, context=context)
            
            response = await self.client.post(
                f"{self.agent_url}/execute",
                json=agent_input.model_dump()
            )
            
            if response.status_code == 200:
                data = response.json()
                return AgentOutput(**data)
            else:
                print(f"Task execution failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error executing task: {e}")
            return None


class Orchestrator:
    """
    Main Orchestrator class
    Manages communication with A2A agent on port 9009
    """
    
    def __init__(self, agent_url: str = "http://localhost:9009"):
        """
        Initialize the orchestrator
        
        Args:
            agent_url: URL of the A2A agent server
        """
        self.agent_url = agent_url
        self.client = A2AOrchestratorClient(agent_url)
        print(f"Orchestrator initialized")
        print(f"Target agent: {agent_url}")
    
    async def start(self):
        """Start the orchestrator and verify agent connection"""
        print("\n" + "="*60)
        print("Starting Orchestrator")
        print("="*60)
        
        # Check agent health
        print(f"\nChecking agent health at {self.agent_url}...")
        is_healthy = await self.client.check_health()
        
        if is_healthy:
            print("✓ Agent is healthy and responding")
        else:
            print("✗ Agent is not responding")
            print(f"  Make sure the agent server is running on {self.agent_url}")
            return False
        
        # Get agent card
        print("\nFetching agent capabilities...")
        card = await self.client.get_agent_card()
        
        if card:
            print("✓ Agent card retrieved:")
            print(f"  Name: {card.get('name')}")
            print(f"  Version: {card.get('version')}")
            print(f"  Description: {card.get('description')}")
            print(f"  Capabilities: {', '.join(card.get('capabilities', []))}")
        else:
            print("✗ Could not retrieve agent card")
        
        print("\n" + "="*60)
        print("Orchestrator ready")
        print("="*60 + "\n")
        
        return True
    
    async def run_task(self, query: str, context: Optional[Dict[str, Any]] = None):
        """
        Run a task by calling the A2A agent
        
        Args:
            query: The query or task description
            context: Optional context data
        """
        print(f"\n{'='*60}")
        print(f"Executing task via A2A agent")
        print(f"{'='*60}")
        print(f"Query: {query}")
        if context:
            print(f"Context: {context}")
        
        # Invoke the agent
        print(f"\nInvoking agent at {self.agent_url}...")
        result = await self.client.invoke_agent(query, context)
        
        if result:
            print(f"\n{'='*60}")
            print("Result received:")
            print(f"{'='*60}")
            print(f"Status: {result.status}")
            print(f"Result: {result.result}")
            if result.metadata:
                print(f"Metadata: {result.metadata}")
            print(f"{'='*60}\n")
        else:
            print("✗ Failed to get result from agent\n")
        
        return result
    
    async def close(self):
        """Close the orchestrator and cleanup"""
        await self.client.close()
        print("Orchestrator closed")


async def main():
    """Main function to run the orchestrator"""
    # Get agent URL from environment or use default
    agent_url = os.getenv("A2A_AGENT_URL", "http://localhost:9009")
    
    # Create orchestrator
    orchestrator = Orchestrator(agent_url=agent_url)
    
    # Start orchestrator
    started = await orchestrator.start()
    
    if not started:
        print("\nError: Could not connect to agent")
        print("Please ensure the agent server is running:")
        print("  python a2a_agent_server.py")
        return
    
    # Example tasks
    print("\nRunning example tasks...\n")
    
    # Task 1: Simple query
    await orchestrator.run_task(
        query="Hello, what can you do?",
        context={"user": "orchestrator", "task_id": 1}
    )
    
    # Task 2: Processing task
    await orchestrator.run_task(
        query="Process this data and return insights",
        context={
            "data": {"values": [1, 2, 3, 4, 5]},
            "operation": "analyze"
        }
    )
    
    # Task 3: Complex query
    await orchestrator.run_task(
        query="Generate a summary report",
        context={
            "report_type": "quarterly",
            "include_charts": True
        }
    )
    
    # Close orchestrator
    await orchestrator.close()
    
    print("\n" + "="*60)
    print("Orchestrator completed")
    print("="*60)


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║       A2A Strands Agent Orchestrator                      ║
    ║       Calls A2A Agent on port 9009                        ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nOrchestrator interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError running orchestrator: {e}")
        sys.exit(1)
