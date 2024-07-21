from django import forms
from django.forms import ModelForm
from song_creation.models import Song

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['name', 'author', 'file']