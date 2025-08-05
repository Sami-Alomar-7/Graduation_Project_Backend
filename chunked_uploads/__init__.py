# Django compatibility patch for django-chunked-upload
# This fixes the ugettext import issue in newer Django versions

import django.utils.translation
from django.utils.translation import gettext

# Monkey patch the django.utils.translation module to provide ugettext
# This is needed because django-chunked-upload expects ugettext to exist
if not hasattr(django.utils.translation, 'ugettext'):
    django.utils.translation.ugettext = gettext
