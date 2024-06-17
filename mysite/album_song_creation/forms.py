from django import forms
from album_song_creation.models import Playlist

class PlaylistForm(forms.Form):
    name = forms.CharField(max_length=15, required=True, label="Playlist Name:")
    description = forms.CharField(max_length=50, required=True, label="Playlist Description")
    logo = forms.ImageField(max_length=100, required=False, label="Logo")
