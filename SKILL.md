# SKILL.md - PPT Export Skill Definition

## Skill Overview

The **PPT Export Skill** is a comprehensive Python-based capability that combines Amazon Bedrock Claude Sonnet 3.5 for intelligent data analysis with python-pptx for professional PowerPoint presentation generation. This skill enables automated creation of data-driven presentations with AI-powered insights and recommendations.

## Purpose

This skill accomplishes the following:

1. **Data Analysis**: Leverages Amazon Bedrock Claude Sonnet 3.5 to analyze business data and generate meaningful insights
2. **Intelligent Recommendations**: Produces actionable recommendations based on data patterns
3. **Professional Presentations**: Creates multi-slide PowerPoint presentations with various content types
4. **AWS Integration**: Supports S3 upload for cloud storage
5. **Flexible Data Handling**: Processes various data formats and structures

## Architecture

```
Data Input → Bedrock Analysis → Format Results → Generate PPT → Save/Upload
     ↓              ↓                  ↓              ↓            ↓
Sample Data    AI Insights      PPT Structure    python-pptx   Local/S3
```

## Core Components

### 1. Bedrock Analyzer Module (`bedrock_analyzer.py`)

Handles all interactions with Amazon Bedrock Claude for data analysis.

#### Function: `analyze_data_with_bedrock()`

```python
def analyze_data_with_bedrock(
    data: Dict[str, Any], 
    prompt_template: str
) -> Dict[str, Any]:
    """
    Send data to Bedrock Claude for analysis.
    
    Args:
        data: Data dictionary to analyze
        prompt_template: Prompt template with {data} placeholder
    
    Returns:
        dict: Analysis result from Bedrock
    
    Raises:
        ValueError: If data or prompt is invalid
        ClientError: If Bedrock API call fails
    """
```

**Usage Example:**
```python
from bedrock_analyzer import analyze_data_with_bedrock

data = {"sales": [{"month": "Jan", "revenue": 100000}]}
prompt = "Analyze this sales data: {data}"

result = analyze_data_with_bedrock(data, prompt)
```

#### Function: `generate_insights()`

```python
def generate_insights(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate insights from data using Bedrock Claude.
    
    Args:
        data: Data dictionary to analyze
    
    Returns:
        dict: Insights with structure:
              {
                  'insights': [list of insight strings],
                  'key_findings': [list of key findings]
              }
    """
```

**Usage Example:**
```python
from bedrock_analyzer import generate_insights

data = {
    "sales": [
        {"month": "January", "revenue": 100000},
        {"month": "February", "revenue": 150000}
    ]
}

insights = generate_insights(data)
print(insights['insights'])  # List of AI-generated insights
```

#### Function: `generate_recommendations()`

```python
def generate_recommendations(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate actionable recommendations using Bedrock Claude.
    
    Args:
        data: Data dictionary to analyze
    
    Returns:
        dict: Recommendations with structure:
              {
                  'recommendations': [list of recommendation strings],
                  'priorities': [list of priority actions]
              }
    """
```

**Usage Example:**
```python
from bedrock_analyzer import generate_recommendations

recommendations = generate_recommendations(data)
print(recommendations['recommendations'])  # List of actionable items
```

#### Function: `format_analysis_for_ppt()`

```python
def format_analysis_for_ppt(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format Bedrock analysis result for PowerPoint structure.
    
    Args:
        analysis_result: Raw analysis result from Bedrock
    
    Returns:
        dict: Formatted data ready for PPT slides with structure:
              {
                  'executive_summary': str,
                  'insights': [list],
                  'recommendations': [list],
                  'key_metrics': dict
              }
    """
```

### 2. PPT Exporter Module (`ppt_exporter.py`)

Handles PowerPoint generation using python-pptx library.

#### Function: `create_presentation()`

```python
def create_presentation(title: str = "Presentation", subtitle: str = "") -> Presentation:
    """
    Initialize a new PowerPoint presentation.
    
    Args:
        title: Presentation title
        subtitle: Presentation subtitle
    
    Returns:
        Presentation: New PowerPoint presentation object
    """
```

