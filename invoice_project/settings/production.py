from .base import *

DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY")

HOST = os.environ.get('HOST', '')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')

CSRF_TRUSTED_ORIGINS = ['https://*.' + HOST, ]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASS"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": int(os.getenv("DB_PORT"))
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('SSL_PORT', 465))
EMAIL_USE_TLS = False
EMAIL_HOST_USER = os.environ.get('EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
EMAIL_USE_SSL = True
