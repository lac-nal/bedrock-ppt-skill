"""
Utility functions for Bedrock PPT Skill.
Provides data validation, formatting, and logging utilities.
"""
import logging
import json
from typing import Any, Dict, List
from datetime import datetime


def setup_logging(log_level: str = 'INFO') -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


logger = setup_logging()


def validate_data_structure(data: Dict[str, Any], required_keys: List[str]) -> bool:
    """
    Validate that data dictionary contains required keys.
    
    Args:
        data: Dictionary to validate
        required_keys: List of required key names
    
    Returns:
        bool: True if all required keys are present
    
    Raises:
        ValueError: If required keys are missing
    """
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")
    return True


def format_currency(amount: float, currency: str = '$') -> str:
    """
    Format a number as currency.
    
    Args:
        amount: Numeric amount
        currency: Currency symbol
    
    Returns:
        str: Formatted currency string
    """
    return f"{currency}{amount:,.2f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format a number as percentage.
    
    Args:
        value: Numeric value (0-100 or 0-1)
        decimals: Number of decimal places
    
    Returns:
        str: Formatted percentage string
    """
    if value <= 1:
        value *= 100
    return f"{value:.{decimals}f}%"


def format_number(value: float, decimals: int = 0) -> str:
    """
    Format a number with thousands separator.
    
    Args:
        value: Numeric value
        decimals: Number of decimal places
    
    Returns:
        str: Formatted number string
    """
    return f"{value:,.{decimals}f}"


def safe_json_loads(json_string: str, default: Any = None) -> Any:
    """
    Safely parse JSON string with error handling.
    
    Args:
        json_string: JSON string to parse
        default: Default value if parsing fails
    
    Returns:
        Parsed JSON object or default value
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        return default


def get_current_date_string(format_str: str = '%Y-%m-%d') -> str:
    """
    Get current date as formatted string.
    
    Args:
        format_str: Date format string
    
    Returns:
        str: Formatted date string
    """
    return datetime.now().strftime(format_str)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
    
    Returns:
        str: Sanitized filename
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks of specified size.
    
    Args:
        lst: List to chunk
        chunk_size: Size of each chunk
    
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """
    Flatten a nested dictionary.
    
    Args:
        d: Dictionary to flatten
        parent_key: Key prefix for nested items
        sep: Separator between nested keys
    
    Returns:
        Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values.
    
    Args:
        old_value: Original value
        new_value: New value
    
    Returns:
        float: Percentage change
    """
    if old_value == 0:
        return 0.0 if new_value == 0 else 100.0
    return ((new_value - old_value) / old_value) * 100


def extract_numeric_values(data: List[Dict[str, Any]], key: str) -> List[float]:
    """
    Extract numeric values from a list of dictionaries.
    
    Args:
        data: List of dictionaries
        key: Key to extract from each dictionary
    
    Returns:
        List of numeric values
    """
    values = []
    for item in data:
        if key in item:
            try:
                values.append(float(item[key]))
            except (ValueError, TypeError):
                logger.warning(f"Could not convert {item[key]} to float")
    return values