**Usage Example:**
```python
from ppt_exporter import create_presentation

prs = create_presentation("Q1 Sales Report", "2024 Analysis")
```

#### Function: `add_title_slide()`

```python
def add_title_slide(prs: Presentation, title: str, subtitle: str = "") -> None:
    """
    Add a title slide to the presentation.
    
    Args:
        prs: Presentation object
        title: Title text
        subtitle: Subtitle text
    """
```

**Usage Example:**
```python
from ppt_exporter import add_title_slide

add_title_slide(prs, "Annual Report", "Year 2024")
```

#### Function: `add_content_slide()`

```python
def add_content_slide(prs: Presentation, title: str, content: List[str]) -> None:
    """
    Add a bullet point content slide to the presentation.
    
    Args:
        prs: Presentation object
        title: Slide title
        content: List of bullet point strings
    """
```

**Usage Example:**
```python
from ppt_exporter import add_content_slide

content = [
    "Revenue increased by 50%",
    "Customer base grew to 10,000",
    "Launched 5 new products"
]
add_content_slide(prs, "Key Achievements", content)
```

#### Function: `add_chart_slide()`

```python
def add_chart_slide(
    prs: Presentation, 
    title: str, 
    chart_data: Dict[str, Any],
    chart_type: str = 'bar'
) -> None:
    """
    Add a slide with a chart to the presentation.
    
    Args:
        prs: Presentation object
        title: Slide title
        chart_data: Dictionary with 'categories' and 'values' keys
        chart_type: Type of chart ('bar', 'line', 'pie')
    """
```

**Usage Example:**
```python
from ppt_exporter import add_chart_slide

chart_data = {
    'categories': ['Jan', 'Feb', 'Mar', 'Apr'],
    'values': [100, 150, 200, 180],
    'series_name': 'Revenue (K)'
}
add_chart_slide(prs, "Monthly Revenue", chart_data, chart_type='bar')
```

#### Function: `add_table_slide()`

```python
def add_table_slide(
    prs: Presentation, 
    title: str, 
    table_data: List[List[Any]]
) -> None:
    """
    Add a slide with a data table to the presentation.
    
    Args:
        prs: Presentation object
        title: Slide title
        table_data: List of lists representing table rows
                   First row is treated as header
    """
```

**Usage Example:**
```python
from ppt_exporter import add_table_slide

table_data = [
    ['Month', 'Revenue', 'Units'],
    ['Jan', '$100,000', '500'],
    ['Feb', '$150,000', '750']
]
add_table_slide(prs, "Sales Details", table_data)
```

#### Function: `save_presentation()`

```python
def save_presentation(prs: Presentation, filename: str) -> str:
    """
    Save the PowerPoint presentation to a file.
    
    Args:
        prs: Presentation object
        filename: Output filename (can include path)
    
    Returns:
        str: Full path to saved file
    """
```

**Usage Example:**
```python
from ppt_exporter import save_presentation

saved_path = save_presentation(prs, "output/report.pptx")
print(f"Saved to: {saved_path}")
```

#### Function: `upload_to_s3()`

```python
def upload_to_s3(filename: str, bucket: str, key: str = None) -> str:
    """
    Upload PowerPoint file to Amazon S3.
    
    Args:
        filename: Local file path to upload
        bucket: S3 bucket name
        key: S3 object key (defaults to filename if not provided)
    
    Returns:
        str: S3 URL of uploaded file
    """
```

**Usage Example:**
```python
from ppt_exporter import upload_to_s3

s3_url = upload_to_s3(
    filename="report.pptx",
    bucket="my-presentations",
    key="reports/2024/q1_report.pptx"
)
print(f"Uploaded to: {s3_url}")
```

## Data Format Specifications

### Input Data Structure

The skill expects data in dictionary format:

