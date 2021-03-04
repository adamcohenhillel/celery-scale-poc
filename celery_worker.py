# Can be run using the command: `celery -A celery_worker worker --loglevel=DEBUG`
# from celery import Celery
from main import make_celery


celery = make_celery()
