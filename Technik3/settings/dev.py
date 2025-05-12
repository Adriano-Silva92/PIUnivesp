#Dev.py carrega os dados de base.py + dev.py no modo desenvolvimento
from dotenv import load_dotenv
load_dotenv() #Carrega os dados sensíveis do arquivo .env

from .base import * #Importa dados do base.py
from decouple import config
import os

DEBUG = True

STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

ALLOWED_HOSTS = ["*"] #nenhum host definido, qualquer url é aceita no modo dev

INSTALLED_APPS += [
    'cloudinary',
    'cloudinary_storage',
]

CLOUDINARY_STORAGE = {
     'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
     'API_KEY': config('CLOUDINARY_API_KEY'),
     'API_SECRET': config('CLOUDINARY_API_SECRET'),

}

#UPLOAD MÍDIA CLOUDNARY
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

#CONFIGURAÇÃO DO BANCO DE DADOS POSTGRESQL
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
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]