```python
{
    "sales": [
        {
            "month": "January",
            "revenue": 100000,
            "units": 500
        },
        {
            "month": "February",
            "revenue": 150000,
            "units": 750
        }
    ],
    "metrics": {
        "total_revenue": 250000,
        "total_units": 1250,
        "average_price": 200
    }
}
```

### Output Structure from Bedrock

```python
{
    "insights": [
        "Revenue shows strong growth trend",
        "February saw 50% increase over January",
        "Average order value remained consistent"
    ],
    "key_findings": [
        "Q1 exceeded targets by 20%",
        "Customer acquisition rate doubled"
    ],
    "recommendations": [
        "Increase inventory for high-demand products",
        "Launch targeted marketing campaign in March"
    ],
    "priorities": [
        "Optimize supply chain",
        "Expand sales team"
    ]
}
```

## boto3 Integration Details

### Bedrock Runtime Client

The skill uses `boto3` to connect to Amazon Bedrock:

```python
import boto3

bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)
```

### Model Configuration

- **Model ID**: `anthropic.claude-3-5-sonnet-20241022-v2:0`
- **API Version**: `bedrock-2023-05-31`
- **Max Tokens**: 4096
- **Temperature**: 0.7
- **Top P**: 0.9

### Request Format

```python
request_body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 4096,
    "messages": [
        {
            "role": "user",
            "content": "Your prompt here"
        }
    ],
    "temperature": 0.7,
    "top_p": 0.9
}

response = bedrock_client.invoke_model(
    modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
    contentType='application/json',
    accept='application/json',
    body=json.dumps(request_body)
)
```

### Response Parsing

```python
response_body = json.loads(response['body'].read())
content = response_body.get('content', [])
result_text = content[0].get('text', '') if content else ''
```

## Error Handling

### Common Errors and Solutions

#### 1. AWS Credentials Error

**Error**: `NoCredentialsError` or `CredentialsNotFound`

**Solution**:
```python
# Set credentials in .env file
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret

# Or use AWS CLI configuration
aws configure
```

#### 2. Bedrock API Throttling

**Error**: `ThrottlingException`

**Solution**: Implement retry logic with exponential backoff
```python
import time

for attempt in range(3):
    try:
        result = analyze_data_with_bedrock(data, prompt)
        break
    except Exception as e:
        if 'ThrottlingException' in str(e):
            time.sleep(2 ** attempt)
        else:
            raise
```

#### 3. Invalid Data Format

**Error**: `ValueError: Missing required keys`

**Solution**: Validate data structure before analysis
```python
from utils import validate_data_structure

required_keys = ['sales', 'metrics']
validate_data_structure(data, required_keys)
```

#### 4. S3 Upload Failure

**Error**: `NoSuchBucket` or `AccessDenied`

**Solution**:
- Verify bucket exists
- Check IAM permissions
- Ensure correct region

```python
# Create bucket if needed
import boto3
s3 = boto3.client('s3')
s3.create_bucket(Bucket='my-bucket')
```

#### 5. File I/O Errors

**Error**: `IOError` or `PermissionError`

**Solution**: Ensure write permissions and directory exists
```python
import os

output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)
```

## Configuration

### Environment Variables (.env)

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# S3 Configuration
S3_BUCKET_NAME=your-bucket-name

# Bedrock Model
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0

# Output Directory
PPT_OUTPUT_DIR=./output
```

### Configuration File (config.py)

Access configuration values:
```python
from config import config

print(config.AWS_REGION)
print(config.BEDROCK_MODEL_ID)
print(config.PPT_CONFIG)  # Styling options
```

## Complete Usage Example

```python
#!/usr/bin/env python3
"""Complete example of using the PPT Export Skill."""

from bedrock_analyzer import BedrockAnalyzer
from ppt_exporter import (
    create_presentation,
    add_title_slide,
    add_content_slide,
    add_chart_slide,
    add_table_slide,
    save_presentation,
    upload_to_s3
)

