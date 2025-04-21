from dotenv import load_dotenv
load_dotenv()

from .base import *
from decouple import config

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DEV_NAME', default='DBTechnik'),
        'USER': config('DEV_USER', default='postgres'),
        'PASSWORD': config('DEV_PASSWORD'),
        'HOST': config('DEV_HOST', default='localhost'),
        'PORT': config('DEV_PORT', default='5432'),
    }
}

# Arquivos de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"