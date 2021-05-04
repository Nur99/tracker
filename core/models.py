from django.db import models
from auth_.models import MainUser
from utils import constants


class CheckList(models.Model):
    class Meta:
        verbose_name = 'Чеклист'
        verbose_name_plural = 'Чеклисты'

    short_name = models.CharField(max_length=50, verbose_name='Имя')
    finished = models.BooleanField(default=False, verbose_name='Сделан')

    def __str__(self):
        return '{} {}'.format(self.short_name, self.finished)


class Task(models.Model):
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    name = models.CharField(max_length=50, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание')
    executor = models.ForeignKey(MainUser, related_name='tasks', on_delete=models.CASCADE, verbose_name='исполнитель')
    observers = models.ManyToManyField(MainUser, blank=True, verbose_name='Наблюдатели', )
    status = models.CharField(max_length=10, choices=constants.STATUSES, verbose_name='Название')
    start_date = models.DateField(verbose_name='Время начала')
    finish_date = models.DateField(verbose_name='Время завершения')
    possible_finish_date = models.DateField(verbose_name='Планируемое время завершения')
    checklists = models.ManyToManyField(CheckList, blank=True, verbose_name='Чеклисты', )

    def __str__(self):
        return '{} {}'.format(self.name, self.status)


class StatusHistory(models.Model):
    class Meta:
        verbose_name = 'История статусов'
        verbose_name_plural = 'Историй статусов'

    task = models.ForeignKey(Task, related_name='status_history', on_delete=models.CASCADE, verbose_name='Название статуса')
    previous_status = models.CharField(max_length=10, choices=constants.STATUSES, verbose_name='Название')
    current_status = models.CharField(max_length=10, choices=constants.STATUSES, verbose_name='Название')
    author = models.ForeignKey(MainUser, related_name='history_changes', on_delete=models.CASCADE, verbose_name='Автор')

    def __str__(self):
        return '{} {}'.format(self.name, self.status)


class Notification(models.Model):
    class Meta:
        verbose_name = 'Напоминание'
        verbose_name_plural = 'Напоминаний'

    task = models.ForeignKey(Task, related_name='nots', on_delete=models.CASCADE, verbose_name='Название задачи')
    text = models.TextField(verbose_name='Текст сообщений')
    recipients = models.ManyToManyField(MainUser, blank=True, verbose_name='Наблюдатели', )    

    def __str__(self):
        return '{} {}'.format(self.task, self.task.name)
