"""
Bedrock Claude integration module for data analysis and insights generation.
Uses Amazon Bedrock with Claude Sonnet 3.5 model via boto3.
"""
import json
import logging
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError, BotoCoreError

from config import config
from utils import setup_logging, safe_json_loads

logger = setup_logging()


class BedrockAnalyzer:
    """Bedrock Claude analyzer for data insights and recommendations."""
    
    def __init__(self, region: str = None, model_id: str = None):
        """
        Initialize Bedrock analyzer.
        
        Args:
            region: AWS region (defaults to config)
            model_id: Bedrock model ID (defaults to config)
        """
        self.region = region or config.AWS_REGION
        self.model_id = model_id or config.BEDROCK_MODEL_ID
        
        try:
            self.bedrock_client = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.region
            )
            logger.info(f"Bedrock client initialized for region: {self.region}")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {e}")
            raise
    
    def analyze_data_with_bedrock(
        self, 
        data: Dict[str, Any], 
        prompt_template: str
    ) -> Dict[str, Any]:
        """
        Send data to Bedrock Claude for analysis.
        
        Args:
            data: Data dictionary to analyze
            prompt_template: Prompt template with {data} placeholder
        
        Returns:
            dict: Analysis result from Bedrock
        
        Raises:
            ValueError: If data or prompt is invalid
            ClientError: If Bedrock API call fails
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        if not prompt_template:
            raise ValueError("Prompt template cannot be empty")
        
        # Format the prompt with data
        data_str = json.dumps(data, indent=2)
        prompt = prompt_template.format(data=data_str)
        
        try:
            # Prepare request body for Claude 3.5 Sonnet
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            logger.info(f"Sending request to Bedrock model: {self.model_id}")
            
            # Invoke Bedrock model
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                contentType='application/json',
                accept='application/json',
                body=json.dumps(request_body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            # Extract text content from Claude response
            content = response_body.get('content', [])
            if content and len(content) > 0:
                result_text = content[0].get('text', '')
            else:
                result_text = ''
            
            logger.info("Successfully received response from Bedrock")
            
            # Try to parse as JSON if possible
            result = safe_json_loads(result_text, {'raw_response': result_text})
            
            return result
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            logger.error(f"Bedrock ClientError [{error_code}]: {error_message}")
            
            if error_code == 'ThrottlingException':
                raise Exception("Bedrock API throttling - please retry later")
            elif error_code == 'ValidationException':
                raise ValueError(f"Invalid request: {error_message}")
            else:
                raise Exception(f"Bedrock API error: {error_message}")
        
        except BotoCoreError as e:
            logger.error(f"Bedrock BotoCoreError: {e}")
            raise Exception(f"AWS connection error: {e}")
        
        except Exception as e:
            logger.error(f"Unexpected error in analyze_data_with_bedrock: {e}")
            raise
    
    def generate_insights(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate insights from data using Bedrock Claude.
        
        Args:
            data: Data dictionary to analyze
        
        Returns:
            dict: Insights with structure: 
                  {
                      'insights': [list of insight strings],
                      'key_findings': [list of key findings]
                  }
        """
        prompt_template = """
You are a data analyst. Analyze the following data and provide insights.

Data:
{data}

Please provide your analysis in the following JSON format:
{{
    "insights": [
        "Insight 1 description",
        "Insight 2 description",
        "Insight 3 description"
    ],
    "key_findings": [
        "Key finding 1",
        "Key finding 2",
        "Key finding 3"
    ]
}}

Focus on:
1. Trends and patterns in the data
2. Notable changes or anomalies
3. Performance metrics
4. Areas of concern or opportunity

Provide 3-5 insights and 3-5 key findings. Be specific and actionable.
"""
        
        try:
            result = self.analyze_data_with_bedrock(data, prompt_template)
            
            # Ensure proper structure
            if 'insights' not in result:
                result['insights'] = []
            if 'key_findings' not in result:
                result['key_findings'] = []
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            # Return default structure on error
            return {
                'insights': [f"Error generating insights: {str(e)}"],
                'key_findings': []
            }
    
    def generate_recommendations(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate actionable recommendations using Bedrock Claude.
        
        Args:
            data: Data dictionary to analyze
        
        Returns:
            dict: Recommendations with structure:
                  {
                      'recommendations': [list of recommendation strings],
                      'priorities': [list of priority actions]
                  }
        """
        prompt_template = """
You are a business consultant. Based on the following data, provide actionable recommendations.

Data:
{data}

Please provide your recommendations in the following JSON format:
{{
    "recommendations": [
        "Recommendation 1 with clear action",
        "Recommendation 2 with clear action",
        "Recommendation 3 with clear action"
    ],
    "priorities": [
        "High priority action 1",
        "High priority action 2"
    ]
}}

Focus on:
1. Actionable steps to improve performance
2. Strategies to address challenges
3. Opportunities for growth
4. Risk mitigation

Provide 3-5 recommendations and 2-3 high priority actions. Be specific and business-focused.
"""
        
        try:
            result = self.analyze_data_with_bedrock(data, prompt_template)
            
            # Ensure proper structure
            if 'recommendations' not in result:
                result['recommendations'] = []
            if 'priorities' not in result:
                result['priorities'] = []
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            # Return default structure on error
            return {
                'recommendations': [f"Error generating recommendations: {str(e)}"],
                'priorities': []
            }
    
    def format_analysis_for_ppt(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format Bedrock analysis result for PowerPoint structure.
        
        Args:
            analysis_result: Raw analysis result from Bedrock
        
        Returns:
            dict: Formatted data ready for PPT slides with structure:
                  {
                      'executive_summary': str,
                      'insights': [list],
                      'recommendations': [list],
                      'key_metrics': dict
                  }
        """
        formatted = {
            'executive_summary': '',
            'insights': [],
            'recommendations': [],
            'key_metrics': {}
        }
        
        try:
            # Extract insights
            if 'insights' in analysis_result:
                formatted['insights'] = analysis_result['insights']
            elif 'key_findings' in analysis_result:
                formatted['insights'] = analysis_result['key_findings']
            
            # Extract recommendations
            if 'recommendations' in analysis_result:
                formatted['recommendations'] = analysis_result['recommendations']
            elif 'priorities' in analysis_result:
                formatted['recommendations'] = analysis_result['priorities']
            
            # Create executive summary
            if formatted['insights']:
                formatted['executive_summary'] = (
                    "Key findings from data analysis reveal important trends "
                    "and opportunities for improvement. "
                    f"Analysis identified {len(formatted['insights'])} key insights "
                    f"and {len(formatted['recommendations'])} actionable recommendations."
                )
            
            # Extract any metrics
            if 'metrics' in analysis_result:
                formatted['key_metrics'] = analysis_result['metrics']
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error formatting analysis for PPT: {e}")
            return formatted


# Convenience functions
def analyze_data_with_bedrock(
    data: Dict[str, Any], 
    prompt_template: str,
    region: str = None,
    model_id: str = None
) -> Dict[str, Any]:
    """
    Convenience function to analyze data with Bedrock Claude.
    
    Args:
        data: Data to analyze
        prompt_template: Prompt template with {data} placeholder
        region: AWS region (optional)
        model_id: Bedrock model ID (optional)
    
    Returns:
        dict: Analysis result
    """
    analyzer = BedrockAnalyzer(region=region, model_id=model_id)
    return analyzer.analyze_data_with_bedrock(data, prompt_template)


def generate_insights(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to generate insights from data.
    
    Args:
        data: Data to analyze
    
    Returns:
        dict: Insights
    """
    analyzer = BedrockAnalyzer()
    return analyzer.generate_insights(data)


def generate_recommendations(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to generate recommendations from data.
    
    Args:
        data: Data to analyze
    
    Returns:
        dict: Recommendations
    """
    analyzer = BedrockAnalyzer()
    return analyzer.generate_recommendations(data)


def format_analysis_for_ppt(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to format analysis for PowerPoint.
    
    Args:
        analysis_result: Analysis result from Bedrock
    
    Returns:
        dict: Formatted data for PPT
    """
    analyzer = BedrockAnalyzer()
    return analyzer.format_analysis_for_ppt(analysis_result)
