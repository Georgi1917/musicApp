from django.urls import path
from album_creation import views

urlpatterns = [
    path('album-page/', views.playlist_page, name='playlist-page'),
    path('create-playlist/', views.show_album_creation_page, name="create-playlist"),
    path('edit-playlist/<int:album_id>/', views.show_album_edit_page, name="edit-playlist"),
    path('delete-playlist/<int:playlist_id>/', views.delete_playlist, name="delete-playlist")
]