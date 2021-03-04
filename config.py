class LocalConfig:
    # Celery:
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


class WorkerConfig:
    # Celery:
    CELERY_BROKER_URL = 'redis://35.176.226.38:6379/0'
    CELERY_RESULT_BACKEND = 'redis://35.176.226.38:6379/0'