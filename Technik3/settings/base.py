from pathlib import Path
from decouple import config, Csv

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Segurança
SECRET_KEY = config('SECRET_KEY', default='chave-insegura-para-dev')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://127.0.0.1:8000', cast=Csv())

# Idioma e localização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Aplicativos instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'TechnikApp',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'TechnikApp.middleware.LastSeenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL e WSGI
ROOT_URLCONF = 'Technik3.urls'
WSGI_APPLICATION = 'Technik3.wsgi.application'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
            ],
        },
    },
]

# Arquivos estáticos (CSS, JS, IMG)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Redirecionamento de login/logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
APPEND_SLASH = True #redirecionamento

# Expirar sessão após 30 minutos de inatividade
SESSION_COOKIE_AGE = 1200  # Expissa sessão automatica 20min sem atividade
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  #Ao fechar navegador encerra sessão

# Chave primária padrão
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# E-mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_PASS', default='')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Validação de senha
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},

    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},

    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},

    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
