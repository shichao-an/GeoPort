import os
from settings import *  # NOQA


DEBUG = False
TEMPLATE_DEBUG = DEBUG

STATIC_URL = 'https://s3.amazonaws.com/geoport/'
ALLOWED_HOSTS = ['geoport.co']

# `STATIC_ROOT` should be commented out if using S3 to serve static files
#STATIC_ROOT = os.path.join(PROJECT_PATH, "static_production")

# `DEFAULT_FILE_STORAGE` should be commented out if using local file storage
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# To manually collect static files to S3, be sure to use the following command:
# ./manage.py collectstatic --settings geoport.settings_production
# If any modified files are not synced, manually delete the file on S3 and
# run the above command again
AWS_STORAGE_BUCKET_NAME = "geoport"
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# Enable fast sync when using S3Boto
AWS_PRELOAD_METADATA = True

# redis://:password@hostname:port/db_number
BROKER_URL = 'redis://localhost:6379/0'
# 'redis://:password@host:port/db'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

FAVICON_PATH = os.path.join(STATIC_URL, 'img/favicon.png')
