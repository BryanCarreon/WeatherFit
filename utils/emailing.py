import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("RECIPIENT_EMAIL")  # testing from .env

def send_weather_email(subject, body, recipient_email = None):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipient_email or TO_EMAIL
        
        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            
            print("Email sent!")

    except Exception as e:
        print("Failed to send email:", e)