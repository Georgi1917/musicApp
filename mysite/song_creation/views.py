from django.shortcuts import render, redirect
from album_song_creation.models import Playlist
from song_creation.models import Song
from song_creation.forms import SongForm
from django.contrib import messages
import os
from django.conf import settings
from song_creation import helper_functions

# Create your views here.

def show_songs_page(request, user_id, album_id):
    needed_songs = Song.objects.filter(album__pk=album_id)

    context = {
        'songs': needed_songs,
        'album_id': album_id
        }

    return render(request, 'song-page.html', context=context)

def create_song(request, user_id, album_id):
    if request.method == "POST":
        song_form = SongForm(request.POST, request.FILES)

        if song_form.is_valid():
            song_name = song_form.cleaned_data["name"]
            song_author = song_form.cleaned_data["author"]
            song_file = song_form.cleaned_data["file"]
            curr_album = Playlist.objects.get(pk=album_id)

            Song.objects.create(name=song_name, author=song_author, file=song_file, album=curr_album)

            print(helper_functions.get_duration_of_song(os.path.join(settings.MEDIA_ROOT, str(song_file))))

            return redirect('song-page', user_id=user_id, album_id=album_id)
        else:
            messages.success(request, ('There was an error, try again!'))
            return redirect("song-page", user_id=user_id, album_id=album_id)

    else:
        song_form = SongForm()

        context = {
            'form': song_form
        }

        return render(request, 'create-song-page.html', context=context)
    
def edit_song(request, user_id, album_id, song_id):

    needed_song_instance = Song.objects.get(pk=song_id)

    if request.method == "POST":
        if "edit" in request.POST:
            song_form = SongForm(request.POST or None, instance=needed_song_instance)

            if song_form.is_valid():
                song_form.save()

                return redirect("song-page", user_id=user_id, album_id=album_id)
        elif "delete" in request.POST:
            os.remove(os.path.join(settings.MEDIA_ROOT, needed_song_instance.file.name))

            needed_song_instance.delete()

            return redirect("song-page", user_id=user_id, album_id=album_id)

    else:
        song_form = SongForm(request.POST or None, instance=needed_song_instance)

        context = {
            "form": song_form
        }

        return render(request, 'edit-song-page.html', context=context)