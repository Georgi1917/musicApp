from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class Playlist(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, default=None, related_name="playlists")

    def __str__(self) -> str:
        return self.name
    

class FollowedPlaylist(models.Model):

    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name="followed_playlists")
    playlist = models.ForeignKey(to=Playlist, on_delete=models.CASCADE, related_name="users_following")