# 1. Prepare your data
data = {
    "sales": [
        {"month": "January", "revenue": 100000, "units": 500},
        {"month": "February", "revenue": 150000, "units": 750},
        {"month": "March", "revenue": 200000, "units": 1000},
        {"month": "April", "revenue": 180000, "units": 900}
    ],
    "metrics": {
        "total_revenue": 630000,
        "total_units": 3150,
        "average_price": 200
    }
}

# 2. Analyze with Bedrock Claude
analyzer = BedrockAnalyzer()
insights = analyzer.generate_insights(data)
recommendations = analyzer.generate_recommendations(data)

# 3. Format results
analysis_result = {**insights, **recommendations}
formatted = analyzer.format_analysis_for_ppt(analysis_result)

# 4. Create PowerPoint presentation
prs = create_presentation()

# 5. Add slides
add_title_slide(prs, "Sales Analysis Report", "Q1 2024")
add_content_slide(prs, "Executive Summary", [formatted['executive_summary']])
add_content_slide(prs, "Key Insights", formatted['insights'])
add_content_slide(prs, "Recommendations", formatted['recommendations'])

# Add chart
chart_data = {
    'categories': [item['month'] for item in data['sales']],
    'values': [item['revenue'] for item in data['sales']],
    'series_name': 'Revenue'
}
add_chart_slide(prs, "Revenue Trend", chart_data)

# Add table
table_data = [['Month', 'Revenue', 'Units']]
for item in data['sales']:
    table_data.append([item['month'], f"${item['revenue']:,}", item['units']])
add_table_slide(prs, "Detailed Data", table_data)

# 6. Save and optionally upload
saved_path = save_presentation(prs, "output/report.pptx")
print(f"Presentation saved: {saved_path}")

# Optional: Upload to S3
# s3_url = upload_to_s3(saved_path, "my-bucket", "reports/q1_2024.pptx")
# print(f"Uploaded to: {s3_url}")
```

## Testing

### Test with Sample Data

```python
# Test Bedrock connection
from bedrock_analyzer import generate_insights

test_data = {"sales": [{"month": "Jan", "revenue": 1000}]}
result = generate_insights(test_data)
print("Bedrock test:", "PASS" if result else "FAIL")

# Test PPT generation
from ppt_exporter import create_presentation, add_title_slide, save_presentation

prs = create_presentation()
add_title_slide(prs, "Test", "Test Subtitle")
path = save_presentation(prs, "test.pptx")
print("PPT test:", "PASS" if path else "FAIL")
```

### Validation

```python
# Validate output
import os
assert os.path.exists("test.pptx"), "PPT file not created"
assert os.path.getsize("test.pptx") > 0, "PPT file is empty"
print("Validation: PASS")
```

## Dependencies

Required Python packages:
- `boto3>=1.34.0` - AWS SDK for Python
- `python-pptx>=0.6.21` - PowerPoint generation
- `pandas>=2.0.0` - Data manipulation
- `python-dotenv>=1.0.0` - Environment variable management

Install all dependencies:
```bash
pip install -r requirements.txt
```

## Best Practices

1. **Always validate data** before sending to Bedrock
2. **Handle API throttling** with retry logic
3. **Use environment variables** for sensitive credentials
4. **Create output directories** before saving files
5. **Log all operations** for debugging
6. **Structure prompts clearly** for better AI responses
7. **Format numbers** appropriately in presentations
8. **Test with sample data** before production use

## Summary

The PPT Export Skill provides a complete solution for automated PowerPoint generation with AI-powered insights. By combining Amazon Bedrock Claude's analytical capabilities with python-pptx's presentation features, this skill enables creation of professional, data-driven presentations with minimal manual effort.

Key capabilities:
- ✅ AI-powered data analysis
- ✅ Automated insight generation
- ✅ Professional PPT creation
- ✅ Multiple slide types (title, content, charts, tables)
- ✅ S3 upload support
- ✅ Comprehensive error handling
- ✅ Flexible data formats
- ✅ Easy-to-use API
