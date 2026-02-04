"""
Excel to PPT integration example.
Demonstrates reading Excel files and creating PowerPoint presentations.
"""
import os
from datetime import datetime
from pathlib import Path

from excel_reader import (
    read_excel_file,
    extract_budget_data,
    prepare_chart_data_from_df,
    prepare_table_data_from_df,
    get_excel_info
)
from ppt_exporter import (
    create_presentation,
    add_title_slide,
    add_content_slide,
    add_chart_slide,
    add_table_slide,
    save_presentation
)
from utils import get_current_date_string


def excel_to_ppt_basic(excel_path: str, output_path: str = None) -> str:
    """
    Create a basic PowerPoint presentation from an Excel file.
    
    Args:
        excel_path: Path to Excel file
        output_path: Output PPT path (optional)
    
    Returns:
        str: Path to generated PPT file
    """
    print(f"\n{'='*60}")
    print("Excel to PPT Conversion")
    print(f"{'='*60}")
    
    # Get Excel file info
    excel_info = get_excel_info(excel_path)
    print(f"\n📊 Reading Excel file: {excel_info['file_name']}")
    print(f"   Sheets: {', '.join(excel_info['sheet_names'])}")
    
    # Read Excel data
    df = read_excel_file(excel_path)
    print(f"   Rows: {len(df)}, Columns: {len(df.columns)}")
    
    # Create presentation
    prs = create_presentation()
    
    # Add title slide
    add_title_slide(
        prs,
        f"Data from {excel_info['file_name']}",
        f"Generated on {get_current_date_string('%B %d, %Y')}"
    )
    
    # Add overview slide
    overview = [
        f"Source: {excel_info['file_name']}",
        f"Total Rows: {len(df)}",
        f"Total Columns: {len(df.columns)}",
        f"Columns: {', '.join(df.columns.tolist()[:5])}{'...' if len(df.columns) > 5 else ''}"
    ]
    add_content_slide(prs, "Data Overview", overview)
    
    # Add data table (first 20 rows)
    table_data = prepare_table_data_from_df(df.head(20))
    add_table_slide(prs, "Data Sample", table_data)
    
    # If there are numeric columns, create a chart
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols and len(df) > 0:
        # Use first column as category and first numeric column as value
        category_col = df.columns[0]
        value_col = numeric_cols[0]
        
        try:
            chart_data = prepare_chart_data_from_df(df.head(10), category_col, value_col)
            add_chart_slide(prs, f"{value_col} by {category_col}", chart_data, chart_type='bar')
            print(f"   Chart created: {value_col} by {category_col}")
        except Exception as e:
            print(f"   Could not create chart: {e}")
    
    # Save presentation
    if not output_path:
        output_dir = './output'
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(output_dir, f'excel_export_{timestamp}.pptx')
    
    saved_path = save_presentation(prs, output_path)
    
    print(f"\n✓ PowerPoint created: {saved_path}")
    print(f"{'='*60}\n")
    
    return saved_path


def budget_excel_to_ppt(excel_path: str, output_path: str = None) -> str:
    """
    Create a budget-focused PowerPoint presentation from Excel data.
    
    Args:
        excel_path: Path to budget Excel file
        output_path: Output PPT path (optional)
    
    Returns:
        str: Path to generated PPT file
    """
    print(f"\n{'='*60}")
    print("Budget Excel to PPT Conversion")
    print(f"{'='*60}")
    
    # Extract budget data
    budget_data = extract_budget_data(excel_path)
    print(f"\n📊 Processing budget data from: {Path(excel_path).name}")
    print(f"   Rows: {budget_data['row_count']}")
    print(f"   Columns: {budget_data['column_count']}")
    
    # Read DataFrame for detailed processing
    df = read_excel_file(excel_path)
    
    # Create presentation
    prs = create_presentation()
    
    # Title slide
    add_title_slide(
        prs,
        "Budget Report",
        f"Generated from {Path(excel_path).name} on {get_current_date_string('%B %d, %Y')}"
    )
    
    # Summary slide
    summary_items = [
        f"Total Records: {budget_data['row_count']}",
        f"Data Columns: {budget_data['column_count']}"
    ]
    
    # Add summary statistics
    if budget_data['summary']:
        summary_items.append("\nNumeric Summary:")
        for col, stats in budget_data['summary'].items():
            summary_items.append(f"  • {col}: Total = ${stats['total']:,.2f}, Avg = ${stats['average']:,.2f}")
    
    add_content_slide(prs, "Budget Summary", summary_items)
    
    # Add detailed data table
    table_data = prepare_table_data_from_df(df)
    add_table_slide(prs, "Budget Details", table_data)
    
    # Create charts for numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols and len(df) > 0:
        category_col = df.columns[0]
        
        for value_col in numeric_cols[:2]:  # Limit to first 2 numeric columns
            try:
                chart_data = prepare_chart_data_from_df(df, category_col, value_col)
                add_chart_slide(prs, f"{value_col} Analysis", chart_data, chart_type='bar')
                print(f"   Chart added: {value_col}")
            except Exception as e:
                print(f"   Could not create chart for {value_col}: {e}")
    
    # Save presentation
    if not output_path:
        output_dir = './output'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'budget_report.pptx')
    
    saved_path = save_presentation(prs, output_path)
    
    print(f"\n✓ Budget PowerPoint created: {saved_path}")
    print(f"{'='*60}\n")
    
    return saved_path


def create_sample_budget_excel():
    """
    Create a sample budget Excel file for testing.
    
    Returns:
        str: Path to created Excel file
    """
    import pandas as pd
    
    # Sample budget data
    budget_data = {
        'Category': ['Salaries', 'Marketing', 'Operations', 'Technology', 'Travel', 'Office'],
        'Q1_Budget': [150000, 50000, 75000, 100000, 20000, 30000],
        'Q1_Actual': [155000, 48000, 72000, 95000, 18000, 28000],
        'Q2_Budget': [150000, 60000, 75000, 100000, 25000, 30000],
        'Q2_Actual': [152000, 65000, 70000, 105000, 22000, 29000]
    }
    
    df = pd.DataFrame(budget_data)
    
    # Calculate variance
    df['Q1_Variance'] = df['Q1_Actual'] - df['Q1_Budget']
    df['Q2_Variance'] = df['Q2_Actual'] - df['Q2_Budget']
    
    # Save to Excel
    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)
    excel_path = os.path.join(output_dir, 'sample_budget.xlsx')
    
    df.to_excel(excel_path, index=False, sheet_name='Budget')
    
    print(f"✓ Sample budget Excel created: {excel_path}")
    return excel_path


def main():
    """Run Excel to PPT examples."""
    print("\n" + "="*80)
    print(" "*20 + "EXCEL TO PPT INTEGRATION EXAMPLES")
    print("="*80)
    
    # Create sample Excel file
    sample_excel = create_sample_budget_excel()
    
    # Example 1: Basic conversion
    print("\n[Example 1] Basic Excel to PPT Conversion")
    excel_to_ppt_basic(sample_excel)
    
    # Example 2: Budget-focused conversion
    print("\n[Example 2] Budget-Focused Conversion")
    budget_excel_to_ppt(sample_excel)
    
    print("\n" + "="*80)
    print("All examples completed successfully!")
    print("Check the './output' directory for generated files.")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
