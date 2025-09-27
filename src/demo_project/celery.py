import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_project.settings')

app = Celery('demo_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'sample-task-every-minute': {
        'task': 'tasks.tasks.sample_task',
        'schedule': crontab(minute='*/1'),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')