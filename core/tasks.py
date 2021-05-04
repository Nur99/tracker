from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from utils import constants


@shared_task
def send_email(obj):
    to_users = [observer["email"] for observer in obj.observers.all().values("email")]
    send_mail(obj.id, constants.UPDATE_MESSAGE, settings.EMAIL_HOST_USER, to_users)