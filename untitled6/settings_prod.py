DEBUG = False
ALLOWED_HOSTS = ['*']
# либо адрес севера

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db2',
        'USER': 'django_shop',
        'PASSWORD': 'goodpas07',
        'HOST': 'localhost',
        'PORT': '',
    }
}
