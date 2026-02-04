"""
PowerPoint generation module for creating presentations.
Uses python-pptx library to create slides with various content types.
"""
import os
import logging
from typing import Dict, List, Any, Optional
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.dml.color import RGBColor
import boto3
from botocore.exceptions import ClientError

from config import config
from utils import setup_logging, sanitize_filename

logger = setup_logging()


def create_presentation(title: str = "Presentation", subtitle: str = "") -> Presentation:
    """
    Initialize a new PowerPoint presentation.
    
    Args:
        title: Presentation title
        subtitle: Presentation subtitle
    
    Returns:
        Presentation: New PowerPoint presentation object
    """
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    logger.info(f"Created new presentation: {title}")
    return prs


def add_title_slide(prs: Presentation, title: str, subtitle: str = "") -> None:
    """
    Add a title slide to the presentation.
    
    Args:
        prs: Presentation object
        title: Title text
        subtitle: Subtitle text
    """
    slide_layout = prs.slide_layouts[0]  # Title slide layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Set title
    title_shape = slide.shapes.title
    title_shape.text = title
    
    # Format title
    title_frame = title_shape.text_frame
    title_paragraph = title_frame.paragraphs[0]
    title_paragraph.font.size = Pt(config.PPT_CONFIG['title_font_size'])
    title_paragraph.font.name = config.PPT_CONFIG['title_font_name']
    title_paragraph.font.bold = True
    title_paragraph.font.color.rgb = RGBColor(*config.PPT_CONFIG['primary_color'])
    
    # Set subtitle if provided
    if subtitle and len(slide.placeholders) > 1:
        subtitle_shape = slide.placeholders[1]
        subtitle_shape.text = subtitle
        
        # Format subtitle
        subtitle_frame = subtitle_shape.text_frame
        subtitle_paragraph = subtitle_frame.paragraphs[0]
        subtitle_paragraph.font.size = Pt(config.PPT_CONFIG['subtitle_font_size'])
        subtitle_paragraph.font.name = config.PPT_CONFIG['title_font_name']
    
    logger.info(f"Added title slide: {title}")


