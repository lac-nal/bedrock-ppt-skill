"""
Main orchestration script for Bedrock PPT Skill.
Integrates data analysis with Bedrock Claude and PowerPoint generation.
"""
import os
import sys
import logging
from typing import Dict, Any
from datetime import datetime

from config import config
from utils import setup_logging, get_current_date_string
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

logger = setup_logging()


def process_data_and_generate_ppt(
    data: Dict[str, Any],
    output_filename: str = None,
    upload_s3: bool = False
) -> str:
    """
    Main function to process data with Bedrock and generate PPT.
    
    Args:
        data: Input data dictionary to analyze
        output_filename: Output PPT filename (optional)
        upload_s3: Whether to upload to S3
    
    Returns:
        str: Path to generated PPT or S3 URL
    """
    try:
        logger.info("Starting data processing and PPT generation")
        
        # Validate configuration
        is_valid, error_msg = config.validate()
        if not is_valid:
            logger.error(f"Configuration error: {error_msg}")
            raise ValueError(f"Configuration error: {error_msg}")
        
        # Initialize Bedrock analyzer
        analyzer = BedrockAnalyzer()
        
        # Generate insights
        logger.info("Generating insights with Bedrock Claude...")
        insights_result = analyzer.generate_insights(data)
        
        # Generate recommendations
        logger.info("Generating recommendations with Bedrock Claude...")
        recommendations_result = analyzer.generate_recommendations(data)
        
        # Combine results
        analysis_result = {
            **insights_result,
            **recommendations_result
        }
        
        # Format for PPT
        formatted_data = analyzer.format_analysis_for_ppt(analysis_result)
        
        # Create presentation
        logger.info("Creating PowerPoint presentation...")
        prs = create_presentation()
        
        # Add title slide
        title = "Data Analysis Report"
        subtitle = f"Generated on {get_current_date_string('%B %d, %Y')}"
        add_title_slide(prs, title, subtitle)
        
        # Add executive summary slide
        if formatted_data.get('executive_summary'):
            add_content_slide(
                prs,
                "Executive Summary",
                [formatted_data['executive_summary']]
            )
        
        # Add insights slide
        if formatted_data.get('insights'):
            add_content_slide(
                prs,
                "Key Insights",
                formatted_data['insights']
            )
        
        # Add recommendations slide
        if formatted_data.get('recommendations'):
            add_content_slide(
                prs,
                "Recommendations",
                formatted_data['recommendations']
            )
        
        # Add data visualization if data contains metrics
        if 'sales' in data and isinstance(data['sales'], list):
            # Prepare chart data
            chart_data = {
                'categories': [item.get('month', '') for item in data['sales']],
                'values': [item.get('revenue', 0) for item in data['sales']],
                'series_name': 'Revenue'
            }
            add_chart_slide(prs, "Sales Performance", chart_data, chart_type='bar')
        
        # Add detailed data table if available
        if 'sales' in data and isinstance(data['sales'], list):
            table_data = [['Month', 'Revenue', 'Units']]
            for item in data['sales']:
                table_data.append([
                    item.get('month', ''),
                    f"${item.get('revenue', 0):,}",
                    item.get('units', 0)
                ])
            add_table_slide(prs, "Detailed Metrics", table_data)
        
        # Determine output filename
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"analysis_report_{timestamp}.pptx"
        
        # Create output directory if specified in config
        if config.PPT_OUTPUT_DIR:
            os.makedirs(config.PPT_OUTPUT_DIR, exist_ok=True)
            output_path = os.path.join(config.PPT_OUTPUT_DIR, output_filename)
        else:
            output_path = output_filename
        
        # Save presentation
        saved_path = save_presentation(prs, output_path)
        logger.info(f"Presentation saved successfully: {saved_path}")
        
        # Upload to S3 if requested
        if upload_s3:
            bucket = config.S3_BUCKET_NAME
            if bucket:
                s3_url = upload_to_s3(saved_path, bucket)
                logger.info(f"Presentation uploaded to S3: {s3_url}")
                return s3_url
            else:
                logger.warning("S3 upload requested but no bucket configured")
        
        return saved_path
        
    except Exception as e:
        logger.error(f"Error in process_data_and_generate_ppt: {e}")
        raise


def main():
    """Main entry point for the script."""
    # Sample data for testing
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
        # Process data and generate PPT
        result = process_data_and_generate_ppt(
            data=sample_data,
            output_filename="sample_report.pptx",
            upload_s3=False
        )
        
        print(f"\n{'='*60}")
        print(f"SUCCESS!")
        print(f"{'='*60}")
        print(f"PowerPoint presentation generated: {result}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"ERROR!")
        print(f"{'='*60}")
        print(f"Failed to generate presentation: {e}")
        print(f"{'='*60}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
