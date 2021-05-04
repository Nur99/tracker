import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracker.settings')

app = Celery('tracker')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "run-me-every-commit": {
        "task": "tracker.tasks.my_task",
        "schedule": crontab()
    }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
