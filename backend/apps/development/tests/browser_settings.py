"""Explicit disposable database for the real-browser smoke test only."""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from .settings import *  # noqa: F401,F403

browser_database = os.environ.get('DEVELOPMENT_BROWSER_DB_PATH')
if not browser_database or Path(browser_database).resolve() == (BASE_DIR / 'db.sqlite3').resolve():
    raise ImproperlyConfigured('A separate DEVELOPMENT_BROWSER_DB_PATH is required.')
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': browser_database}}
DEVELOPMENT_CLUSTER1_ENABLED = True
SECRET_KEY = 'disposable-development-browser-secret-key-only'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
MIDDLEWARE = [entry for entry in MIDDLEWARE if 'whitenoise' not in entry]
STORAGES = {'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'}}
