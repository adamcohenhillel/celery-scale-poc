from random import randint
from celery import shared_task


@shared_task(bind=True, name='random_task')
def random_task(self):
    """Task that get random int, sleep, and return
    in the meantime, it updates its progress
    """
    time.sleep(randint(1, 1000))
    return {'msg': 'Random done',}
