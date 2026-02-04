"""
Example: Using claude_agent_sdk with Bedrock PPT Skill

This example demonstrates how to use claude_agent_sdk to:
1. Read SKILL.md to understand capabilities
2. Process Excel files and create PowerPoint presentations
3. Use the Bedrock PPT Skill through an agent workflow

Note: This requires claude_agent_sdk to be installed:
    pip install claude-agent-sdk (or your specific SDK package)
"""
import os
import sys
import asyncio
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 80)
print(" " * 20 + "CLAUDE AGENT SDK EXAMPLE")
print(" " * 15 + "Using Bedrock PPT Skill with SKILL.md")
print("=" * 80)

# Check if claude_agent_sdk is available
try:
    # Attempt to import (this is a placeholder - adjust based on actual SDK)
    # from claude_agent_sdk import query, ClaudeAgentOptions
    HAS_CLAUDE_SDK = False  # Set to True when SDK is installed
    print("\n⚠️  Note: claude_agent_sdk not installed or not available")
    print("    This example shows the pattern without requiring the SDK")
except ImportError:
    HAS_CLAUDE_SDK = False
    print("\n⚠️  Note: claude_agent_sdk not installed")
    print("    This example demonstrates the integration pattern")

print("\n" + "-" * 80)
print("Step 1: Reading SKILL.md")
print("-" * 80)

from agent_integration import read_skill_file

# Read SKILL.md to understand capabilities
skill_content = read_skill_file()
print(f"✓ SKILL.md loaded: {len(skill_content)} characters")
print(f"\nFirst 500 characters:")
print("-" * 80)
print(skill_content[:500])
print("-" * 80)

# Parse key capabilities from SKILL.md
print("\n" + "-" * 80)
print("Step 2: Extracting Capabilities from SKILL.md")
print("-" * 80)

capabilities = []
if "analyze_data_with_bedrock" in skill_content:
    capabilities.append("✓ Bedrock data analysis")
if "excel_to_ppt" in skill_content:
    capabilities.append("✓ Excel to PPT conversion")
if "create_presentation" in skill_content:
    capabilities.append("✓ Direct PPT creation")
if "add_chart_slide" in skill_content:
    capabilities.append("✓ Chart generation")
if "add_table_slide" in skill_content:
    capabilities.append("✓ Table creation")

print("Detected capabilities:")
for cap in capabilities:
    print(f"  {cap}")

# Demonstrate the pattern that would be used with claude_agent_sdk
print("\n" + "=" * 80)
print("Step 3: Claude Agent SDK Integration Pattern")
print("=" * 80)

print("""
When using claude_agent_sdk, you would set it up like this:

```python
from claude_agent_sdk import query, ClaudeAgentOptions
import asyncio
import os

# Configure environment
os.environ["CLAUDE_CODE_USE_BEDROCK"] = "1"
os.environ["AWS_REGION"] = "us-east-1"
os.environ["ANTHROPIC_MODEL"] = "us.anthropic.claude-sonnet-4-20250514-v1:0"

async def main():
    # Set up options
    options = ClaudeAgentOptions(
        cwd=os.getcwd(),
        model="us.anthropic.claude-sonnet-4-20250514-v1:0",
        system_prompt=f'''You are an expert at creating PowerPoint presentations.
        
Available capabilities from SKILL.md:
{skill_content[:1000]}

Use the agent_integration.py module to process data and create presentations.
''',
        setting_sources=["user", "project"],
        allowed_tools=["Skill", "Read", "Write", "Bash"]
    )
    
    # Query the agent
    async for message in query(
        prompt=\"""
Read SKILL.md and understand the available functions.
Then read budget.xlsx and create a PowerPoint presentation with:
- Title slide
- Data overview
- Charts showing trends
- Summary table
Save it as budget_report.pptx
\""",
        options=options
    ):
        print(message)

if __name__ == "__main__":
    asyncio.run(main())
```
""")

# Demonstrate without SDK - direct function calls
print("\n" + "=" * 80)
print("Step 4: Direct Function Call (Without SDK)")
print("=" * 80)

print("\nSince claude_agent_sdk is not installed, demonstrating direct usage:")

from agent_integration import process_excel_with_skill
from excel_to_ppt_example import create_sample_budget_excel

# Create sample data
print("\n1. Creating sample Excel file...")
sample_excel = create_sample_budget_excel()
print(f"   ✓ Created: {sample_excel}")

# Process using the skill (as the agent would)
print("\n2. Processing with Bedrock PPT Skill...")
print("   (This is what claude_agent_sdk would call internally)")

result = process_excel_with_skill(
    excel_path=sample_excel,
    output_path="output/agent_sdk_example_output.pptx",
    read_skill=True  # Agent reads SKILL.md first
)

print("\n3. Results:")
if result['success']:
    print(f"   ✓ Success!")
    print(f"   ✓ Output: {result['output_path']}")
    print(f"   ✓ SKILL.md was read: {'Yes' if result['skill_content'] else 'No'}")
else:
    print(f"   ✗ Error: {result['error']}")

# Show how agent would understand capabilities
print("\n" + "=" * 80)
print("Step 5: How Agent Understands Capabilities from SKILL.md")
print("=" * 80)

print("""
The agent (claude_agent_sdk) would:

1. READ SKILL.md to discover:
   - Available functions and their signatures
   - Input/output formats
   - Usage examples
   - Error handling patterns

2. PARSE the skill definition to understand:
   - Function: create_presentation() - Creates new PPT
   - Function: add_title_slide() - Adds title
   - Function: add_chart_slide() - Adds charts
   - Function: add_table_slide() - Adds tables
   - Function: excel_to_ppt_with_ai() - Excel conversion

3. USE the functions based on user prompts:
   User: "Create a PPT from budget.xlsx"
   Agent: Reads SKILL.md, finds excel_to_ppt_with_ai(), calls it

4. RETURN results to user:
   Agent: "Created budget_report.pptx with 5 slides"
""")

print("\n" + "=" * 80)
print("Summary")
print("=" * 80)

print("""
✅ SKILL.md Integration:
   - SKILL.md provides complete API documentation
   - Agent reads it to understand capabilities
   - Agent uses functions as documented

✅ Integration Pattern:
   - read_skill_file() to load SKILL.md
   - Parse capabilities from content
   - Use agent_integration.py functions
   - Return results

✅ What claude_agent_sdk Would Do:
   1. Read SKILL.md automatically
   2. Understand available functions
   3. Execute user requests using the skill
   4. Create PowerPoint presentations

✅ Without SDK:
   - Direct function calls work the same way
   - Read SKILL.md manually
   - Call functions directly
   - Same results

To use with actual claude_agent_sdk:
   pip install claude-agent-sdk
   Then uncomment the SDK imports in this file
""")

print("\n" + "=" * 80)
print("Example Complete!")
print("=" * 80)
print(f"\nGenerated file: output/agent_sdk_example_output.pptx")
print("This demonstrates the pattern for claude_agent_sdk integration.\n")
