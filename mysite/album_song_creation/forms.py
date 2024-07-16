from django import forms
from django.forms import ModelForm
from album_song_creation.models import Playlist

class PlaylistForm(ModelForm):
    class Meta:
        model = Playlist
        fields = ["name", "description", "logo"]
