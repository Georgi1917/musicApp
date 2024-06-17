from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Playlist(models.Model):
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='album_logos/', height_field=None, width_field=None, max_length=100)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=None)