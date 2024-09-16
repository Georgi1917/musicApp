from django.db import models
from album_song_creation.models import Playlist

# Create your models here.

class Song(models.Model):
    name = models.CharField(max_length=60)
    author = models.CharField(max_length=60)
    file = models.FileField(upload_to='song_files/')
    duration = models.CharField(max_length=30, null=True)
    duration_in_seconds = models.CharField(max_length=30, null=True)
    album = models.ForeignKey(to=Playlist, on_delete=models.CASCADE, default=None)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super(Song, self).delete(*args, **kwargs)