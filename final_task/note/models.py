from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


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
    date_time = models.DateTimeField(default=datetime.now()+timedelta(days=1), verbose_name='Дата публикации')
    public = models.BooleanField(verbose_name='Опубликовано')
    status = models.IntegerField(default=0, choices=STATUS, verbose_name='Статус')
    author = models.ForeignKey(User, related_name='author', on_delete=models.PROTECT, blank=True, verbose_name='Автор')

    def __str__(self):
        return str(self.title)

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
