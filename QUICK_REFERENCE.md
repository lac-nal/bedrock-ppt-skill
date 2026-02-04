# Quick Reference: Create PPT Files with Bedrock Skill

## ⚡ Fastest Way to Create PPT

### Method 1: Python Code (3 lines)
```python
from ppt_exporter import create_presentation, add_title_slide, save_presentation
prs = create_presentation()
add_title_slide(prs, "My Title", "My Subtitle")
save_presentation(prs, "output.pptx")
```

### Method 2: Excel to PPT (1 line)
```bash
python agent_integration.py data.xlsx --output report.pptx
```

### Method 3: Run Demo (1 line)
```bash
python demo_create_ppt.py
```

---

## 📋 All Available Functions

### PPT Creation (ppt_exporter.py)
```python
from ppt_exporter import *

prs = create_presentation()                    # Start new PPT
add_title_slide(prs, "Title", "Subtitle")     # Add title
add_content_slide(prs, "Title", ["a", "b"])   # Add bullets
add_chart_slide(prs, "Title", chart_data)     # Add chart
add_table_slide(prs, "Title", table_data)     # Add table
save_presentation(prs, "file.pptx")           # Save PPT
```

### Excel Reading (excel_reader.py)
```python
from excel_reader import *

df = read_excel_file("data.xlsx")             # Read Excel
data = extract_budget_data("data.xlsx")       # Get structured data
chart = prepare_chart_data_from_df(df, "X", "Y")  # Prepare chart
table = prepare_table_data_from_df(df)        # Prepare table
```

### Bedrock AI (bedrock_analyzer.py)
```python
from bedrock_analyzer import *

insights = generate_insights(data)            # AI insights
recs = generate_recommendations(data)         # AI recommendations
```

### Agent Integration (agent_integration.py)
```python
from agent_integration import *

skill = read_skill_file()                     # Read SKILL.md
result = excel_to_ppt_with_ai("x.xlsx")       # Excel→PPT with AI
```

---

## 🎯 Common Tasks

### Task 1: Create Simple Report
```python
from ppt_exporter import *

prs = create_presentation()
add_title_slide(prs, "Q1 Report", "2024")
add_content_slide(prs, "Summary", [
    "Revenue: $1M",
    "Profit: $200K",
    "Growth: 25%"
])
save_presentation(prs, "q1_report.pptx")
```

### Task 2: Add Chart
```python
chart_data = {
    'categories': ['Jan', 'Feb', 'Mar'],
    'values': [100, 150, 200],
    'series_name': 'Sales'
}
add_chart_slide(prs, "Monthly Sales", chart_data, chart_type='bar')
```

### Task 3: Add Table
```python
table_data = [
    ['Name', 'Value'],
    ['Sales', '1000'],
    ['Cost', '600'],
    ['Profit', '400']
]
add_table_slide(prs, "Financial Data", table_data)
```

### Task 4: Convert Excel to PPT
```python
from agent_integration import excel_to_ppt_with_ai

excel_to_ppt_with_ai(
    excel_path="budget.xlsx",
    output_path="budget_report.pptx"
)
```

---

## 🔧 Chart Types
- `'bar'` - Bar chart
- `'line'` - Line chart
- `'pie'` - Pie chart

## 📊 Chart Data Format
```python
{
    'categories': ['A', 'B', 'C'],     # X-axis labels
    'values': [10, 20, 30],            # Y-axis values
    'series_name': 'My Data'           # Legend name
}
```

## 📋 Table Data Format
```python
[
    ['Header1', 'Header2', 'Header3'],  # First row = headers
    ['Data1', 'Data2', 'Data3'],        # Data rows
    ['Data4', 'Data5', 'Data6']
]
```

---

## 🚀 Installation
```bash
pip install -r requirements.txt
```

## 📚 Documentation
- `SKILL.md` - Complete API reference
- `README.md` - Full user guide
- `INTEGRATION_GUIDE.md` - Integration patterns
- `ANSWER.md` - Verification that PPT creation works

## 💻 Command Line Examples
```bash
# Run demo
python demo_create_ppt.py

# Convert Excel
python agent_integration.py data.xlsx

# Run examples
python example.py
python excel_to_ppt_example.py
```

---

## ✅ Verified Working
- ✓ Direct PPT creation
- ✓ Excel to PPT conversion
- ✓ Charts (bar, line, pie)
- ✓ Tables with formatting
- ✓ SKILL.md reading
- ✓ Command-line interface
- ✓ Python API

**All features tested and working!**
