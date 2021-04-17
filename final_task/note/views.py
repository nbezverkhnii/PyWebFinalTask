from rest_framework import status as st
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from .models import Note, Comment
from .serializers import OneNoteViewSerializer, NoteEditorSerializer, QuerySerializer, CommentViewSerializer, CommentAddSerializer


class OneNoteView(APIView):
    """
    APIView для получения одной заметки
    """
    def get(self, request, note_id):
        """
        Энд-поинт для получения одной зметки
        """
        note = Note.objects.filter(pk=note_id, public=True).first()

        if not note:
            raise NotFound(f'Опубликованная статья с id={note_id} не найдена')

        serializer = OneNoteViewSerializer(note)
        return Response(serializer.data)


class NoteView(APIView):
    """
    APIView для получения всех заметок
    """
    def get(self, request):
        """
        Энд-поинт для получения всех заметок
        """

        notes = Note.objects.filter(public=True).order_by('date_time').order_by('status')
        if not notes:
            raise NotFound(f'Заметок нет')

        query_params = QuerySerializer(data=request.query_params)
        if query_params.is_valid():
            q_full = Q()
            q_status = Q()
            if query_params.data.get('status'):
                for value in query_params.data['status']:
                    q_status |= Q(status=value)
            if query_params.data.get('important'):
                q_full &= Q(important=query_params.data['important'])
            if query_params.data.get('visiability'):
                q_full &= Q(visiability=query_params.data['visiability'])
            notes = notes.filter(q_status & q_full)
        else:
            return Response(query_params.errors, status=st.HTTP_400_BAD_REQUEST)

        serializer = OneNoteViewSerializer(notes, many=True)

        return Response(serializer.data)


class NoteEditorView(APIView):
    """
    APIView для редактирования заметок
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Энд-поинт для добавления заметки
        """
        new_note = NoteEditorSerializer(data=request.data)

        if new_note.is_valid():
            new_note.save(author=request.user)
            return Response(new_note.data, status=st.HTTP_201_CREATED)
        else:
            return Response(new_note.errors, status=st.HTTP_400_BAD_REQUEST)

    def patch(self, request, note_id):
        """
        Энд-поинт для изменения заметки
        """
        note = Note.objects.filter(pk=note_id, author=request.user).first()
        if not note:
            raise NotFound(f'Статья с id={note_id} у пользователя {request.user.username} не найдена')

        new_note = NoteEditorSerializer(note, data=request.data, partial=True)

        if new_note.is_valid():
            new_note.save(author=request.user)
            return Response(new_note.data, status=st.HTTP_201_CREATED)
        else:
            return Response(new_note.errors, status=st.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):
        """
        Энд-поинт для удаления заметки
        """
        note = Note.objects.filter(pk=note_id, author=request.user).delete()
        return Response(status=st.HTTP_204_NO_CONTENT)


class CommentView(APIView):
    """
    APIView для получения комментариев
    """
    def get(self, request, note_id):
        """
        Энд-поинет для получения комментариев к заметке с note_id
        """
        comment = Comment.objects.filter(note=note_id)
        if not comment:
            raise NotFound(f'У заметки с id={note_id} нет комментариев')

        serializer = CommentViewSerializer(comment, many=True)
        return Response(serializer.data)


class CommentEditorView(APIView):
    """
    Комментарии к заметкам
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, note_id):
        """
        Энд-поинет для доавления комментариев к заметке с note_id
        """
        note = Note.objects.filter(id=note_id).first()
        if not note:
            raise NotFound(f'Заметка с id={note_id} не найдена')

        new_comment = CommentAddSerializer(data=request.data)
        if new_comment.is_valid():
            new_comment.save(note=note, author=request.user)
            return Response(new_comment.data, status=st.HTTP_201_CREATED)
        else:
            return Response(new_comment.errors, status=st.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        """
        Энд-поинет для удаления комментариев к заметке с note_id
        """
        comment = Comment.objects.filter(pk=comment_id, author=request.user)
        comment.delete()
        return Response(status=st.HTTP_204_NO_CONTENT)
