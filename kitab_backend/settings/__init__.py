"""
Django Settings Package for Kitab Backend
Bu package development, production və Heroku settings fayllarını təqdim edir
"""

import os

# Environment-based settings selection
DJANGO_ENV = os.getenv('DJANGO_ENV', 'development')
IS_HEROKU = os.getenv('IS_HEROKU', 'False').lower() == 'true'

if IS_HEROKU:
    # Heroku environment
    from .heroku import *
elif DJANGO_ENV == 'production':
    # Production environment
    from .production import *
else:
    # Development environment
    from .development import * 