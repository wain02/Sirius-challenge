import requests
import json
from typing import Dict, List, Optional


class EmailService:
    """Simple email service using SendGrid API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sendgrid.com/v3/mail/send"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
    
    def send_email(
        self,
        from_email: str,
        to_email: str,
        to_name: str,
        subject: str,
        html_content: str,
        substitutions: Optional[Dict[str, str]] = None
    ) -> Dict:
        """
        Send an email using SendGrid API
        
        Args:
            from_email: Sender email address
            to_email: Recipient email address
            to_name: Recipient name
            subject: Email subject
            html_content: HTML content of the email
            substitutions: Dictionary of substitutions for template variables
            
        Returns:
            Dict containing the response from SendGrid API
        """
        
        payload = {
            "from": {
                "email": from_email
            },
            "personalizations": [
                {
                    "to": [
                        {
                            "email": to_email,
                            "name": to_name
                        }
                    ],
                    "subject": subject
                }
            ],
            "content": [
                {
                    "type": "text/html",
                    "value": html_content
                }
            ]
        }
        
        # Add substitutions if provided
        if substitutions:
            payload["personalizations"][0]["substitutions"] = substitutions
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(payload)
            )
            
            return {
                "status_code": response.status_code,
                "response_text": response.text,
                "success": response.status_code == 202
            }
            
        except Exception as e:
            return {
                "status_code": None,
                "response_text": str(e),
                "success": False,
                "error": str(e)
            }