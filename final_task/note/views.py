from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from .models import Note, Comment
from .serializers import OneNoteViewSerializer, NoteViewSerializer, NoteEditorSerializer


class OneNoteView(APIView):
    """

    """
    def get(self, request, note_id):
        """

        """
        note = Note.objects.filter(pk=note_id, public=True).first()

        if not note:
            raise NotFound(f'Опубликованная статья с id={note_id} не найдена')

        serializer = OneNoteViewSerializer(note)
        return Response(serializer.data)


class NoteView(APIView):
    """

    """
    def get(self, request, note_id):
        """

        :param request:
        :param note_id:
        :return:
        """

        notes = Note.objects.filter(public=True).order_by('date_time').order_by('status')

        if not notes:
            raise NotFound(f'Опубликованная статья с id={note_id} не найдена')

        serializer = OneNoteViewSerializer(notes, many=True)

        return Response(serializer.data)


class NoteEditorView(APIView):
    """

    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """

        """
        new_note = NoteEditorSerializer(data=request.data)

        if new_note.is_valid():
            new_note.save(author=request.user)
            return Response(new_note.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, note_id):
        """

        """
        note = Note.objects.filter(pk=note_id, author=request.user).first()
        if not note:
            raise NotFound(f'Статья с id={note_id} у пользователя {request.user.username} не найдена')

        new_note = NoteEditorSerializer(note, data=request.data, partial=True)

        if new_note.is_valid():
            new_note.save(author=request.user)
            return Response(new_note.data, status=status.HTTP_201_CREATED)
        else:
            return Response(new_note.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):
        """

        """
        article = Note.objects.filter(pk=note_id, author=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