def add_content_slide(prs: Presentation, title: str, content: List[str]) -> None:
    """
    Add a bullet point content slide to the presentation.
    
    Args:
        prs: Presentation object
        title: Slide title
        content: List of bullet point strings
    """
    slide_layout = prs.slide_layouts[1]  # Title and Content layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Set title
    title_shape = slide.shapes.title
    title_shape.text = title
    
    # Format title
    title_frame = title_shape.text_frame
    title_paragraph = title_frame.paragraphs[0]
    title_paragraph.font.size = Pt(32)
    title_paragraph.font.name = config.PPT_CONFIG['title_font_name']
    title_paragraph.font.bold = True
    title_paragraph.font.color.rgb = RGBColor(*config.PPT_CONFIG['primary_color'])
    
    # Add content
    body_shape = slide.placeholders[1]
    text_frame = body_shape.text_frame
    text_frame.clear()  # Clear default text
    
    for i, item in enumerate(content):
        if i == 0:
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()
        
        p.text = item
        p.level = 0
        p.font.size = Pt(config.PPT_CONFIG['content_font_size'])
        p.font.name = config.PPT_CONFIG['content_font_name']
        p.space_before = Pt(6)
    
    logger.info(f"Added content slide: {title} ({len(content)} items)")


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
                   Example: {'categories': ['Jan', 'Feb'], 'values': [100, 150]}
        chart_type: Type of chart ('bar', 'line', 'pie')
    """
    slide_layout = prs.slide_layouts[5]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Add title
    left = Inches(0.5)
    top = Inches(0.5)
    width = Inches(9)
    height = Inches(0.75)
    
    title_box = slide.shapes.add_textbox(left, top, width, height)
    title_frame = title_box.text_frame
    title_frame.text = title
    title_paragraph = title_frame.paragraphs[0]
    title_paragraph.font.size = Pt(32)
    title_paragraph.font.name = config.PPT_CONFIG['title_font_name']
    title_paragraph.font.bold = True
    title_paragraph.font.color.rgb = RGBColor(*config.PPT_CONFIG['primary_color'])
    
    # Prepare chart data
    chart_data_obj = CategoryChartData()
    chart_data_obj.categories = chart_data.get('categories', [])
    
    # Handle multiple series or single series
    values = chart_data.get('values', [])
    series_name = chart_data.get('series_name', 'Series 1')
    
    if isinstance(values, dict):
        # Multiple series
        for name, vals in values.items():
            chart_data_obj.add_series(name, vals)
    else:
        # Single series
        chart_data_obj.add_series(series_name, values)
    
    # Determine chart type
    chart_type_map = {
        'bar': XL_CHART_TYPE.COLUMN_CLUSTERED,
        'line': XL_CHART_TYPE.LINE,
        'pie': XL_CHART_TYPE.PIE
    }
    xl_chart_type = chart_type_map.get(chart_type.lower(), XL_CHART_TYPE.COLUMN_CLUSTERED)
    
    # Add chart
    x = Inches(1)
    y = Inches(1.5)
    cx = Inches(8)
    cy = Inches(5)
    
    chart = slide.shapes.add_chart(
        xl_chart_type, x, y, cx, cy, chart_data_obj
    ).chart
    
    # Style chart
    chart.has_legend = True
    chart.legend.position = 2  # Right position
    chart.legend.include_in_layout = False
    
    logger.info(f"Added chart slide: {title} (type: {chart_type})")


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
                   Example: [['Month', 'Revenue'], ['Jan', 100], ['Feb', 150]]
    """
    slide_layout = prs.slide_layouts[5]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Add title
    left = Inches(0.5)
    top = Inches(0.5)
    width = Inches(9)
    height = Inches(0.75)
    
    title_box = slide.shapes.add_textbox(left, top, width, height)
    title_frame = title_box.text_frame
    title_frame.text = title
    title_paragraph = title_frame.paragraphs[0]
    title_paragraph.font.size = Pt(32)
    title_paragraph.font.name = config.PPT_CONFIG['title_font_name']
    title_paragraph.font.bold = True
    title_paragraph.font.color.rgb = RGBColor(*config.PPT_CONFIG['primary_color'])
    
    # Calculate table dimensions
    rows = len(table_data)
    cols = len(table_data[0]) if table_data else 0
    
    # Add table
    left = Inches(1)
    top = Inches(1.5)
    width = Inches(8)
    height = Inches(4.5)
    
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    
    # Fill table data
    for i, row_data in enumerate(table_data):
        for j, cell_value in enumerate(row_data):
            cell = table.rows[i].cells[j]
            cell.text = str(cell_value)
            
            # Format cell text
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(14)
                paragraph.font.name = config.PPT_CONFIG['content_font_name']
                
                # Bold header row
                if i == 0:
                    paragraph.font.bold = True
                    paragraph.font.color.rgb = RGBColor(255, 255, 255)
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(*config.PPT_CONFIG['primary_color'])
    
    logger.info(f"Added table slide: {title} ({rows}x{cols})")


def save_presentation(prs: Presentation, filename: str) -> str:
    """
    Save the PowerPoint presentation to a file.
    
    Args:
        prs: Presentation object
        filename: Output filename (can include path)
    
    Returns:
        str: Full path to saved file
    
    Raises:
        IOError: If file cannot be saved
    """
    try:
        # Split path and filename to sanitize only filename
        output_dir = os.path.dirname(filename)
        base_filename = os.path.basename(filename)
        
        # Sanitize only the filename part
        base_filename = sanitize_filename(base_filename)
        
        # Ensure .pptx extension
        if not base_filename.endswith('.pptx'):
            base_filename += '.pptx'
        
        # Reconstruct full path
        if output_dir:
            filename = os.path.join(output_dir, base_filename)
            # Create output directory if it doesn't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
        else:
            filename = base_filename
        
        # Save presentation
        prs.save(filename)
        
        # Get absolute path
        abs_path = os.path.abspath(filename)
        
        logger.info(f"Presentation saved: {abs_path}")
        return abs_path
        
    except Exception as e:
        logger.error(f"Error saving presentation: {e}")
        raise IOError(f"Failed to save presentation: {e}")


