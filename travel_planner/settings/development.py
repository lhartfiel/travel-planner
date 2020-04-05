from .defaults import *

SECRET_KEY = "qgiosyo2^%#*rsrm8_v+55xqp^czf!s2^*-9bp^&5^drv*$w=^"

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        # 'ENGINE': 'mysql.connector.django',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "travel_db",
        'USER': "admin",
        'PASSWORD': "password123",
        'HOST': "127.0.0.1",  # Or an IP Address that your DB is hosted on
        'PORT': "3306",
        'OPTIONS': {
            'autocommit': True,
            # 'use_pure': True
        },
    }
}


EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "travelpocketapp@gmail.com"
EMAIL_HOST_PASSWORD = "TravPlanner123"





