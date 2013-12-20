import mongoengine
try:
    from .credentials import (MONGODB_DB, MONGODB_USER, MONGODB_PWD)
except:
    from .credentials_production import (MONGODB_DB, MONGODB_USER, MONGODB_PWD)


mongoengine.connect(MONGODB_DB, username=MONGODB_USER, password=MONGODB_PWD,
                    tz_aware=True)  # `tz_aware' same to settings.USE_TZ
