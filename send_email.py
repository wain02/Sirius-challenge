#!/usr/bin/env python3
"""
Basic script to send email using SendGrid
Based on the provided request example
"""

import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from services.email_service import EmailService

# Load environment variables from .env file
load_dotenv()

def main():
    # Get SendGrid API Key from environment variables
    API_KEY = os.getenv('SENDGRID_API_KEY')
    
    if not API_KEY:
        print("Error: SENDGRID_API_KEY not found in environment variables")
        print("Please check your .env file or set the environment variable")
        return
    
    # Initialize email service
    email_service = EmailService(API_KEY)
    
    # Email configuration (from environment variables or defaults)
    from_email = os.getenv('FROM_EMAIL', "mwainwright@fi.uba.ar")
    to_email = os.getenv('TO_EMAIL', "martinwain2002@gmail.com")
    to_name = "Destinatario"
    subject = "hey there *names*"
    
    # HTML content with template variables
    html_content = "<p>Dear *names*,</p><p>Your score was *scores*</p><p>Thanks!</p>"
    
    # Substitutions for template variables
    substitutions = {
        "*names*": "tere",
        "*scores*": "98"
    }
    
    # Send email
    print("Sending email...")
    result = email_service.send_email(
        from_email=from_email,
        to_email=to_email,
        to_name=to_name,
        subject=subject,
        html_content=html_content,
        substitutions=substitutions
    )
    
    # Print result
    if result["success"]:
        print("✅ Email sent successfully!")
        print(f"Status code: {result['status_code']}")
    else:
        print("❌ Failed to send email")
        print(f"Status code: {result['status_code']}")
        print(f"Response: {result['response_text']}")
        if "error" in result:
            print(f"Error: {result['error']}")


if __name__ == "__main__":
    main()