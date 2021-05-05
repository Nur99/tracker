from rest_framework import serializers
from .models import (CheckList, Notification, StatusHistory, Task)
from auth_.models import MainUser


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def complete(self, task, new_status):
        if task.status != new_status:
            author = MainUser.objects.get(id=self.context.get('request').user.id)
            StatusHistory.objects.create(task=task,
                                         previous_status=task.status,
                                         current_status=new_status,
                                         author=author)
