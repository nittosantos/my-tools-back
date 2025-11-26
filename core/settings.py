from pathlib import Path
import os
from datetime import timedelta
import dj_database_url
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-ix0_4s(+i-ybcky^+hg&3r@t_o#t((_i4fbnq7&7opf8%iz+*=')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') if os.environ.get('ALLOWED_HOSTS') else ['*']


# Application definition

INSTALLED_APPS = [
    'colorfield',
    'admin_interface',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',  # Cloudinary para armazenamento de mídia (deve vir antes de staticfiles)
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',  # Swagger/OpenAPI documentation
    'corsheaders',  # CORS headers para permitir requisições do frontend
    'cloudinary',  # SDK do Cloudinary
    'marketplace',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise para servir arquivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware (deve vir antes de CommonMiddleware)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Usa DATABASE_URL se disponível (Railway fornece isso), senão usa SQLite para desenvolvimento
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
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

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Diretório onde os arquivos estáticos serão coletados

# Garantir que o diretório staticfiles existe
STATIC_ROOT.mkdir(parents=True, exist_ok=True)

STATICFILES_DIRS = [
    BASE_DIR / 'core' / 'static',
]

# WhiteNoise para servir arquivos estáticos em produção
# Usa CompressedStaticFilesStorage (mais simples) em vez de CompressedManifestStaticFilesStorage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração de Mídia (Imagens)
# Configuração do Cloudinary
CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY', '')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', '')

# Se Cloudinary estiver configurado, configura o Cloudinary
if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api

    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET
    )

    # Configuração para django-cloudinary-storage (caso ainda use ImageField em outros lugares)
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
        'API_KEY': CLOUDINARY_API_KEY,
        'API_SECRET': CLOUDINARY_API_SECRET,
    }
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    MEDIA_URL = '/media/'
else:
    # Usa armazenamento local (desenvolvimento)
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 9 itens por página (3 linhas x 3 colunas no grid) para alinhar com o frontend
    'PAGE_SIZE': 9,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=12),  # dura 12 horas
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),   # dura 7 dias
}

# Configurações do drf-spectacular (Swagger/OpenAPI)
SPECTACULAR_SETTINGS = {
    'TITLE': 'My Tools API',
    'DESCRIPTION': 'API REST para marketplace de aluguel de ferramentas. Sistema desenvolvido em Django REST Framework.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,  # Permite multipart/form-data
    'SCHEMA_PATH_PREFIX': '/api/',
    # Servidores disponíveis no Swagger (permite alternar entre ambientes)
    'SERVERS': [
        {
            'url': os.environ.get('RAILWAY_PUBLIC_DOMAIN', 'http://127.0.0.1:8000'),
            'description': 'Servidor de produção' if os.environ.get('RAILWAY_PUBLIC_DOMAIN') else 'Servidor local'
        },
    ],
    'TAGS': [
        {'name': 'Autenticação', 'description': 'Endpoints de autenticação JWT'},
        {'name': 'Ferramentas', 'description': 'CRUD de ferramentas disponíveis para aluguel'},
        {'name': 'Aluguéis', 'description': 'Gerenciamento de aluguéis de ferramentas'},
    ],
}

# Configuração CORS - Permite requisições do frontend
# Em produção, use variável de ambiente CORS_ALLOWED_ORIGINS separada por vírgula
# IMPORTANTE: As origens NÃO podem ter barra final ou path (apenas domínio)
CORS_ALLOWED_ORIGINS_ENV = os.environ.get('CORS_ALLOWED_ORIGINS', '')
if CORS_ALLOWED_ORIGINS_ENV:
    # Remove espaços e remove barra final se houver (django-cors-headers não permite paths)
    CORS_ALLOWED_ORIGINS = [
        origin.strip().rstrip('/')
        for origin in CORS_ALLOWED_ORIGINS_ENV.split(',')
        if origin.strip()
    ]
else:
    # Desenvolvimento local
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",  # Vite dev server (porta padrão)
        "http://127.0.0.1:5173",  # Vite dev server (IP local)
        "http://localhost:3000",  # Caso use outra porta
        "http://127.0.0.1:3000",  # Caso use outra porta
    ]

# Debug: Log das origens permitidas
if DEBUG:
    print(f"[DEBUG] CORS_ALLOWED_ORIGINS: {CORS_ALLOWED_ORIGINS}")
else:
    # Em produção, sempre log para debug
    print(f"[CORS] CORS_ALLOWED_ORIGINS_ENV (raw): '{CORS_ALLOWED_ORIGINS_ENV}'")
    print(f"[CORS] CORS_ALLOWED_ORIGINS (parsed): {CORS_ALLOWED_ORIGINS}")
    if not CORS_ALLOWED_ORIGINS_ENV:
        print("[WARNING] CORS_ALLOWED_ORIGINS não configurado! Usando apenas localhost.")
    elif not CORS_ALLOWED_ORIGINS:
        print("[ERROR] CORS_ALLOWED_ORIGINS está vazio após parsing!")

# Permite credenciais (cookies, headers de autenticação)
CORS_ALLOW_CREDENTIALS = True

# Métodos HTTP permitidos
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Headers permitidos
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Expor headers customizados
CORS_EXPOSE_HEADERS = [
    'content-type',
    'x-total-count',
]

# Configurações de Segurança para Produção
# Aplicadas apenas quando DEBUG=False (produção)
if not DEBUG:
    # HTTPS/SSL - Desabilitado temporariamente para evitar conflitos com Railway
    # O Railway já gerencia HTTPS automaticamente através do proxy reverso
    # SECURE_SSL_REDIRECT = True  # Comentado para evitar problemas com CORS

    SESSION_COOKIE_SECURE = True  # Cookies apenas via HTTPS
    CSRF_COOKIE_SECURE = True  # CSRF cookies apenas via HTTPS
    SECURE_BROWSER_XSS_FILTER = True  # Proteção XSS
    SECURE_CONTENT_TYPE_NOSNIFF = True  # Previne MIME type sniffing
    X_FRAME_OPTIONS = 'DENY'  # Previne clickjacking

    # HSTS (HTTP Strict Transport Security) - força HTTPS por 1 ano
    SECURE_HSTS_SECONDS = 31536000  # 1 ano
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Previne redirecionamento para sites não confiáveis
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'