
# Can be run using the command:
# `celery -A worker.celery worker -l info -Q queueName`
from celery import Celery

from config import WorkerConfig


celery = Celery(
    'cadoHardWorker',
    broker=WorkerConfig.CELERY_BROKER_URL,
    backend=WorkerConfig.CELERY_RESULT_BACKEND,
    include=['tasks']
)
