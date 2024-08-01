from settings import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

MIDDLEWARE.append('silk.middleware.SilkyMiddleware')
INSTALLED_APPS.append('silk')
SILKY_PYTHON_PROFILER = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'development.sqlite3'),
    }
}
