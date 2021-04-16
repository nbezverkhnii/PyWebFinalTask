from django.urls import path

from . import views

app_name = 'note'

urlpatterns = [
    path('note/', views.NoteView.as_view(), name='note'),
    path('note/add/', views.NoteEditorView.as_view(), name='add'),
    path('note/<int:note_id>/', views.OneNoteView.as_view(), name='one_note'),
    path('note/<int:note_id>/edit/', views.NoteEditorView.as_view(), name='edit'),
    path('note/<int:note_id>/del/', views.NoteEditorView.as_view(), name='del'),

    path('comment/<int:note_id>/', views.CommentView.as_view(), name='comment_get'),
    path('comment/<int:note_id>/add/', views.CommentEditorView.as_view(), name='comment_add'),
    path('comment/<int:comment_id>/del/', views.CommentEditorView.as_view(), name='comment_del'),
]
