from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    """
    Заметка
    """
    status = (
        (0, 'Активно'),
        (1, 'Отложено'),
        (2, 'Выполнено'),
    )
    publication_day = datetime.now()+timedelta(days=1)

    title = models.CharField(max_length=250, null=False, verbose_name='Заголовок')
    message = models.TextField(default='', blank=True, verbose_name='Текст')
    date_time = models.DateTimeField(default=publication_day, blank=True, verbose_name='Дата публикации')
    important = models.BooleanField(default=False, blank=True, verbose_name='Важно')
    visiability = models.BooleanField(default=True, blank=True, verbose_name='Публичность')
    public = models.BooleanField(default=True, verbose_name='Опубликовано', blank=True)
    status = models.IntegerField(default=0, choices=status, blank=True, verbose_name='Статус')
    author = models.ForeignKey(User, related_name='author', on_delete=models.PROTECT, blank=True, verbose_name='Автор')

    def __str__(self):
        return f'{self.get_status_display()}: {self.title}'

    class Meta:
        verbose_name = 'Заметки'
        verbose_name_plural = 'Заметки'


class Comment(models.Model):
    """
    Комментарии и оценки к статьям
    """
    RATINGS = (
        (0, 'Без оценки'),
        (1, 'Ужасно'),
        (2, 'Плохо'),
        (3, 'Нормально'),
        (4, 'Хорошо'),
        (5, 'Отлично'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, related_name='comments', on_delete=models.CASCADE, verbose_name='Заметка')
    date_add = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    message = models.TextField(default='', blank=True, verbose_name='Текст комментария')
    rating = models.IntegerField(default=0, choices=RATINGS, verbose_name='Оценка')

    def __str__(self):
        return f'{self.get_rating_display()}: {self.message or "Без комментариев"}'

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'
