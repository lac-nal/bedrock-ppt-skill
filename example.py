"""
Example script demonstrating the Bedrock PPT Skill.
Shows how to use the skill with sample sales data.
"""
import os
from datetime import datetime

from bedrock_analyzer import BedrockAnalyzer, generate_insights, generate_recommendations
from ppt_exporter import (
    create_presentation,
    add_title_slide,
    add_content_slide,
    add_chart_slide,
    add_table_slide,
    save_presentation
)
from utils import get_current_date_string, format_currency


def example_basic_usage():
    """
    Example 1: Basic usage with sample sales data.
    Demonstrates creating a simple presentation without Bedrock analysis.
    """
    print("\n" + "="*60)
    print("Example 1: Basic PPT Generation (No Bedrock)")
    print("="*60)
    
    # Sample data
    sample_data = {
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
    
    # Create presentation
    prs = create_presentation()
    
    # Add title slide
    add_title_slide(
        prs,
        "Q1 Sales Report",
        f"Performance Overview - {get_current_date_string('%B %Y')}"
    )
    
    # Add overview slide
    overview_content = [
        f"Total Revenue: {format_currency(sample_data['metrics']['total_revenue'])}",
        f"Total Units Sold: {sample_data['metrics']['total_units']:,}",
        f"Average Price: {format_currency(sample_data['metrics']['average_price'])}",
        "Period: January - April 2024"
    ]
    add_content_slide(prs, "Overview", overview_content)
    
    # Add chart slide
    chart_data = {
        'categories': [item['month'] for item in sample_data['sales']],
        'values': [item['revenue'] for item in sample_data['sales']],
        'series_name': 'Revenue ($)'
    }
    add_chart_slide(prs, "Monthly Revenue Trend", chart_data, chart_type='bar')
    
    # Add table slide
    table_data = [['Month', 'Revenue', 'Units', 'Avg Price']]
    for item in sample_data['sales']:
        avg_price = item['revenue'] / item['units'] if item['units'] > 0 else 0
        table_data.append([
            item['month'],
            format_currency(item['revenue']),
            f"{item['units']:,}",
            format_currency(avg_price)
        ])
    add_table_slide(prs, "Detailed Sales Data", table_data)
    
    # Save presentation
    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, "example_basic_report.pptx")
    saved_path = save_presentation(prs, filename)
    
    print(f"✓ Presentation saved: {saved_path}")
    return saved_path


