"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x%g%o!l*z&e7fjjlbayh98cxg)%#t*d$^=dze@)u93w-ws^#36'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',
    'corsheaders',
    'orders',
    'rest_framework',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
# place corsMiddlerware before django's commonMiddleware

# The reason CorsMiddleware should come before CommonMiddleware is about the handling of HTTP responses:
# Pre-Processing of Requests: CorsMiddleware needs to process the request first to add the necessary CORS headers. If a request from a non-allowed origin gets processed by other middlewares before it reaches CorsMiddleware, there might be cases where CORS headers won't be added correctly, leading to CORS errors on the client side.
# Handling HTTP Redirects: If CommonMiddleware redirects a request (e.g., appending a slash to the URL) before CorsMiddleware gets to process it, the redirect response may not include the necessary CORS headers. As a result, browsers will block the response due to CORS policy violations.
# Optimizing Response Time: Handling CORS before other potentially time-consuming middleware can optimize response times for blocked cross-origin requests, as it avoids unnecessary processing for requests that will ultimately be rejected due to CORS policies.
    
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Note : using PyMongo will mean to establish MongoDB connection directly in the code(pymongo.py)
# commented to use to connect to PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER':'postgres',
        'PASSWORD':'postgres',
        'HOST':'104.198.198.1',
        'PORT':'5432'
    },
    'auth_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'auth_db',
        'USER':'admin',
        'PASSWORD':'admin',
        'HOST':'104.198.198.1',
        'PORT':'5432'
    },
    'transaction_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'transaction_db',
        'USER':'admin',
        'PASSWORD':'admin',
        'HOST':'104.198.198.1',
        'PORT':'5432'
    }
}

DATABASES_ROUTERS = ['ecommerce.routers.PostgresRouter']

AUTH_USER_MODEL = 'users.CustomUser'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
}

# Ensure CSRF_COOKIE_NAME is set to the default or matches your frontend configuration
CSRF_COOKIE_NAME = 'csrftoken'  
CSRF_COOKIE_DOMAIN = 
# Ensure CSRF_COOKIE_HTTPONLY is False if you need to read the CSRF token with JavaScript
CSRF_COOKIE_HTTPONLY = False  

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Frontend application origin
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

# logging setting 
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
