import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailService:
    """
    Email service that sends emails via Gmail SMTP.
    Falls back to console logging if SMTP credentials are not configured.
    """
    
    @staticmethod
    def send_email(to: str, subject: str, body: str):
        # Try to send via Gmail SMTP first
        try:
            # Get SMTP credentials from environment variables
            smtp_email = os.getenv("SMTP_EMAIL")
            smtp_password = os.getenv("SMTP_PASSWORD")
            
            if smtp_email and smtp_password:
                return EmailService._send_via_smtp(to, subject, body, smtp_email, smtp_password)
            else:
                print("SMTP credentials not configured, falling back to console logging")
                return EmailService._log_to_console(to, subject, body)
                
        except Exception as e:
            print(f"SMTP sending failed: {e}, falling back to console logging")
            return EmailService._log_to_console(to, subject, body)
    
    @staticmethod
    def _send_via_smtp(to: str, subject: str, body: str, smtp_email: str, smtp_password: str):
        """Send email via Gmail SMTP."""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = smtp_email
            msg['To'] = to
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MIMEText(body, 'plain'))
            
            # Gmail SMTP configuration
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # Enable security
            server.login(smtp_email, smtp_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(smtp_email, to, text)
            server.quit()
            
            print(f"Email sent successfully to {to}")
            
            return {
                "type": "email",
                "method": "smtp",
                "details": {
                    "to": to,
                    "subject": subject,
                    "status": "sent",
                    "timestamp": datetime.now().isoformat(),
                    "smtp_server": "smtp.gmail.com"
                }
            }
            
        except Exception as e:
            print(f"SMTP error: {e}")
            raise e
    
    @staticmethod
    def _log_to_console(to: str, subject: str, body: str):
        """Fallback method that logs email to console."""
        print(f"--- [EMAIL LOGGED] ---")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"----------------------")
        
        return {
            "type": "email",
            "method": "console",
            "details": {
                "to": to,
                "subject": subject,
                "status": "logged",
                "timestamp": datetime.now().isoformat(),
                "note": "Email logged to console - SMTP not configured"
            }
        }
