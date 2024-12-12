from django.urls import path
from song_creation import views

urlpatterns = [
    path('songs/<int:album_id>/', views.show_songs_page, name="song-page"),
    path('songs/<int:album_id>/create-song/', views.create_song, name="create-song"),
    path('songs/<int:album_id>/edit-song/<int:song_id>/', views.edit_song, name="edit-song"),
    path('songs/<int:album_id>/delete-song/<int:song_id>/', views.delete_song, name="delete-song"),
    path('followed-songs/<int:playlist_id>/', views.followed_playlist_songs, name="followed-songs")
]