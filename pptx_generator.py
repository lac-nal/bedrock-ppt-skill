"""
PPTX Generator Module
Handles PowerPoint presentation generation for the A2A agent
"""
from typing import Dict, List, Any, Optional
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import os
from datetime import datetime


class PPTXGenerator:
    """
    PowerPoint presentation generator
    """
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize PPTX generator
        
        Args:
            output_dir: Directory to save generated PPTX files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def create_presentation(
        self,
        title: str,
        subtitle: str = "",
        content_slides: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Create a PowerPoint presentation
        
        Args:
            title: Presentation title
            subtitle: Presentation subtitle
            content_slides: List of slide definitions
            
        Returns:
            str: Path to the generated PPTX file
        """
        prs = Presentation()
        
        # Add title slide
        self._add_title_slide(prs, title, subtitle)
        
        # Add content slides if provided
        if content_slides:
            for slide_def in content_slides:
                slide_type = slide_def.get("type", "bullet")
                
                if slide_type == "bullet":
                    self._add_bullet_slide(
                        prs,
                        slide_def.get("title", ""),
                        slide_def.get("bullets", [])
                    )
                elif slide_type == "table":
                    self._add_table_slide(
                        prs,
                        slide_def.get("title", ""),
                        slide_def.get("data", [])
                    )
                elif slide_type == "text":
                    self._add_text_slide(
                        prs,
                        slide_def.get("title", ""),
                        slide_def.get("content", "")
                    )
        
        # Save presentation
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"presentation_{timestamp}.pptx"
        filepath = os.path.join(self.output_dir, filename)
        prs.save(filepath)
        
        return filepath
    
    def _add_title_slide(self, prs: Presentation, title: str, subtitle: str = ""):
        """
        Add a title slide
        
        Args:
            prs: Presentation object
            title: Title text
            subtitle: Subtitle text
        """
        slide_layout = prs.slide_layouts[0]  # Title slide layout
        slide = prs.slides.add_slide(slide_layout)
        
        title_shape = slide.shapes.title
        subtitle_shape = slide.placeholders[1]
        
        title_shape.text = title
        if subtitle:
            subtitle_shape.text = subtitle
    
    def _add_bullet_slide(self, prs: Presentation, title: str, bullets: List[str]):
        """
        Add a slide with bullet points
        
        Args:
            prs: Presentation object
            title: Slide title
            bullets: List of bullet points
        """
        slide_layout = prs.slide_layouts[1]  # Title and content layout
        slide = prs.slides.add_slide(slide_layout)
        
        title_shape = slide.shapes.title
        title_shape.text = title
        
        # Add bullet points
        body_shape = slide.placeholders[1]
        text_frame = body_shape.text_frame
        text_frame.clear()
        
        for i, bullet_text in enumerate(bullets):
            if i == 0:
                p = text_frame.paragraphs[0]
            else:
                p = text_frame.add_paragraph()
            
            p.text = bullet_text
            p.level = 0
    
    def _add_text_slide(self, prs: Presentation, title: str, content: str):
        """
        Add a slide with text content
        
        Args:
            prs: Presentation object
            title: Slide title
            content: Text content
        """
        slide_layout = prs.slide_layouts[1]  # Title and content layout
        slide = prs.slides.add_slide(slide_layout)
        
        title_shape = slide.shapes.title
        title_shape.text = title
        
        body_shape = slide.placeholders[1]
        text_frame = body_shape.text_frame
        text_frame.clear()
        
        p = text_frame.paragraphs[0]
        p.text = content
    
    def _add_table_slide(self, prs: Presentation, title: str, data: List[List[str]]):
        """
        Add a slide with a table
        
        Args:
            prs: Presentation object
            title: Slide title
            data: Table data as list of rows
        """
        if not data or len(data) == 0:
            return
        
        slide_layout = prs.slide_layouts[5]  # Blank layout
        slide = prs.slides.add_slide(slide_layout)
        
        # Add title
        left = Inches(0.5)
        top = Inches(0.5)
        width = Inches(9)
        height = Inches(0.5)
        
        title_box = slide.shapes.add_textbox(left, top, width, height)
        title_frame = title_box.text_frame
        title_frame.text = title
        
        # Make title bold and larger
        for paragraph in title_frame.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.size = Pt(28)
        
        # Add table
        rows = len(data)
        cols = len(data[0]) if data else 0
        
        if cols == 0:
            return
        
        left = Inches(0.5)
        top = Inches(1.5)
        width = Inches(9)
        height = Inches(5)
        
        table = slide.shapes.add_table(rows, cols, left, top, width, height).table
        
        # Fill table with data
        for i, row_data in enumerate(data):
            for j, cell_value in enumerate(row_data):
                cell = table.cell(i, j)
                cell.text = str(cell_value)
                
                # Header row formatting
                if i == 0:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(68, 114, 196)
                    for paragraph in cell.text_frame.paragraphs:
                        for run in paragraph.runs:
                            run.font.color.rgb = RGBColor(255, 255, 255)
                            run.font.bold = True
    
    def create_simple_presentation(self, title: str, content: str = "") -> str:
        """
        Create a simple one-slide presentation
        
        Args:
            title: Presentation title
            content: Content text
            
        Returns:
            str: Path to the generated PPTX file
        """
        slides = []
        if content:
            slides.append({
                "type": "text",
                "title": "Content",
                "content": content
            })
        
        return self.create_presentation(title, "", slides)
    
    def create_report_presentation(
        self,
        title: str,
        sections: List[Dict[str, Any]]
    ) -> str:
        """
        Create a report-style presentation with multiple sections
        
        Args:
            title: Report title
            sections: List of section definitions
            
        Returns:
            str: Path to the generated PPTX file
        """
        content_slides = []
        
        for section in sections:
            section_title = section.get("title", "Section")
            section_type = section.get("type", "bullet")
            
            if section_type == "bullet" and "items" in section:
                content_slides.append({
                    "type": "bullet",
                    "title": section_title,
                    "bullets": section["items"]
                })
            elif section_type == "table" and "data" in section:
                content_slides.append({
                    "type": "table",
                    "title": section_title,
                    "data": section["data"]
                })
            elif section_type == "text" and "content" in section:
                content_slides.append({
                    "type": "text",
                    "title": section_title,
                    "content": section["content"]
                })
        
        return self.create_presentation(title, "", content_slides)


def generate_pptx(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate PPTX based on request data
    
    Args:
        request_data: Dictionary with presentation details
        
    Returns:
        dict: Result with file path and metadata
    """
    generator = PPTXGenerator()
    
    title = request_data.get("title", "Presentation")
    subtitle = request_data.get("subtitle", "")
    content_slides = request_data.get("slides", [])
    
    # Generate presentation
    filepath = generator.create_presentation(title, subtitle, content_slides)
    
    # Get file size
    file_size = os.path.getsize(filepath)
    
    return {
        "success": True,
        "filepath": filepath,
        "filename": os.path.basename(filepath),
        "file_size": file_size,
        "slides_count": len(content_slides) + 1,  # +1 for title slide
        "message": f"Presentation created successfully: {os.path.basename(filepath)}"
    }
