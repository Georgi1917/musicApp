from django.urls import path
from song_creation.views import show_songs_page, create_song, edit_song

urlpatterns = [
    path('songs/<int:album_id>', show_songs_page, name="song-page"),
    path('songs/<int:album_id>/create-song', create_song, name="create-song"),
    path('songs/<int:album_id>/edit-song/<int:song_id>', edit_song, name="edit-song")
]