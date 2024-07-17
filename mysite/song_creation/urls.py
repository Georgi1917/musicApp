from django.urls import path
from song_creation.views import show_songs_page, create_song

urlpatterns = [
    path('songs/<int:album_id>', show_songs_page, name="song-page"),
    path('songs/<int:album_id>/create-song', create_song, name="create-song")
]