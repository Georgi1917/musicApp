from django.urls import path
from album_creation import views

urlpatterns = [
    path('album-page/', views.PlaylistPage.as_view(), name='playlist-page'),
    path('create-playlist/', views.CreatePlaylist.as_view(), name="create-playlist"),
    path('edit-playlist/<int:album_id>/', views.show_album_edit_page, name="edit-playlist"),
    path('delete-playlist/<int:playlist_id>/', views.delete_playlist, name="delete-playlist"),
    path('unfollow-playlist/<int:playlist_id>/', views.unfollow_playlist, name="unfollow")
]