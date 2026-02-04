"""
Claude Agent SDK Integration Example.
Demonstrates how to use the PPT skill with claude_agent_sdk for reading Excel and creating PPT.

This script is designed to work with claude_agent_sdk and can read SKILL.md.
"""
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
from bedrock_analyzer import BedrockAnalyzer, generate_insights, generate_recommendations
from utils import get_current_date_string
import pandas as pd


def read_skill_file(skill_path: str = None) -> str:
    """
    Read the SKILL.md file to understand available capabilities.
    
    Args:
        skill_path: Path to SKILL.md file (optional, auto-detected if None)
    
    Returns:
        str: Content of SKILL.md file
    """
    if skill_path is None:
        # Try to find SKILL.md in current directory or parent
        current_dir = Path(__file__).parent
        skill_path = current_dir / "SKILL.md"
        
        if not skill_path.exists():
            skill_path = current_dir.parent / "SKILL.md"
    else:
        skill_path = Path(skill_path)
    
    if not skill_path.exists():
        raise FileNotFoundError(f"SKILL.md not found at: {skill_path}")
    
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"✓ Read SKILL.md from: {skill_path}")
    return content


def excel_to_ppt_with_ai(
    excel_path: str,
    output_path: str = None,
    use_bedrock: bool = False
) -> str:
    """
    Convert Excel file to PowerPoint with optional AI analysis.
    
    This function can be called by claude_agent_sdk to process Excel files.
    
    Args:
        excel_path: Path to Excel file (.xlsx)
        output_path: Output PPT path (optional)
        use_bedrock: Whether to use Bedrock AI for insights (requires AWS credentials)
    
    Returns:
        str: Path to generated PowerPoint file
    """
    excel_path = Path(excel_path)
    
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")
    
    print(f"\n{'='*60}")
    print(f"Converting Excel to PowerPoint")
    print(f"{'='*60}")
    print(f"Input:  {excel_path}")
    
    # Get Excel info
    excel_info = get_excel_info(str(excel_path))
    print(f"Sheets: {', '.join(excel_info['sheet_names'])}")
    
    # Read Excel data
    df = read_excel_file(str(excel_path))
    print(f"Rows:   {len(df)}")
    print(f"Cols:   {len(df.columns)}")
    
    # Extract data for analysis
    budget_data = extract_budget_data(str(excel_path))
    
    # Create presentation
    prs = create_presentation()
    
    # Add title slide
    add_title_slide(
        prs,
        f"Report: {excel_path.stem}",
        f"Generated on {get_current_date_string('%B %d, %Y')}"
    )
    
    # Add data overview
    overview = [
        f"Source File: {excel_path.name}",
        f"Total Records: {len(df)}",
        f"Columns: {', '.join(df.columns.tolist()[:5])}{'...' if len(df.columns) > 5 else ''}",
        f"Data Range: {df.index[0]} to {df.index[-1]}" if len(df) > 0 else "No data"
    ]
    add_content_slide(prs, "Data Overview", overview)
    
    # If AI analysis is enabled, generate insights
    if use_bedrock:
        try:
            print("Generating AI insights with Bedrock...")
            
            # Generate insights
            insights = generate_insights(budget_data)
            if insights.get('insights'):
                add_content_slide(prs, "AI-Generated Insights", insights['insights'])
                print(f"✓ Added {len(insights['insights'])} insights")
            
            # Generate recommendations
            recommendations = generate_recommendations(budget_data)
            if recommendations.get('recommendations'):
                add_content_slide(prs, "AI Recommendations", recommendations['recommendations'])
                print(f"✓ Added {len(recommendations['recommendations'])} recommendations")
        
        except Exception as e:
            print(f"⚠ Could not generate AI insights: {e}")
            print("  (Continuing without AI analysis)")
    
    # Add data table
    table_data = prepare_table_data_from_df(df.head(20))
    add_table_slide(prs, "Data Table", table_data)
    print("✓ Added data table")
    
    # Create charts for numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols and len(df) > 0:
        category_col = df.columns[0]
        
        # Add up to 2 charts
        for i, value_col in enumerate(numeric_cols[:2]):
            try:
                chart_data = prepare_chart_data_from_df(df.head(15), category_col, value_col)
                chart_type = 'bar' if i == 0 else 'line'
                add_chart_slide(prs, f"{value_col} Analysis", chart_data, chart_type=chart_type)
                print(f"✓ Added chart: {value_col}")
            except Exception as e:
                print(f"⚠ Could not create chart for {value_col}: {e}")
    
    # Save presentation
    if output_path is None:
        output_dir = excel_path.parent / "output"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{excel_path.stem}_report.pptx"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    saved_path = save_presentation(prs, str(output_path))
    
    print(f"\n✓ PowerPoint created: {saved_path}")
    print(f"{'='*60}\n")
    
    return saved_path