def upload_to_s3(filename: str, bucket: str, key: str = None) -> str:
    """
    Upload PowerPoint file to Amazon S3.
    
    Args:
        filename: Local file path to upload
        bucket: S3 bucket name
        key: S3 object key (defaults to filename if not provided)
    
    Returns:
        str: S3 URL of uploaded file
    
    Raises:
        FileNotFoundError: If file doesn't exist
        ClientError: If S3 upload fails
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    
    if not bucket:
        raise ValueError("S3 bucket name is required")
    
    # Use filename as key if not provided
    if key is None:
        key = os.path.basename(filename)
    
    try:
        # Create S3 client
        s3_client = boto3.client('s3', region_name=config.AWS_REGION)
        
        # Upload file
        s3_client.upload_file(
            filename, 
            bucket, 
            key,
            ExtraArgs={'ContentType': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'}
        )
        
        # Generate S3 URL
        s3_url = f"s3://{bucket}/{key}"
        
        logger.info(f"Uploaded to S3: {s3_url}")
        return s3_url
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"S3 upload error [{error_code}]: {error_message}")
        
        if error_code == 'NoSuchBucket':
            raise ValueError(f"S3 bucket does not exist: {bucket}")
        else:
            raise Exception(f"S3 upload failed: {error_message}")
    
    except Exception as e:
        logger.error(f"Unexpected error uploading to S3: {e}")
        raise


# Convenience function to create a complete presentation
def create_complete_presentation(
    title: str,
    subtitle: str,
    slides: List[Dict[str, Any]],
    filename: str,
    upload_s3: bool = False,
    s3_bucket: str = None
) -> str:
    """
    Create a complete PowerPoint presentation with multiple slides.
    
    Args:
        title: Presentation title
        subtitle: Presentation subtitle
        slides: List of slide dictionaries with 'type', 'title', and 'content' keys
                Example: [
                    {'type': 'content', 'title': 'Overview', 'content': ['Point 1', 'Point 2']},
                    {'type': 'chart', 'title': 'Data', 'content': {'categories': [...], 'values': [...]}}
                ]
        filename: Output filename
        upload_s3: Whether to upload to S3
        s3_bucket: S3 bucket name (required if upload_s3=True)
    
    Returns:
        str: Path to saved file or S3 URL
    """
    # Create presentation
    prs = create_presentation(title, subtitle)
    
    # Add title slide
    add_title_slide(prs, title, subtitle)
    
    # Add content slides
    for slide_info in slides:
        slide_type = slide_info.get('type', 'content')
        slide_title = slide_info.get('title', 'Untitled')
        slide_content = slide_info.get('content', [])
        
        if slide_type == 'content':
            add_content_slide(prs, slide_title, slide_content)
        elif slide_type == 'chart':
            chart_type = slide_info.get('chart_type', 'bar')
            add_chart_slide(prs, slide_title, slide_content, chart_type)
        elif slide_type == 'table':
            add_table_slide(prs, slide_title, slide_content)
    
    # Save presentation
    saved_path = save_presentation(prs, filename)
    
    # Upload to S3 if requested
    if upload_s3:
        if not s3_bucket:
            s3_bucket = config.S3_BUCKET_NAME
        
        if s3_bucket:
            s3_url = upload_to_s3(saved_path, s3_bucket)
            return s3_url
        else:
            logger.warning("S3 upload requested but no bucket configured")
    
    return saved_path
