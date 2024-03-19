from .base import *
from django.contrib.messages import constants as messages

SECRET_KEY = 'django-insecure-oxkve+727kqsw57lu$y5tcn&r%n2tc6l5frwm1=34rif(zjzbt'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MESSAGE_TAGS = { 
    messages.DEBUG : 'alert-info',
    messages.INFO : 'alert-info',
    messages.SUCCESS : 'alert-success',
    messages.WARNING : 'alert-warning',
    messages.ERROR: 'alert-danger'

}

EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = '0abbeaf851fa28'
EMAIL_HOST_PASSWORD = '7d2a4a944fd8b2'
EMAIL_PORT = '2525'



