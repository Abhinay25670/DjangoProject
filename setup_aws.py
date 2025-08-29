#!/usr/bin/env python3
"""
AWS Deployment Setup Script for PharmaTrack
This script helps configure your Django application for AWS deployment.
"""

import os
import secrets
import string
from pathlib import Path

def generate_secret_key():
    """Generate a secure Django secret key"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    return ''.join(secrets.choice(alphabet) for _ in range(50))

def create_env_file():
    """Create a .env file with default values"""
    env_content = f"""# Django Settings
SECRET_KEY={generate_secret_key()}
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development, change to PostgreSQL for production)
DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
EMAIL_VERIFICATION_TIMEOUT_HOURS=24

# AWS S3 (Optional - for static files)
USE_S3=False
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with default values")
    print("⚠️  Please update the .env file with your actual credentials")

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'django',
        'gunicorn',
        'whitenoise',
        'psycopg2-binary',
        'dj-database-url',
        'reportlab',
        'openpyxl',
        'xlsxwriter'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed")
        return True

def create_directories():
    """Create necessary directories"""
    directories = ['logs', 'staticfiles', 'media']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Created necessary directories")

def check_django_setup():
    """Check Django configuration"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmatrack.settings')
        import django
        django.setup()
        
        from django.conf import settings
        print("✅ Django settings are valid")
        
        # Check if database is accessible
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection is working")
        
    except Exception as e:
        print(f"❌ Django setup issue: {e}")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 PharmaTrack AWS Deployment Setup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return
    
    # Create directories
    create_directories()
    
    # Check Django setup
    if not check_django_setup():
        return
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        create_env_file()
    else:
        print("✅ .env file already exists")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Update .env file with your actual credentials")
    print("2. Install AWS CLI: https://docs.aws.amazon.com/cli/")
    print("3. Install EB CLI: pip install awsebcli")
    print("4. Configure AWS credentials: aws configure")
    print("5. Run deployment: ./deploy.sh")
    print("\nFor detailed instructions, see: aws_deployment_guide.md")

if __name__ == "__main__":
    main() 