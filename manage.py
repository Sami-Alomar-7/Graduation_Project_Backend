#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Django compatibility patch for django-chunked-upload
# This fixes the ugettext import issue in newer Django versions
import django.utils.translation
from django.utils.translation import gettext

# Monkey patch the django.utils.translation module to provide ugettext
# This is needed because django-chunked-upload expects ugettext to exist
if not hasattr(django.utils.translation, 'ugettext'):
    django.utils.translation.ugettext = gettext

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graduation_backend.settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()