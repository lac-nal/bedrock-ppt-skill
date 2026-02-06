# A2A Strands Agent System

A distributed agent system using the Strands Agents A2A (Agent-to-Agent) protocol.

## Architecture

```
┌─────────────────────┐
│   Orchestrator      │  ← Client that calls the agent
│  (orchestrator.py)  │
└──────────┬──────────┘
           │ HTTP/REST
           ↓
┌─────────────────────┐
│  A2A Agent Server   │  ← Agent running on port 9009
│ (a2a_agent_server.py)│
└─────────────────────┘
```

## Components

### 1. A2A Agent Server (`a2a_agent_server.py`)
- Runs on port 9009
- Implements the A2A protocol
- Provides REST API endpoints for agent invocation
- Built with FastAPI and Strands Agents framework

**Endpoints:**
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /card` - Get agent capabilities
- `POST /invoke` - Invoke the agent
- `POST /execute` - Execute task (alias)

### 2. Orchestrator (`orchestrator.py`)
- Client that calls the A2A agent
- Manages task execution and workflow
- Handles communication with agent on port 9009
- Demonstrates agent invocation patterns

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Start the A2A Agent Server

```bash
python a2a_agent_server.py
```

The agent will start on port 9009 and display:
```
Starting A2A Strands Agent Server on 0.0.0.0:9009
Agent: A2A Strands Agent v1.0.0
Capabilities: task_execution, query_processing, context_aware_responses
...
```

### Step 2: Run the Orchestrator

In a new terminal:

```bash
python orchestrator.py
```

The orchestrator will:
1. Connect to the agent on port 9009
2. Check agent health
3. Retrieve agent capabilities
4. Execute example tasks
5. Display results

## Configuration

### Environment Variables

Create a `.env` file:

```bash
# Agent Server Configuration
A2A_AGENT_PORT=9009
A2A_AGENT_HOST=0.0.0.0

# Orchestrator Configuration
A2A_AGENT_URL=http://localhost:9009
```

## API Examples

### Using curl

**Check agent health:**
```bash
curl http://localhost:9009/health
```

**Get agent card:**
```bash
curl http://localhost:9009/card
```

**Invoke agent:**
```bash
curl -X POST http://localhost:9009/invoke \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello agent", "context": {"user": "test"}}'
```

### Using Python

```python
import asyncio
from orchestrator import Orchestrator

async def main():
    # Create orchestrator
    orch = Orchestrator(agent_url="http://localhost:9009")
    
    # Start and connect
    await orch.start()
    
    # Run a task
    result = await orch.run_task(
        query="Process this request",
        context={"data": "example"}
    )
    
    # Close
    await orch.close()

asyncio.run(main())
```

## Development

### Adding Agent Capabilities

To add new capabilities to the agent, modify `a2a_agent_server.py`:

1. Update the `capabilities` list in `StrandsA2AAgent.__init__()`
2. Implement logic in `_execute_task()` method
3. Update the agent card in `get_card()` method

Example:

```python
async def _execute_task(self, query: str, context: Dict[str, Any]) -> str:
    # Your custom logic here
    if "data_analysis" in query.lower():
        return await self._analyze_data(context)
    elif "report" in query.lower():
        return await self._generate_report(context)
    else:
        return f"Processed: {query}"
```

### Testing

**Test agent server:**
```bash
# Start server
python a2a_agent_server.py

# In another terminal
curl http://localhost:9009/health
```

**Test orchestrator:**
```bash
# With server running
python orchestrator.py
```

## Strands Agents Framework

This implementation uses the [Strands Agents](https://strandsagents.com) A2A protocol:

- **Documentation**: https://strandsagents.com/latest/documentation/
- **A2A API Reference**: https://strandsagents.com/latest/documentation/docs/api-reference/python/agent/a2a_agent/
- **A2A Protocol**: https://a2a-protocol.org/

### Key Features

- **Distributed**: Agents run as independent services
- **Scalable**: Horizontal scaling with load balancing
- **Protocol-based**: Standard A2A protocol for interoperability
- **FastAPI**: Built on modern async Python framework
- **Type-safe**: Pydantic models for input/output validation

## Troubleshooting

### Agent not responding
- Check if agent server is running: `curl http://localhost:9009/health`
- Verify port 9009 is not in use: `lsof -i :9009`
- Check logs for errors

### Connection refused
- Ensure agent server started successfully
- Verify firewall settings allow port 9009
- Check agent URL in orchestrator configuration

### Import errors
- Install dependencies: `pip install -r requirements.txt`
- Verify Python version: `python --version` (should be 3.8+)

## Project Structure

```
.
├── a2a_agent_server.py    # A2A agent server (port 9009)
├── orchestrator.py        # Orchestrator client
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## License

MIT License

## Resources

- [Strands Agents Documentation](https://strandsagents.com/latest/documentation/)
- [A2A Protocol Specification](https://a2a-protocol.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Support

For issues or questions:
1. Check the [Strands Agents documentation](https://strandsagents.com)
2. Review agent logs for errors
3. Verify network connectivity between orchestrator and agent

---

**Built with Strands Agents A2A Protocol**
