# Claude Agent SDK Integration with SKILL.md

## Overview

This document explains how the Bedrock PPT Skill integrates with `claude_agent_sdk` using SKILL.md as the capability definition.

## How It Works

### 1. SKILL.md as Capability Definition

The `SKILL.md` file serves as a machine-readable skill definition that:
- Documents all available functions
- Provides function signatures and parameters
- Shows usage examples
- Defines data formats
- Explains error handling

### 2. Integration Flow

```
┌─────────────────┐
│  claude_agent   │
│     _sdk        │
└────────┬────────┘
         │
         ├─ 1. Read SKILL.md
         │     ↓
         │  Parse capabilities
         │     ↓
         ├─ 2. User Prompt
         │     ↓
         │  Understand request
         │     ↓
         ├─ 3. Execute Functions
         │     ↓
         │  Call agent_integration.py
         │     ↓
         └─ 4. Return Results
               ↓
            PowerPoint file
```

## Using claude_agent_sdk with SKILL.md

### Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
# pip install claude-agent-sdk  # When available
```

2. **Configure Environment**
```bash
export AWS_REGION=us-east-1
export ANTHROPIC_MODEL=us.anthropic.claude-sonnet-4-20250514-v1:0
```

### Example Code

```python
from claude_agent_sdk import query, ClaudeAgentOptions
import asyncio
import os

# Read SKILL.md content
from agent_integration import read_skill_file
skill_content = read_skill_file()

async def main():
    options = ClaudeAgentOptions(
        cwd=os.getcwd(),
        model="us.anthropic.claude-sonnet-4-20250514-v1:0",
        system_prompt=f"""You are an expert at creating PowerPoint presentations.

Available capabilities from SKILL.md:
{skill_content}

Use the functions documented in SKILL.md to process data and create presentations.
Available modules: agent_integration, ppt_exporter, excel_reader
""",
        setting_sources=["user", "project"],
        allowed_tools=["Skill", "Read", "Write", "Bash"]
    )
    
    # Agent reads SKILL.md and executes user request
    async for message in query(
        prompt="""
        Read budget.xlsx from current directory and create a PowerPoint presentation.
        Include:
        - Title slide with report name
        - Data overview slide
        - Charts showing financial trends
        - Table with detailed data
        Save as budget_report.pptx
        """,
        options=options
    ):
        print(message)

if __name__ == "__main__":
    asyncio.run(main())
```

## What SKILL.md Provides to the Agent

### 1. Function Discovery
The agent reads SKILL.md to discover available functions:

```markdown
From SKILL.md:

Function: create_presentation()
Function: add_title_slide(prs, title, subtitle)
Function: add_chart_slide(prs, title, chart_data, chart_type)
Function: excel_to_ppt_with_ai(excel_path, output_path)
```

### 2. Parameter Understanding
The agent learns function parameters:

```python
# From SKILL.md
def add_chart_slide(
    prs: Presentation, 
    title: str, 
    chart_data: Dict[str, Any],
    chart_type: str = 'bar'
)

# Chart data format:
{
    'categories': ['Jan', 'Feb', 'Mar'],
    'values': [100, 150, 200],
    'series_name': 'Revenue'
}
```

### 3. Usage Patterns
The agent follows documented usage patterns:

```python
# Pattern from SKILL.md
from ppt_exporter import create_presentation, add_title_slide
prs = create_presentation()
add_title_slide(prs, "Report", "2024")
save_presentation(prs, "output.pptx")
```

### 4. Error Handling
The agent knows how to handle errors:

```python
# From SKILL.md error handling section
try:
    result = excel_to_ppt_with_ai(excel_path)
except FileNotFoundError:
    print("Excel file not found")
except ValueError:
    print("Invalid data format")
```

## Direct Usage (Without SDK)

If `claude_agent_sdk` is not available, you can use the functions directly:

```python
from agent_integration import read_skill_file, process_excel_with_skill

# 1. Read SKILL.md
skill = read_skill_file()
print(f"Loaded skill with {len(skill)} characters")

# 2. Use the skill
result = process_excel_with_skill(
    excel_path="budget.xlsx",
    output_path="report.pptx",
    read_skill=True
)

# 3. Check results
if result['success']:
    print(f"Created: {result['output_path']}")
```

## Key Functions for Agent Integration

### read_skill_file()
```python
def read_skill_file(skill_path: str = None) -> str:
    """
    Read SKILL.md to understand available capabilities.
    Auto-detects SKILL.md location if not specified.
    """