def process_excel_with_skill(
    excel_path: str,
    output_path: str = None,
    read_skill: bool = True
) -> Dict[str, Any]:
    """
    Process Excel file using the PPT skill capabilities.
    
    This is the main entry point for claude_agent_sdk integration.
    
    Args:
        excel_path: Path to Excel file
        output_path: Output PPT path (optional)
        read_skill: Whether to read SKILL.md first (default: True)
    
    Returns:
        dict: Result information
    """
    result = {
        'success': False,
        'excel_path': excel_path,
        'output_path': None,
        'skill_content': None,
        'error': None
    }
    
    try:
        # Read SKILL.md if requested
        if read_skill:
            skill_content = read_skill_file()
            result['skill_content'] = skill_content[:500] + "..."  # Store first 500 chars
            print(f"✓ Loaded skill documentation ({len(skill_content)} characters)")
        
        # Process Excel and create PPT
        output = excel_to_ppt_with_ai(
            excel_path=excel_path,
            output_path=output_path,
            use_bedrock=False  # Default to False to avoid credential issues
        )
        
        result['success'] = True
        result['output_path'] = output
        
    except Exception as e:
        result['error'] = str(e)
        print(f"✗ Error: {e}")
    
    return result


def main():
    """
    Main function for standalone execution.
    Compatible with claude_agent_sdk workflow.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert Excel to PowerPoint using PPT Skill')
    parser.add_argument('excel_path', help='Path to Excel file')
    parser.add_argument('--output', '-o', help='Output PPT path (optional)')
    parser.add_argument('--no-skill', action='store_true', help='Skip reading SKILL.md')
    parser.add_argument('--with-ai', action='store_true', help='Use Bedrock AI for insights')
    
    args = parser.parse_args()
    
    # Read SKILL.md
    if not args.no_skill:
        try:
            skill = read_skill_file()
            print(f"\nSkill loaded ({len(skill)} chars)")
            print("\nSkill Overview (first 300 chars):")
            print("-" * 60)
            print(skill[:300] + "...")
            print("-" * 60)
        except Exception as e:
            print(f"Warning: Could not read SKILL.md: {e}")
    
    # Process Excel file
    result = excel_to_ppt_with_ai(
        excel_path=args.excel_path,
        output_path=args.output,
        use_bedrock=args.with_ai
    )
    
    print(f"\nResult: {result}")


if __name__ == "__main__":
    # Check if arguments provided
    if len(sys.argv) > 1:
        main()
    else:
        # Run demo with sample data
        print("\n" + "="*80)
        print(" "*15 + "CLAUDE AGENT SDK INTEGRATION - DEMO MODE")
        print("="*80)
        print("\nNo arguments provided. Creating sample Excel and converting to PPT...")
        
        # Create sample Excel
        from excel_to_ppt_example import create_sample_budget_excel
        sample_excel = create_sample_budget_excel()
        
        # Process it
        print("\n" + "="*80)
        result = process_excel_with_skill(sample_excel, read_skill=True)
        
        print("\n" + "="*80)
        print("RESULT:")
        print(f"  Success: {result['success']}")
        print(f"  Input:   {result['excel_path']}")
        print(f"  Output:  {result['output_path']}")
        if result['error']:
            print(f"  Error:   {result['error']}")
        print("="*80)
        
        print("\nTo use with arguments:")
        print("  python agent_integration.py <excel_file> [--output <ppt_file>] [--with-ai]")
