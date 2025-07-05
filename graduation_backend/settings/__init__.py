"""
Settings package for graduation_backend project.
"""
import os

# Set the default settings module based on the environment
DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')

if DJANGO_ENV == 'production':
    from .production import *
else:
    from .development import * 