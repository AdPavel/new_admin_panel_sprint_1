import os
from dotenv import load_dotenv
from split_settings.tools import include
from pathlib import Path

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', False) == 'True'
ALLOWED_HOSTS = ['127.0.0.1']


# Application definition
include(
    'components/app_and_template.py'
)
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

include(
    'components/database.py'
)


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

include(
    'components/password_validation.py'
)


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

include(
    'components/internationalization.py'
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
