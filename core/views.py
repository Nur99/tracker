from django.conf import settings
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import (TaskSerializer)
from .models import (CheckList, Notification, StatusHistory, Task)
from utils import constants
from core.tasks import send_email

import logging

logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    pagination_class = None

    def partial_update(self, request, *args, **kwargs):
        super(TaskViewSet, self).partial_update(request, *args, **kwargs)
        send_email(ph=self.get_object().id)
        #send_email.delay(pk=self.get_object().id)
        return Response(TaskSerializer(self.get_object()).data)
