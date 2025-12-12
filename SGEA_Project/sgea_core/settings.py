from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ngy@4#j42tsgv9pu&@mgddf9b-3b5(j75tnr6ny3$^3pa*pmc!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', 
    'inicio.apps.InicioConfig',
    'users.apps.UsersConfig',
    'events.apps.EventsConfig',
    'audit.apps.AuditConfig',
    'rest_framework',
    'rest_framework.authtoken',
]

# ID do site atual (1 = localhost configurado no banco)
SITE_ID = 1

# Define que o modelo de usuário é o personalizado
AUTH_USER_MODEL = 'users.Usuario'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sgea_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # O Django já procura dentro das pastas 'templates' de cada app (APP_DIRS=True)
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sgea_core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

# Alterado para o horário de Brasília para os logs ficarem corretos
TIME_ZONE = 'America/Sao_Paulo' 

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'sgea_core', 'static'),
]

# Configurações de Mídia (Uploads de usuários)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- CONFIGURAÇÕES DE AUTENTICAÇÃO E LOGIN ---

# URL para onde o usuário é enviado se tentar acessar uma página restrita sem estar logado
LOGIN_URL = 'login'

# URL para onde o usuário vai após fazer login com sucesso
LOGIN_REDIRECT_URL = '/eventos/' 

# URL para onde o usuário vai após fazer logout (vai para a home)
LOGOUT_REDIRECT_URL = '/'


# --- CONFIGURAÇÕES DE EMAIL (FILEBASED - ARQUIVO) ---
# Isso salva o e-mail numa pasta 'emails_enviados' na raiz do projeto
# Resolve o problema do link quebrando no terminal
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'emails_enviados')
DEFAULT_FROM_EMAIL = 'GoEvents! <noreply@goevents.com>'


# --- CONFIGURAÇÕES DO DJANGO REST FRAMEWORK ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    
    'DEFAULT_THROTTLE_RATES': {
        'events.list': '20/day', 
        'events.enroll': '50/day', 
    }
}