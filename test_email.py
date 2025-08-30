#!/usr/bin/env python
"""
Simple email test script to verify SendGrid configuration
Run this locally to test your email setup before deploying
"""

import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmatrack.railway_settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    print("=== Email Configuration Test ===")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"SENDGRID_API_KEY: {'Set' if os.environ.get('SENDGRID_API_KEY') else 'Not set'}")
    print()
    
    try:
        # Test email sending
        print("Attempting to send test email...")
        send_mail(
            subject='Test Email from PharmaTrack',
            message='This is a test email to verify email configuration.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['abhinay02005@gmail.com'],  # Replace with your email
            fail_silently=False,
        )
        print("✅ Test email sent successfully!")
        
    except Exception as e:
        print(f"❌ Error sending test email: {str(e)}")
        print(f"Error type: {type(e).__name__}")

if __name__ == '__main__':
    test_email()
