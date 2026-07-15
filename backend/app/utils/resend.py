import resend
import os
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv('RESEND_API_KEY')

def send_email(to: str, subject: str, html_content: str):
    try:
        response = resend.Emails.send({
            'from': os.getenv('RESEND_FROM_EMAIL', 'noreply@yourdomain.com'),
            'to': to,
            'subject': subject,
            'html': html_content
        })
        return response
    except Exception as e:
        raise Exception(f"Email sending failed: {str(e)}")