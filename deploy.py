#!/usr/bin/env python3
"""
Quick deployment script for PharmaTrack
This script helps with common deployment tasks
"""

import os
import sys
import subprocess
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmatrack.settings')
django.setup()

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(e.stderr)
        return False

def main():
    print("🚀 PharmaTrack Deployment Script")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("manage.py").exists():
        print("❌ Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Run system checks
    if not run_command("python manage.py check", "Running system checks"):
        sys.exit(1)
    
    # Run migrations
    if not run_command("python manage.py migrate", "Running database migrations"):
        sys.exit(1)
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        sys.exit(1)
    
    # Create superuser if it doesn't exist
    from django.contrib.auth.models import User
    if not User.objects.filter(is_superuser=True).exists():
        print("👤 No superuser found. Creating one...")
        username = input("Enter superuser username (default: admin): ").strip() or "admin"
        email = input("Enter superuser email: ").strip()
        password = input("Enter superuser password: ").strip()
        
        if email and password:
            User.objects.create_superuser(username, email, password)
            print("✅ Superuser created successfully")
        else:
            print("⚠️ Skipping superuser creation")
    
    print("\n🎉 Deployment preparation completed!")
    print("\n📋 Next steps:")
    print("1. Set up your web server (Nginx, Apache)")
    print("2. Configure your WSGI server (Gunicorn, uWSGI)")
    print("3. Set up SSL certificate")
    print("4. Configure environment variables")
    print("5. Test your application")
    
    print("\n🔧 Useful commands:")
    print("   python manage.py runserver 0.0.0.0:8000  # Test locally")
    print("   gunicorn pharmatrack.wsgi:application    # Run with Gunicorn")
    print("   python manage.py collectstatic           # Collect static files")

if __name__ == "__main__":
    main()
