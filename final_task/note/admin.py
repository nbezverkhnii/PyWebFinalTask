from datetime import datetime, timedelta

from django.contrib import admin

from .models import Note, Comment


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """
    Настройка вида панели администратора для работы с моделью Note
    """
    # Отображение в режимепросмотра
    list_display = ('title', 'message', 'date_time', 'important')
    # Отображение полей в режиме редактирования
    fields = (('title', 'author'), 'message', ('visiability', 'public', 'status', 'important'))
    # Поля только для чтения в режиме редактирования
    readonly_fields = ('date_time',)
    # Поля для поиска
    search_fields = ('title', 'message')
    # Поля фильтрации
    list_filter = ['visiability', 'public', 'status', 'important']

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод для сохранения статьи без указания автора
        Теперь автор будет подставляться прямо из запроса request.user
        А дата = +1 день от даты создания
        """
        if not hasattr(obj, 'author') or not obj.author:
            obj.author = request.user
        if not hasattr(obj, 'date_time') or not obj.author:
            obj.date_time = datetime.now()+timedelta(days=1)
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Настройка вида панели администратора для работы с моделью Comment
    """
    # Отображение в режиме просмотра
    list_display = ('message', 'rating', 'date_add')
    # Отображение полей в режиме редактирования
    fields = ('note', 'author', 'message', 'rating', 'date_add')
    # Поля только для чтения в режиме редактирования
    readonly_fields = ('date_add',)
    # Поля для поиска
    search_fields = ('message', 'author')
    # Поля фильтрации
    list_filter = ['note', 'rating']

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод для сохранения без указания автора
        Теперь автор будет подставляться прямо из запроса request.user
        """
        if not hasattr(obj, 'author') or not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
