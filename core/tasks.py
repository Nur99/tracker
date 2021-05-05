from datetime import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from utils import constants
from .models import Task, Notification
from tracker.celery import app


# @shared_task
def send_email(pk):
    task = Task.objects.get(id=pk)
    to_users = [observer["email"] for observer in task.observers.all().values("email")]
    send_mail(pk, constants.UPDATE_MESSAGE, settings.EMAIL_HOST_USER, to_users)
    Notification.objects.create(task=task, text=constants.UPDATE_MESSAGE, recipients=task.observers.all())


@app.task
def expired_tasks():
    for task in Task.objects.all():
        if task.finish_date > datetime.now():
            to_users = [task.executor.email, ] + \
                       [observer["email"] for observer in task.observers.all().values("email")]
            send_mail(task.id, constants.TASK_EXPIRED_MESSAGE, settings.EMAIL_HOST_USER, to_users)
            Notification.objects.create(task=task, text=constants.UPDATE_MESSAGE,
                                        recipients=task.observers.all() + task.executor)
