from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from utils import constants
from .models import Task
from tracker.celery import app


@shared_task
def send_email(pk):
    task = Task.objects.get(id=pk)
    to_users = [observer["email"] for observer in task.observers.all().values("email")]
    send_mail(pk, constants.UPDATE_MESSAGE, settings.EMAIL_HOST_USER, to_users)


@app.task
def my_task():
    print(12)
