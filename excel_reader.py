"""
Excel reader module for reading data from Excel files.
Provides functions to extract data from .xlsx files for PPT generation.
"""
import logging
from typing import Dict, List, Any, Optional
import pandas as pd
from pathlib import Path

from utils import setup_logging, validate_data_structure

logger = setup_logging()


def read_excel_file(file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
    """
    Read an Excel file and return a pandas DataFrame.
    
    Args:
        file_path: Path to the Excel file
        sheet_name: Optional sheet name to read. If None, reads the first sheet.
    
    Returns:
        pd.DataFrame: Data from the Excel file
    
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is not a valid Excel file
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Excel file not found: {file_path}")
    
    if file_path.suffix.lower() not in ['.xlsx', '.xls']:
        raise ValueError(f"File must be an Excel file (.xlsx or .xls): {file_path}")
    
    try:
        # Read Excel file
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            logger.info(f"Read Excel file: {file_path}, sheet: {sheet_name}")
        else:
            df = pd.read_excel(file_path)
            logger.info(f"Read Excel file: {file_path} (first sheet)")
        
        return df
    
    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
        raise ValueError(f"Failed to read Excel file: {e}")


def read_all_sheets(file_path: str) -> Dict[str, pd.DataFrame]:
    """
    Read all sheets from an Excel file.
    
    Args:
        file_path: Path to the Excel file
    
    Returns:
        dict: Dictionary with sheet names as keys and DataFrames as values
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Excel file not found: {file_path}")
    
    try:
        # Read all sheets
        sheets_dict = pd.read_excel(file_path, sheet_name=None)
        logger.info(f"Read {len(sheets_dict)} sheets from: {file_path}")
        return sheets_dict
    
    except Exception as e:
        logger.error(f"Error reading Excel sheets: {e}")
        raise ValueError(f"Failed to read Excel sheets: {e}")


def excel_to_dict(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Convert a pandas DataFrame to a dictionary format suitable for analysis.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        dict: Data in dictionary format
    """
    try:
        # Convert DataFrame to list of dictionaries (one per row)
        records = df.to_dict('records')
        
        # Calculate summary statistics for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        summary = {}
        for col in numeric_cols:
            summary[col] = {
                'total': float(df[col].sum()),
                'average': float(df[col].mean()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'count': int(df[col].count())
            }
        
        result = {
            'data': records,
            'summary': summary,
            'columns': df.columns.tolist(),
            'row_count': len(df),
            'column_count': len(df.columns)
        }
        
        logger.info(f"Converted DataFrame to dict: {len(records)} rows, {len(df.columns)} columns")
        return result
    
    except Exception as e:
        logger.error(f"Error converting DataFrame to dict: {e}")
        raise


def extract_budget_data(file_path: str, sheet_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract budget data from Excel file in a format suitable for PPT generation.
    
    Args:
        file_path: Path to the Excel file
        sheet_name: Optional sheet name to read
    
    Returns:
        dict: Budget data structured for analysis and PPT generation
    """
    df = read_excel_file(file_path, sheet_name)
    
    # Convert to dict
    data_dict = excel_to_dict(df)
    
    # Add metadata
    data_dict['source_file'] = str(file_path)
    if sheet_name:
        data_dict['sheet_name'] = sheet_name
    
    return data_dict


def prepare_chart_data_from_df(
    df: pd.DataFrame, 
    category_column: str, 
    value_column: str
) -> Dict[str, Any]:
    """
    Prepare chart data from DataFrame for PPT chart slides.
    
    Args:
        df: pandas DataFrame
        category_column: Column name to use for categories (x-axis)
        value_column: Column name to use for values (y-axis)
    
    Returns:
        dict: Chart data in format expected by add_chart_slide()
    """
    if category_column not in df.columns:
        raise ValueError(f"Category column '{category_column}' not found in DataFrame")
    
    if value_column not in df.columns:
        raise ValueError(f"Value column '{value_column}' not found in DataFrame")
    
    chart_data = {
        'categories': df[category_column].tolist(),
        'values': df[value_column].tolist(),
        'series_name': value_column
    }
    
    return chart_data


def prepare_table_data_from_df(
    df: pd.DataFrame, 
    include_header: bool = True
) -> List[List[Any]]:
    """
    Prepare table data from DataFrame for PPT table slides.
    
    Args:
        df: pandas DataFrame
        include_header: Whether to include column headers
    
    Returns:
        list: Table data in format expected by add_table_slide()
    """
    table_data = []
    
    if include_header:
        table_data.append(df.columns.tolist())
    
    # Add data rows
    for _, row in df.iterrows():
        table_data.append(row.tolist())
    
    return table_data


def get_excel_info(file_path: str) -> Dict[str, Any]:
    """
    Get information about an Excel file without reading all data.
    
    Args:
        file_path: Path to the Excel file
    
    Returns:
        dict: Information about the Excel file
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Excel file not found: {file_path}")
    
    try:
        # Get sheet names
        excel_file = pd.ExcelFile(file_path)
        sheet_names = excel_file.sheet_names
        
        info = {
            'file_name': file_path.name,
            'file_path': str(file_path),
            'file_size_bytes': file_path.stat().st_size,
            'sheet_names': sheet_names,
            'sheet_count': len(sheet_names)
        }
        
        logger.info(f"Excel file info: {info['file_name']} - {info['sheet_count']} sheets")
        return info
    
    except Exception as e:
        logger.error(f"Error getting Excel info: {e}")
        raise ValueError(f"Failed to get Excel file info: {e}")


# Example usage
if __name__ == "__main__":
    # Example of how to use this module
    print("Excel Reader Module")
    print("="*60)
    print("\nExample usage:")
    print("""
    from excel_reader import read_excel_file, extract_budget_data
    
    # Read Excel file
    df = read_excel_file('budget.xlsx')
    
    # Extract budget data
    budget_data = extract_budget_data('budget.xlsx')
    
    # Use with PPT generation
    from ppt_exporter import create_presentation, add_table_slide
    prs = create_presentation()
    table_data = prepare_table_data_from_df(df)
    add_table_slide(prs, 'Budget Data', table_data)
    """)
