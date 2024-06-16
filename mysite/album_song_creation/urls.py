from django.urls import path
from album_song_creation.views import show_album_creation_page

urlpatterns = [
    path('/create-album', show_album_creation_page, name="album")
]