def example_with_bedrock():
    """
    Example 2: Using Bedrock Claude for data analysis.
    Demonstrates full integration with AI-powered insights.
    """
    print("\n" + "="*60)
    print("Example 2: PPT Generation with Bedrock Analysis")
    print("="*60)
    
    # Sample data
    sample_data = {
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
    
    try:
        # Initialize Bedrock analyzer
        print("Initializing Bedrock Claude...")
        analyzer = BedrockAnalyzer()
        
        # Generate insights
        print("Generating insights...")
        insights_result = generate_insights(sample_data)
        
        # Generate recommendations
        print("Generating recommendations...")
        recommendations_result = generate_recommendations(sample_data)
        
        # Format for PPT
        analysis_result = {**insights_result, **recommendations_result}
        formatted_data = analyzer.format_analysis_for_ppt(analysis_result)
        
        # Create presentation
        print("Creating presentation...")
        prs = create_presentation()
        
        # Add title slide
        add_title_slide(
            prs,
            "AI-Powered Sales Analysis",
            f"Insights from Bedrock Claude - {get_current_date_string('%B %d, %Y')}"
        )
        
        # Add executive summary
        if formatted_data.get('executive_summary'):
            add_content_slide(
                prs,
                "Executive Summary",
                [formatted_data['executive_summary']]
            )
        
        # Add insights
        if formatted_data.get('insights'):
            add_content_slide(
                prs,
                "Key Insights from AI Analysis",
                formatted_data['insights']
            )
        
        # Add recommendations
        if formatted_data.get('recommendations'):
            add_content_slide(
                prs,
                "AI-Generated Recommendations",
                formatted_data['recommendations']
            )
        
        # Add chart
        chart_data = {
            'categories': [item['month'] for item in sample_data['sales']],
            'values': [item['revenue'] for item in sample_data['sales']],
            'series_name': 'Revenue ($)'
        }
        add_chart_slide(prs, "Revenue Trend Analysis", chart_data, chart_type='line')
        
        # Add table
        table_data = [['Month', 'Revenue', 'Units', 'Growth %']]
        for i, item in enumerate(sample_data['sales']):
            if i > 0:
                prev_revenue = sample_data['sales'][i-1]['revenue']
                growth = ((item['revenue'] - prev_revenue) / prev_revenue * 100)
                growth_str = f"{growth:+.1f}%"
            else:
                growth_str = "N/A"
            
            table_data.append([
                item['month'],
                format_currency(item['revenue']),
                f"{item['units']:,}",
                growth_str
            ])
        add_table_slide(prs, "Performance Metrics", table_data)
        
        # Save presentation
        output_dir = "./output"
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.join(output_dir, "example_bedrock_report.pptx")
        saved_path = save_presentation(prs, filename)
        
        print(f"✓ Presentation saved: {saved_path}")
        return saved_path
        
    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nNote: Bedrock example requires valid AWS credentials.")
        print("Falling back to basic example without AI analysis.")
        return example_basic_usage()


def example_custom_data():
    """
    Example 3: Using custom data structure.
    Shows flexibility in handling different data formats.
    """
    print("\n" + "="*60)
    print("Example 3: Custom Data Structure")
    print("="*60)
    
    # Custom data structure
    product_data = {
        "products": [
            {"name": "Product A", "sales": 45000, "margin": 25},
            {"name": "Product B", "sales": 32000, "margin": 30},
            {"name": "Product C", "sales": 28000, "margin": 20},
            {"name": "Product D", "sales": 15000, "margin": 35}
        ]
    }
    
    # Create presentation
    prs = create_presentation()
    
    # Add title slide
    add_title_slide(
        prs,
        "Product Performance Analysis",
        "Comparative Product Sales Report"
    )
    
    # Add overview
    total_sales = sum(p['sales'] for p in product_data['products'])
    avg_margin = sum(p['margin'] for p in product_data['products']) / len(product_data['products'])
    
    overview_content = [
        f"Total Sales Across All Products: {format_currency(total_sales)}",
        f"Average Profit Margin: {avg_margin:.1f}%",
        f"Number of Products Analyzed: {len(product_data['products'])}",
        "Analysis Period: Current Quarter"
    ]
    add_content_slide(prs, "Overview", overview_content)
    
    # Add chart comparing products
    chart_data = {
        'categories': [p['name'] for p in product_data['products']],
        'values': [p['sales'] for p in product_data['products']],
        'series_name': 'Sales ($)'
    }
    add_chart_slide(prs, "Product Sales Comparison", chart_data, chart_type='bar')
    
    # Add table with details
    table_data = [['Product', 'Sales', 'Margin %', 'Profit']]
    for product in product_data['products']:
        profit = product['sales'] * (product['margin'] / 100)
        table_data.append([
            product['name'],
            format_currency(product['sales']),
            f"{product['margin']}%",
            format_currency(profit)
        ])
    add_table_slide(prs, "Product Details", table_data)
    
    # Save presentation
    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, "example_custom_data.pptx")
    saved_path = save_presentation(prs, filename)
    
    print(f"✓ Presentation saved: {saved_path}")
    return saved_path


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print(" " * 20 + "BEDROCK PPT SKILL - EXAMPLES")
    print("="*80)
    
    # Run examples
    example_basic_usage()
    example_with_bedrock()
    example_custom_data()
    
    print("\n" + "="*80)
    print("All examples completed successfully!")
    print("Check the './output' directory for generated PowerPoint files.")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
