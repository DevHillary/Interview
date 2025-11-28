import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('crm')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Only configure Celery if broker URL is provided
if settings.CELERY_BROKER_URL:
    # Load task modules from all registered Django apps.
    app.autodiscover_tasks()

    # Configure periodic tasks
    app.conf.beat_schedule = {
        'check-reminders-every-minute': {
            'task': 'crm.tasks.check_reminders',
            'schedule': crontab(minute='*/1'),  # Run every minute
        },
    }
else:
    print("Warning: CELERY_BROKER_URL not set. Celery tasks will run synchronously.")


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

