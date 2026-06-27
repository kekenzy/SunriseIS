import os
os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-testing-only')
os.environ.setdefault('POSTGRES_DB', 'test')
os.environ.setdefault('POSTGRES_USER', 'test')
os.environ.setdefault('POSTGRES_PASSWORD', 'test')

from .settings import *  # noqa

SECRET_KEY = 'test-secret-key-for-testing-only'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
