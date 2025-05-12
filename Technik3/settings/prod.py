#Prod.py complementa dados do base.py
from dotenv import load_dotenv
load_dotenv() #Carrega os dados sensíveis do arquivo .env

from .base import *
from decouple import config
import os

DEBUG = True #Está True para testes no servidor, mas o correto seria False

ALLOWED_HOSTS = ['technikpi.fly.dev'] #Host exclusivo para a URL em prod

CSRF_TRUSTED_ORIGINS = [
    'https://technikpi.fly.dev',
]

# Configuração do banco de dados Postgresql no Fly.io (usando variáveis de ambiente seguras)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('PROD_NAME', default='postgres'),
        'USER': config('PROD_USER', default='postgres'),
        'PASSWORD': config('PROD_PASSWORD', default='pe1InJlwLgXGX1L'),
        'HOST': config('PROD_HOST', default='technik-db.flycast'),
        'PORT': config('PROD_PORT', default='5432'),
    }
}

#INSTALANDO AS DEPENDÊNCIAS DO CLOUDNARY PARA SERVIR ARQUIVOS NA NUVEM SOMENTE EM PRODUÇÃO
INSTALLED_APPS += [
    'cloudinary',
    'cloudinary_storage',
]


CLOUDINARY_STORAGE = {
     'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
     'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
     'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),

}

#UPLOAD MÍDIA CLOUDNARY
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# CONFIGURAÇÕES RECOMENDADAS PARA SEGURANÇA
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ESSENCIAL PARA FLY.IO
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#print("🔧 [prod.py] Configurações de produção carregadas.") #Testes no console do Fly.io
#print("Storage em uso:", DEFAULT_FILE_STORAGE) #Teste no console do Fly.io

# Segurança extra em produção
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True