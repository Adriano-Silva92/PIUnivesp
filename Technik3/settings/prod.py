from dotenv import load_dotenv
load_dotenv()

from .base import *
from decouple import config
import os

DEBUG = True

ALLOWED_HOSTS = ['technikpi.fly.dev']

CSRF_TRUSTED_ORIGINS = [
    'https://technikpi.fly.dev',
]

# Configuração do banco de dados do Fly.io (usando variáveis de ambiente seguras)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('PROD_NAME', default='postgres'),
        'USER': config('PROD_USER', default='postgres'),
        'PASSWORD': config('PROD_PASSWORD'),
        'HOST': config('PROD_HOST', default='technik-db.flycast'),
        'PORT': config('PROD_PORT', default='5432'),
    }
}

#INSTALANDO AS DEPENDÊNCIAS DO CLOUDNARY SERVIR ARQUIVOS NA NUVEM SOMENTE EM PRODUÇÃO
INSTALLED_APPS += [
    'cloudinary',
    'cloudinary_storage',
]

#UPLOAD MÍDIA CLOUDNARY
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
     'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
     'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
     'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),

}

# CONFIGURAÇÕES RECOMENDADAS PARA SEGURANÇA
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ESSENCIAL PARA FLY.IO
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

print("🔧 [prod.py] Configurações de produção carregadas.")
print("Storage em uso:", DEFAULT_FILE_STORAGE)