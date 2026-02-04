# Claude Agent SDK Integration Guide

This guide shows how to integrate the Bedrock PPT Skill with `claude_agent_sdk` to read Excel files and create PowerPoint presentations.

## Overview

The Bedrock PPT Skill now supports:
- ✅ Reading Excel files (.xlsx, .xls)
- ✅ Reading SKILL.md for capability discovery
- ✅ Creating PowerPoint presentations with charts and tables
- ✅ Compatible with claude_agent_sdk workflows
- ✅ Optional AI-powered insights with Amazon Bedrock

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- boto3 (AWS SDK)
- python-pptx (PowerPoint generation)
- pandas (data processing)
- openpyxl (Excel reading)
- python-dotenv (configuration)

### 2. Basic Usage

```python
from agent_integration import excel_to_ppt_with_ai

# Convert Excel to PowerPoint
result = excel_to_ppt_with_ai(
    excel_path="budget.xlsx",
    output_path="budget_report.pptx",
    use_bedrock=False  # Set to True for AI insights
)

print(f"PowerPoint created: {result}")
```

### 3. Command Line Usage

```bash
# Convert Excel to PowerPoint
python agent_integration.py budget.xlsx --output report.pptx

# With AI insights (requires AWS credentials)
python agent_integration.py budget.xlsx --output report.pptx --with-ai

# Run demo mode
python agent_integration.py
```

## Integration with claude_agent_sdk

### Pattern 1: Direct Integration

The skill provides a function that matches the pattern in your code:

```python
from agent_integration import process_excel_with_skill

# Process Excel file and create PPT
result = process_excel_with_skill(
    excel_path="D:\\NLS\\New folder (2)\\budget.xlsx",
    output_path="D:\\NLS\\New folder (2)\\budget_report.pptx",
    read_skill=True  # Automatically reads SKILL.md
)

if result['success']:
    print(f"Success! PPT created at: {result['output_path']}")
else:
    print(f"Error: {result['error']}")
```

### Pattern 2: With claude_agent_sdk

If you're using `claude_agent_sdk`, you can integrate like this:

```python
from claude_agent_sdk import query, ClaudeAgentOptions
import asyncio
import os

os.environ["CLAUDE_CODE_USE_BEDROCK"] = "1"
os.environ["AWS_REGION"] = "us-east-1"
os.environ["ANTHROPIC_MODEL"] = "us.anthropic.claude-sonnet-4-20250514-v1:0"
os.environ["AWS_ACCESS_KEY_ID"] = "your_access_key_id_here"
os.environ["AWS_SECRET_ACCESS_KEY"] = "your_secret_access_key_here"

async def main():
    options = ClaudeAgentOptions(
        cwd="D:\\NLS\\New folder (2)",
        model="us.anthropic.claude-sonnet-4-20250514-v1:0",
        system_prompt="You are an expert at creating PowerPoint presentations from data. Use the Bedrock PPT Skill to read Excel files and create presentations.",
        setting_sources=["user", "project"],
        allowed_tools=["Skill", "Read", "Write", "Bash"]
    )

    async for message in query(
        prompt="""
        Read budget.xlsx from path: D:\\NLS\\New folder (2) 
        and create a pptx file with the budget data into slides. 
        Save output to: D:\\NLS\\New folder (2)\\budget_report.pptx
        
        Use the agent_integration.py script to process the Excel file.
        First, read SKILL.md to understand the capabilities.
        """,
        options=options
    ):
        print(message)

if __name__ == "__main__":
    asyncio.run(main())
```

### Pattern 3: Step-by-Step with Skill Reading

```python
import sys
import os

# Add skill directory to path
sys.path.insert(0, "path/to/bedrock-ppt-skill")

from agent_integration import read_skill_file, excel_to_ppt_with_ai

# Step 1: Read SKILL.md to understand capabilities
skill_content = read_skill_file()
print(f"Skill loaded: {len(skill_content)} characters")
print("\nSkill Overview:")
print(skill_content[:500])  # Print first 500 chars

# Step 2: Process Excel file
excel_path = "D:\\NLS\\New folder (2)\\budget.xlsx"
output_path = "D:\\NLS\\New folder (2)\\budget_report.pptx"

result = excel_to_ppt_with_ai(
    excel_path=excel_path,
    output_path=output_path,
    use_bedrock=False  # Can enable AI if credentials configured
)

print(f"\nPowerPoint created: {result}")
```

## SKILL.md Reading

The skill automatically reads SKILL.md to understand available functions:

```python
from agent_integration import read_skill_file

# Read skill documentation
skill = read_skill_file()

# The skill documentation contains:
# - Function signatures
# - Usage examples
# - Data format specifications
# - Error handling guidelines
# - Integration patterns

print(f"Skill documentation: {len(skill)} characters")
```

## Excel File Processing

### Supported Excel Features

- ✅ Multiple sheets (reads first by default)
- ✅ Numeric data (automatic chart generation)
- ✅ Text data (table generation)
- ✅ Headers and column names
- ✅ Summary statistics calculation

### Excel Data Structure

The skill works best with Excel files structured like:

