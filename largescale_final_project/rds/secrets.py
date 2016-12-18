import os

SECRET_KEY = '5#=fje(zd&2%@-x*3s)5v5k6@ipi27_w7e76&y&mdpu76nm2i+'

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_AUTH_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        },
        'auth_db': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_AUTH_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        },
        'db1' : {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_1_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        },
        'db2' : {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_2_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        },
    }
else:
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rental_app',
        'USER': 'appserver',
        'PASSWORD': 'foobarzoot',
        'HOST': 'aap1nfbft5yzor.cnj0nqnsfxth.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
        }
    }

EMAIL_PASSWORD = 'largescale'

# Database routers go here:
DATABASE_ROUTERS = ['renting_app.routers.UserRouter']
