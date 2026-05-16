import os

from .settings import *  # noqa: F403


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv('SQLITE_NAME', BASE_DIR / 'db.sqlite3'),  # noqa: F405
    }
}

MEDIA_ROOT = os.getenv('MEDIA_ROOT', BASE_DIR / 'media')  # noqa: F405

# Keep local demo flows from writing wizard state into SQLite sessions.
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
