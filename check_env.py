import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graduation_backend.settings.development')
django.setup()

from django.conf import settings

print("=== ENVIRONMENT VARIABLES ===")
print(f"EMAIL_BACKEND: {os.getenv('EMAIL_BACKEND')}")
print(f"GMAIL_API_CLIENT_ID: {os.getenv('GMAIL_API_CLIENT_ID')}")
print(f"GMAIL_API_CLIENT_SECRET: {os.getenv('GMAIL_API_CLIENT_SECRET')}")
print(f"GMAIL_API_REFRESH_TOKEN: {os.getenv('GMAIL_API_REFRESH_TOKEN')}")
print(f"GMAIL_API_USER: {os.getenv('GMAIL_API_USER')}")

print("\n=== DJANGO SETTINGS ===")
print(f"EMAIL_BACKEND: {getattr(settings, 'EMAIL_BACKEND', 'Not set')}")
print(f"GMAIL_API_CLIENT_ID: {getattr(settings, 'GMAIL_API_CLIENT_ID', 'Not set')}")
print(f"GMAIL_API_USER: {getattr(settings, 'GMAIL_API_USER', 'Not set')}") 