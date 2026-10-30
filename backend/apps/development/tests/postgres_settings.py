"""Disposable loopback PostgreSQL only; never read a production connection URL."""
import os
from .settings import *  # noqa: F401,F403

DATABASES = {'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'mindmetric_stage6', 'USER': 'stage6test', 'PASSWORD': '',
    'HOST': '127.0.0.1', 'PORT': int(os.environ.get('STAGE6_POSTGRES_PORT', '55436')),
    'TEST': {'NAME': 'test_mindmetric_stage6'},
    'OPTIONS': {'connect_timeout': 5, 'options': '-c lock_timeout=10000 -c statement_timeout=30000'},
}}
SECRET_KEY = 'isolated-postgres-development-test-secret-only'
