from rest_framework import serializers
from .models import (CheckList, Notification, StatusHistory, Task)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