```
| Category  | Q1_Budget | Q1_Actual | Q2_Budget | Q2_Actual |
|-----------|-----------|-----------|-----------|-----------|
| Salaries  | 150000    | 155000    | 150000    | 152000    |
| Marketing | 50000     | 48000     | 60000     | 65000     |
| ...       | ...       | ...       | ...       | ...       |
```

### Generated PowerPoint Structure

The created PowerPoint includes:

1. **Title Slide** - File name and date
2. **Data Overview** - File info, row/column counts
3. **Data Table** - Full data display (up to 20 rows)
4. **Charts** - Automatic chart generation for numeric columns
5. **AI Insights** (optional) - If Bedrock is enabled

## Advanced Usage

### Custom Excel Processing

```python
from excel_reader import (
    read_excel_file,
    prepare_chart_data_from_df,
    prepare_table_data_from_df
)
from ppt_exporter import (
    create_presentation,
    add_title_slide,
    add_chart_slide,
    add_table_slide,
    save_presentation
)

# Read Excel
df = read_excel_file("budget.xlsx")

# Create presentation
prs = create_presentation()
add_title_slide(prs, "Budget Report", "2024 Analysis")

# Add custom table
table_data = prepare_table_data_from_df(df)
add_table_slide(prs, "Budget Details", table_data)

# Add custom chart
chart_data = prepare_chart_data_from_df(df, "Category", "Q1_Budget")
add_chart_slide(prs, "Q1 Budget", chart_data, chart_type='bar')

# Save
save_presentation(prs, "custom_report.pptx")
```

### With AI Insights

```python
from agent_integration import excel_to_ppt_with_ai

# Enable AI insights (requires AWS credentials in environment)
result = excel_to_ppt_with_ai(
    excel_path="budget.xlsx",
    output_path="budget_ai_report.pptx",
    use_bedrock=True  # Enable AI analysis
)
```

## Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# Bedrock Model (optional)
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0

# Output directory (optional)
PPT_OUTPUT_DIR=./output
```

### AWS Credentials

For AWS Bedrock integration:

1. Configure AWS credentials:
   ```bash
   aws configure
   ```

2. Or use environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=your_key
   export AWS_SECRET_ACCESS_KEY=your_secret
   export AWS_REGION=us-east-1
   ```

3. Or use IAM roles (recommended for EC2/Lambda)

## Examples

### Example 1: Simple Conversion

```bash
python agent_integration.py budget.xlsx
```

Output: `budget_report.pptx` in the same directory

### Example 2: Custom Output Path

```bash
python agent_integration.py budget.xlsx --output /path/to/report.pptx
```

### Example 3: With AI Analysis

```bash
python agent_integration.py budget.xlsx --output report.pptx --with-ai
```

### Example 4: Programmatic Usage

```python
from agent_integration import process_excel_with_skill

result = process_excel_with_skill(
    excel_path="budget.xlsx",
    output_path="report.pptx",
    read_skill=True
)

print(f"Success: {result['success']}")
print(f"Output: {result['output_path']}")
```

## Troubleshooting

### Issue 1: "No module named 'openpyxl'"

**Solution:**
```bash
pip install openpyxl
# or
pip install -r requirements.txt
```

### Issue 2: "Excel file not found"

**Solution:**
- Use absolute paths: `D:\\NLS\\folder\\file.xlsx`
- Or use raw strings: `r"D:\NLS\folder\file.xlsx"`
- Check file exists: `os.path.exists("file.xlsx")`

### Issue 3: "Unable to locate credentials" (for AI features)

**Solution:**
```bash
aws configure
# or set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

### Issue 4: SKILL.md not found

**Solution:**
The script auto-detects SKILL.md in the current directory or parent. Ensure you're running from the correct directory or provide the path:

```python
from agent_integration import read_skill_file
skill = read_skill_file("path/to/SKILL.md")
```

## API Reference

### Main Functions

#### `excel_to_ppt_with_ai(excel_path, output_path, use_bedrock)`

Convert Excel file to PowerPoint with optional AI analysis.

**Parameters:**
- `excel_path` (str): Path to Excel file
- `output_path` (str, optional): Output PPT path
- `use_bedrock` (bool): Enable AI insights (default: False)

**Returns:** str - Path to generated PowerPoint

#### `process_excel_with_skill(excel_path, output_path, read_skill)`

Process Excel using skill capabilities.

**Parameters:**
- `excel_path` (str): Path to Excel file
- `output_path` (str, optional): Output PPT path
- `read_skill` (bool): Read SKILL.md first (default: True)

**Returns:** dict - Result with success, output_path, error

#### `read_skill_file(skill_path)`

Read SKILL.md documentation.

**Parameters:**
- `skill_path` (str, optional): Path to SKILL.md

**Returns:** str - Content of SKILL.md

## Support

For issues and questions:
- Check [SKILL.md](SKILL.md) for detailed documentation
- Review [README.md](README.md) for setup instructions
- Run examples: `python excel_to_ppt_example.py`

---

**Built with ❤️ for automated PowerPoint generation from Excel data**
