"""
A2A Agent Server
Strands Agents A2A implementation running on port 9009
With PPTX export capability
"""
import os
import json
from typing import Any, Dict, List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn
from pptx_generator import PPTXGenerator, generate_pptx


# Define the Agent's input/output models
class AgentInput(BaseModel):
    """Input model for the agent"""
    query: str = Field(..., description="The query or task for the agent")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class AgentOutput(BaseModel):
    """Output model for the agent"""
    result: str = Field(..., description="The result from the agent")
    status: str = Field(default="success", description="Status of the operation")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class AgentCard(BaseModel):
    """Agent Card - describes the agent's capabilities"""
    name: str = "A2A Strands Agent"
    version: str = "1.0.0"
    description: str = "A2A Agent implementation using Strands Agents framework with PPTX export"
    capabilities: List[str] = [
        "task_execution",
        "query_processing",
        "context_aware_responses",
        "pptx_export",
        "pptx_generation"
    ]
    endpoint: str = "http://localhost:9009"


# Initialize FastAPI app
app = FastAPI(
    title="A2A Strands Agent",
    description="Agent-to-Agent communication using Strands Agents framework",
    version="1.0.0"
)


# Agent implementation class
class StrandsA2AAgent:
    """
    Strands A2A Agent implementation
    """
    
    def __init__(self):
        self.name = "A2A Strands Agent"
        self.version = "1.0.0"
        self.capabilities = [
            "task_execution",
            "query_processing", 
            "context_aware_responses",
            "pptx_export",
            "pptx_generation"
        ]
        self.pptx_generator = PPTXGenerator()
    
    async def process(self, agent_input: AgentInput) -> AgentOutput:
        """
        Process the agent input and return output
        
        Args:
            agent_input: Input data for the agent
            
        Returns:
            AgentOutput: Result from processing
        """
        query = agent_input.query
        context = agent_input.context or {}
        
        # Process the query - this is where your agent logic goes
        result = await self._execute_task(query, context)
        
        return AgentOutput(
            result=result,
            status="success",
            metadata={
                "agent": self.name,
                "version": self.version,
                "processed_query": query
            }
        )
    
    async def _execute_task(self, query: str, context: Dict[str, Any]) -> str:
        """
        Execute the task based on query and context
        
        Args:
            query: The query string
            context: Additional context
            
        Returns:
            str: Result of task execution
        """
        query_lower = query.lower()
        
        # Check if this is a PPTX generation request
        if "pptx" in query_lower or "powerpoint" in query_lower or "presentation" in query_lower:
            return await self._handle_pptx_request(query, context)
        
        # Default processing for non-PPTX requests
        response = f"Processed query: '{query}'"
        
        if context:
            response += f"\nWith context: {list(context.keys())}"
        
        # Add your agent's core logic here
        # For example: data processing, API calls, computations, etc.
        
        return response
    
    async def _handle_pptx_request(self, query: str, context: Dict[str, Any]) -> str:
        """
        Handle PPTX generation request
        
        Args:
            query: The query string
            context: Additional context with presentation details
            
        Returns:
            str: Result with file path and details
        """
        try:
            # Extract presentation details from context
            title = context.get("title", "Generated Presentation")
            subtitle = context.get("subtitle", "")
            slides = context.get("slides", [])
            
            # If slides not provided, create a simple presentation
            if not slides:
                # Create a simple presentation based on query
                slides = [
                    {
                        "type": "text",
                        "title": "Content",
                        "content": query
                    }
                ]
            
            # Generate PPTX
            request_data = {
                "title": title,
                "subtitle": subtitle,
                "slides": slides
            }
            
            result = generate_pptx(request_data)
            
            # Format response
            response = f"✓ PPTX Generated Successfully!\n\n"
            response += f"File: {result['filename']}\n"
            response += f"Path: {result['filepath']}\n"
            response += f"Size: {result['file_size']:,} bytes\n"
            response += f"Slides: {result['slides_count']}\n"
            response += f"\nPresentation ready for download."
            
            return response
            
        except Exception as e:
            return f"Error generating PPTX: {str(e)}"
    
    def get_card(self) -> AgentCard:
        """
        Get the agent card describing capabilities
        
        Returns:
            AgentCard: Agent metadata and capabilities
        """
        return AgentCard(
            name=self.name,
            version=self.version,
            description="A2A Agent implementation using Strands Agents framework with PPTX export",
            capabilities=self.capabilities,
            endpoint="http://localhost:9009"
        )


# Initialize the agent
agent = StrandsA2AAgent()


# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "A2A Strands Agent Server",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/card")
async def get_card():
    """
    Get agent card - describes the agent's capabilities
    """
    return agent.get_card().model_dump()


@app.post("/invoke")
async def invoke(agent_input: AgentInput) -> AgentOutput:
    """
    Main endpoint to invoke the agent
    
    Args:
        agent_input: Input for the agent
        
    Returns:
        AgentOutput: Result from the agent
    """
    try:
        result = await agent.process(agent_input)
        return result
    except Exception as e:
        return AgentOutput(
            result=f"Error processing request: {str(e)}",
            status="error",
            metadata={"error_type": type(e).__name__}
        )


@app.post("/execute")
async def execute(agent_input: AgentInput) -> AgentOutput:
    """
    Alternative endpoint to execute agent tasks
    Alias for /invoke for compatibility
    
    Args:
        agent_input: Input for the agent
        
    Returns:
        AgentOutput: Result from the agent
    """
    return await invoke(agent_input)


def run_server(host: str = "0.0.0.0", port: int = 9009):
    """
    Run the A2A agent server
    
    Args:
        host: Host to bind to
        port: Port to listen on (default: 9009)
    """
    print(f"Starting A2A Strands Agent Server on {host}:{port}")
    print(f"Agent: {agent.name} v{agent.version}")
    print(f"Capabilities: {', '.join(agent.capabilities)}")
    print(f"\nEndpoints:")
    print(f"  - GET  /              : Root endpoint")
    print(f"  - GET  /health        : Health check")
    print(f"  - GET  /card          : Agent card (capabilities)")
    print(f"  - POST /invoke        : Invoke agent")
    print(f"  - POST /execute       : Execute task (alias)")
    print(f"\nServer starting...")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )


if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Get port from environment or use default
    port = int(os.getenv("A2A_AGENT_PORT", "9009"))
    host = os.getenv("A2A_AGENT_HOST", "0.0.0.0")
    
    # Run the server
    run_server(host=host, port=port)
