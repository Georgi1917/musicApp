from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Playlist(models.Model):
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=50)
    logo = models.ImageField(
        upload_to='album_logos/', 
        height_field=None, width_field=None, 
        max_length=100,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=None, related_name="playlists")

    def delete(self, *args, **kwargs):
        self.logo.delete()
        super(Playlist, self).delete(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
    

class FollowedPlaylist(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="followed_playlists")
    playlist = models.ForeignKey(to=Playlist, on_delete=models.CASCADE, related_name="users_following")