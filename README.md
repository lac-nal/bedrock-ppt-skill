# Bedrock PPT Skill

> 🚀 AI-Powered PowerPoint Generation with Amazon Bedrock Claude Sonnet 3.5

An intelligent Python skill that combines Amazon Bedrock Claude for data analysis with python-pptx for automated PowerPoint presentation generation.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![boto3](https://img.shields.io/badge/boto3-latest-orange.svg)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

The **Bedrock PPT Skill** automates the creation of professional PowerPoint presentations by:

1. **Analyzing Data**: Using Amazon Bedrock Claude Sonnet 3.5 to extract insights from your data
2. **Generating Insights**: AI-powered analysis that identifies trends, patterns, and opportunities
3. **Creating Recommendations**: Actionable business recommendations based on data
4. **Building Presentations**: Automated PPT generation with multiple slide types
5. **Cloud Integration**: Optional S3 upload for easy sharing

Perfect for business analysts, data scientists, and anyone who needs to quickly create data-driven presentations.

## ✨ Features

### Core Capabilities
- 🤖 **AI-Powered Analysis**: Leverages Claude Sonnet 3.5 for intelligent data insights
- 📊 **Multiple Slide Types**: Title, content, charts (bar/line/pie), and tables
- ☁️ **AWS Integration**: Direct integration with Bedrock and S3
- 🎨 **Customizable Styling**: Configure fonts, colors, and layouts
- 📝 **Comprehensive Logging**: Track all operations for debugging
- 🛡️ **Error Handling**: Robust error handling for production use

### Supported Chart Types
- Bar charts
- Line charts
- Pie charts

### Supported Data Formats
- Sales data with time series
- Product performance metrics
- Financial data
- Custom data structures

## 🏗️ Architecture

```
┌─────────────┐
│  Input Data │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Bedrock Claude     │
│  (Data Analysis)    │
└──────┬──────────────┘
       │
       ├─► Insights
       ├─► Recommendations
       └─► Key Findings
       │
       ▼
┌─────────────────────┐
│  Format for PPT     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  python-pptx        │
│  (PPT Generation)   │
└──────┬──────────────┘
       │
       ├─► Local Save
       └─► S3 Upload (optional)
```

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher**
- **AWS Account** with access to:
  - Amazon Bedrock (Claude Sonnet 3.5)
  - Amazon S3 (optional, for uploads)
- **AWS Credentials** configured
- **Bedrock Model Access**: Request access to Claude 3.5 Sonnet in AWS console

### AWS Bedrock Setup

1. Go to AWS Console → Bedrock
2. Navigate to "Model access"
3. Request access to "Claude 3.5 Sonnet"
4. Wait for approval (usually instant for supported regions)

Supported regions:
- `us-east-1` (US East - N. Virginia)
- `us-west-2` (US West - Oregon)
- `eu-west-1` (Europe - Ireland)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/lac-nal/bedrock-ppt-skill.git
cd bedrock-ppt-skill
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

## ⚙️ Configuration

### Environment Variables

Edit the `.env` file with your settings:

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here

# S3 Configuration (Optional)
S3_BUCKET_NAME=your-bucket-name

# Bedrock Model Configuration
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0

# PPT Configuration
PPT_OUTPUT_DIR=./output
```

### AWS Credentials Setup

#### Option 1: Environment Variables (.env file)
Already configured above.

#### Option 2: AWS CLI Configuration
```bash
aws configure
```

#### Option 3: IAM Role (for EC2/Lambda)
No configuration needed - uses instance role automatically.

### Styling Configuration

Customize PPT appearance in `config.py`:

```python
PPT_CONFIG = {
    'title_font_size': 44,
    'subtitle_font_size': 32,
    'content_font_size': 18,
    'title_font_name': 'Calibri',
    'content_font_name': 'Calibri',
    'primary_color': (0, 112, 192),      # RGB for blue
    'secondary_color': (68, 114, 196),   # RGB for lighter blue
    'text_color': (0, 0, 0),             # RGB for black
}
```

## 📖 Usage

### Quick Start

```python
from main import process_data_and_generate_ppt

# Your data
data = {
    "sales": [
        {"month": "January", "revenue": 100000, "units": 500},
        {"month": "February", "revenue": 150000, "units": 750},
        {"month": "March", "revenue": 200000, "units": 1000}
    ],
    "metrics": {
        "total_revenue": 450000,
        "total_units": 2250,
        "average_price": 200
    }
}

# Generate presentation
result = process_data_and_generate_ppt(
    data=data,
    output_filename="my_report.pptx",
    upload_s3=False
)

print(f"Presentation created: {result}")
```

### Command Line Usage

#### Run Main Script
```bash
python main.py
```

#### Run Examples
```bash
python example.py
```

This will create three example presentations in the `./output` directory:
1. `example_basic_report.pptx` - Basic PPT without AI
2. `example_bedrock_report.pptx` - Full AI-powered analysis
3. `example_custom_data.pptx` - Custom data structure

## 💡 Examples

### Example 1: Basic PowerPoint Generation

```python
from ppt_exporter import (
    create_presentation,
    add_title_slide,
    add_content_slide,
    add_chart_slide,
    save_presentation
)

# Create presentation
prs = create_presentation()

# Add title
add_title_slide(prs, "Q1 Sales Report", "2024 Analysis")

# Add content slide
content = [
    "Revenue grew 50% year-over-year",
    "Expanded to 3 new markets",
    "Customer satisfaction: 95%"
]
add_content_slide(prs, "Highlights", content)

# Add chart
chart_data = {
    'categories': ['Jan', 'Feb', 'Mar'],
    'values': [100, 150, 200],
    'series_name': 'Revenue (K)'
}
add_chart_slide(prs, "Revenue Growth", chart_data, chart_type='line')

# Save
save_presentation(prs, "output/report.pptx")
```

### Example 2: AI-Powered Analysis

```python
from bedrock_analyzer import BedrockAnalyzer
from ppt_exporter import create_presentation, add_content_slide

# Prepare data
data = {
    "sales": [
        {"month": "Q1", "revenue": 300000},
        {"month": "Q2", "revenue": 450000},
        {"month": "Q3", "revenue": 500000}
    ]
}

# Analyze with Bedrock
analyzer = BedrockAnalyzer()
insights = analyzer.generate_insights(data)
recommendations = analyzer.generate_recommendations(data)

# Create presentation
prs = create_presentation()
add_content_slide(prs, "AI Insights", insights['insights'])
add_content_slide(prs, "Recommendations", recommendations['recommendations'])

save_presentation(prs, "ai_analysis.pptx")
```

### Example 3: Upload to S3

```python
from ppt_exporter import upload_to_s3

# After creating your presentation
local_file = "output/report.pptx"
s3_url = upload_to_s3(
    filename=local_file,
    bucket="my-presentations",
    key="reports/2024/q1_report.pptx"
)

print(f"Uploaded to: {s3_url}")
```

### Example 4: Complete Workflow

```python
from main import process_data_and_generate_ppt

# Load your data (from CSV, database, API, etc.)
data = load_your_data()

# Generate presentation with AI analysis
result = process_data_and_generate_ppt(
    data=data,
    output_filename="complete_report.pptx",
    upload_s3=True  # Upload to S3
)

print(f"Success! Presentation available at: {result}")
```

## 📚 API Reference

For detailed API documentation, see [SKILL.md](SKILL.md).

### Key Modules

#### `bedrock_analyzer.py`
- `analyze_data_with_bedrock()` - Send data to Claude for analysis
- `generate_insights()` - Generate insights from data
- `generate_recommendations()` - Generate recommendations
- `format_analysis_for_ppt()` - Format analysis for slides

#### `ppt_exporter.py`
- `create_presentation()` - Initialize new PPT
- `add_title_slide()` - Add title slide
- `add_content_slide()` - Add bullet points
- `add_chart_slide()` - Add charts (bar/line/pie)
- `add_table_slide()` - Add data tables
- `save_presentation()` - Save PPT file
- `upload_to_s3()` - Upload to S3

#### `utils.py`
- `validate_data_structure()` - Validate data format
- `format_currency()` - Format numbers as currency
- `format_percentage()` - Format as percentage
- `setup_logging()` - Configure logging

## 🔧 Troubleshooting

### Common Issues

#### Issue 1: "No module named 'boto3'"

**Solution:**
```bash
pip install -r requirements.txt
```

#### Issue 2: "Unable to locate credentials"

**Solution:**
Check your AWS credentials:
```bash
# Verify credentials
aws sts get-caller-identity

# Or set in .env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
```

#### Issue 3: "Access denied to Bedrock model"

**Solution:**
1. Go to AWS Console → Bedrock
2. Click "Model access"
3. Request access to Claude 3.5 Sonnet
4. Wait for approval

#### Issue 4: "ThrottlingException"

**Solution:**
Bedrock has rate limits. Add retry logic:
```python
import time

for i in range(3):
    try:
        result = generate_insights(data)
        break
    except Exception as e:
        if 'Throttling' in str(e):
            time.sleep(2 ** i)  # Exponential backoff
        else:
            raise
```

#### Issue 5: "FileNotFoundError: output directory"

**Solution:**
```python
import os
os.makedirs("output", exist_ok=True)
```

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

- Check [SKILL.md](SKILL.md) for detailed documentation
- Review [example.py](example.py) for working examples
- Check AWS Bedrock documentation: https://docs.aws.amazon.com/bedrock/

## 🧪 Testing

Run the example script to verify installation:

```bash
python example.py
```

Expected output:
```
================================================================================
                    BEDROCK PPT SKILL - EXAMPLES
================================================================================

============================================================
Example 1: Basic PPT Generation (No Bedrock)
============================================================
✓ Presentation saved: /path/to/output/example_basic_report.pptx

...

All examples completed successfully!
Check the './output' directory for generated PowerPoint files.
================================================================================
```

## 📁 Project Structure

```
bedrock-ppt-skill/
├── README.md                 # This file
├── SKILL.md                  # Detailed skill documentation
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── config.py                # Configuration settings
├── bedrock_analyzer.py      # Bedrock Claude integration
├── ppt_exporter.py          # PowerPoint generation
├── main.py                  # Main orchestration script
├── example.py               # Working examples
└── utils.py                 # Helper utilities
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Amazon Web Services for Bedrock Claude
- python-pptx library maintainers
- boto3 SDK team

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the [SKILL.md](SKILL.md) documentation
- Review AWS Bedrock documentation

---

**Built with ❤️ using Amazon Bedrock Claude and python-pptx**