```

### process_excel_with_skill()
```python
def process_excel_with_skill(
    excel_path: str,
    output_path: str = None,
    read_skill: bool = True
) -> Dict[str, Any]:
    """
    Main entry point for agent workflows.
    Reads SKILL.md, processes Excel, creates PPT.
    """
```

### excel_to_ppt_with_ai()
```python
def excel_to_ppt_with_ai(
    excel_path: str,
    output_path: str = None,
    use_bedrock: bool = False
) -> str:
    """
    Convert Excel to PowerPoint with optional AI analysis.
    Can be called directly by claude_agent_sdk.
    """
```

## Benefits of SKILL.md Integration

### For Agents
✅ **Self-documenting**: Agent discovers capabilities automatically  
✅ **Type-aware**: Understands parameters and return types  
✅ **Example-driven**: Learns from documented usage patterns  
✅ **Error-aware**: Knows how to handle errors  

### For Developers
✅ **Single source of truth**: SKILL.md defines the API  
✅ **Version control**: Track capability changes  
✅ **Documentation**: Human and machine readable  
✅ **Extensible**: Add new functions by updating SKILL.md  

## Testing the Integration

### Test 1: Read SKILL.md
```bash
python example_claude_agent_sdk.py
```

This demonstrates:
- Reading SKILL.md
- Parsing capabilities
- Using functions directly
- Creating PowerPoint output

### Test 2: Verify Capabilities
```python
from agent_integration import read_skill_file

skill = read_skill_file()
assert "create_presentation" in skill
assert "add_chart_slide" in skill
assert "excel_to_ppt" in skill
print("✓ All capabilities documented")
```

### Test 3: Direct Function Usage
```python
from agent_integration import excel_to_ppt_with_ai

result = excel_to_ppt_with_ai(
    excel_path="test.xlsx",
    output_path="test.pptx"
)
print(f"✓ Created: {result}")
```

## Comparison: With vs Without SDK

### With claude_agent_sdk
```python
# Agent reads SKILL.md automatically
# Agent interprets user intent
# Agent calls appropriate functions
# Agent handles errors

async for message in query(
    prompt="Create PPT from budget.xlsx",
    options=options
):
    print(message)
```

### Without SDK (Direct)
```python
# Manual: Read SKILL.md
skill = read_skill_file()

# Manual: Call function
result = excel_to_ppt_with_ai("budget.xlsx")

# Manual: Check result
if result:
    print(f"Created: {result}")
```

Both approaches produce the same results!

## Common Use Cases

### Use Case 1: Excel to PPT
```
User: "Convert my sales data to a presentation"
Agent: Reads SKILL.md, finds excel_to_ppt_with_ai()
Agent: Calls function with sales.xlsx
Result: sales_report.pptx created
```

### Use Case 2: Custom Presentation
```
User: "Create a quarterly report with charts"
Agent: Reads SKILL.md, finds create_presentation(), add_chart_slide()
Agent: Creates presentation with specified slides
Result: quarterly_report.pptx created
```

### Use Case 3: Data Analysis + PPT
```
User: "Analyze budget.xlsx and create presentation with insights"
Agent: Reads SKILL.md, finds generate_insights() and excel_to_ppt_with_ai()
Agent: Analyzes data, generates insights, creates PPT
Result: budget_analysis.pptx with AI insights
```

## Troubleshooting

### Issue: SKILL.md not found
**Solution**: Ensure SKILL.md is in the current directory or parent directory

### Issue: Functions not recognized
**Solution**: Check that SKILL.md contains complete function documentation

### Issue: claude_agent_sdk import error
**Solution**: The example works without SDK, showing the pattern for when it's available

## Next Steps

1. **Run the example**: `python example_claude_agent_sdk.py`
2. **Read SKILL.md**: Review complete API documentation
3. **Try direct functions**: Use agent_integration.py functions
4. **Install SDK**: When available, add claude_agent_sdk integration

## Summary

✅ **SKILL.md** serves as the skill definition  
✅ **read_skill_file()** loads the capabilities  
✅ **agent_integration.py** provides the functions  
✅ **claude_agent_sdk** can use the skill (when available)  
✅ **Direct usage** works without SDK  

The source code **is designed** to work with `claude_agent_sdk` through SKILL.md!
