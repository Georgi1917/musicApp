from django import forms
from django.forms import ModelForm
from song_creation.models import Song
from song_creation.validators import validate_file_is_mp3

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['name', 'author', 'file']

    def __init__(self, *args, **kwargs):
        super(SongForm, self).__init__(*args, **kwargs)
        self.fields["file"].validators.append(validate_file_is_mp3)