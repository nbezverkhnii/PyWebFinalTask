from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    """

    """
    STATUS = (
        (0, 'Активно'),
        (1, 'Отложено'),
        (2, 'Выполнено'),
    )

    title = models.CharField(max_length=250, null=False, verbose_name='Заголовок')
    massage = models.TextField(verbose_name='Текст')
    date_time = models.DateTimeField(..., verbose_name='Время публикации')
    public = models.BooleanField(verbose_name='Опубликовано')
    status = models.IntegerField(default=0, choices=STATUS, verbose_name='Статус')
    author = models.ForeignKey(User, related_name='author', on_delete=models.PROTECT, blank=True, verbose_name='Автор')

