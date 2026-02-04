"""
Configuration module for Bedrock PPT Skill.
Loads environment variables and provides configuration settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for AWS Bedrock and PPT settings."""
    
    # AWS Configuration
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    # S3 Configuration
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', '')
    
    # Bedrock Model Configuration
    BEDROCK_MODEL_ID = os.getenv(
        'BEDROCK_MODEL_ID',
        'anthropic.claude-3-5-sonnet-20241022-v2:0'
    )
    
    # PPT Styling Configuration
    PPT_CONFIG = {
        'title_font_size': 44,
        'subtitle_font_size': 32,
        'content_font_size': 18,
        'title_font_name': 'Calibri',
        'content_font_name': 'Calibri',
        'primary_color': (0, 112, 192),  # RGB for blue
        'secondary_color': (68, 114, 196),  # RGB for lighter blue
        'text_color': (0, 0, 0),  # RGB for black
    }
    
    # Output Configuration
    PPT_OUTPUT_DIR = os.getenv('PPT_OUTPUT_DIR', './output')
    
    @classmethod
    def validate(cls):
        """
        Validate that required configuration is present.
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not cls.AWS_REGION:
            return False, "AWS_REGION is not configured"
        
        # AWS credentials are optional if using IAM roles
        # but we can warn if not present
        if not cls.AWS_ACCESS_KEY_ID and not cls.AWS_SECRET_ACCESS_KEY:
            print("Warning: AWS credentials not found in environment. "
                  "Assuming IAM role or default credentials.")
        
        return True, None


# Create default config instance
config = Config()
