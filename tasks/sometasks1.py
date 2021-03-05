from time import sleep
import random
from celery import shared_task


@shared_task(bind=True, name='long_task')
def long_task(self):
    """Task that takes long time to run, but 
    in the meantime, it updates its progress
    so we can fetch it from api endpoint
    """
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = 1000
    
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        sleep(1)

    return {
        'current': 100,
        'total': 100,
        'status': 'Task completed!',
        'result': 42
    }
