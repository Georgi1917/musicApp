from django.shortcuts import render, redirect
from album_song_creation.models import Playlist
from song_creation.models import Song
from song_creation.forms import SongForm
from django.contrib import messages
import os
from django.conf import settings
from song_creation import helper_functions

# Create your views here.

def show_songs_page(request, album_id):
    needed_songs = Song.objects.filter(album__pk=album_id)

    context = {
        'songs': needed_songs,
        'album_id': album_id
        }

    return render(request, 'song_creation/song-page.html', context=context)

def create_song(request, album_id):
    if request.method == "POST":
        song_form = SongForm(request.POST, request.FILES)

        if song_form.is_valid():
            song_name = song_form.cleaned_data["name"]
            song_author = song_form.cleaned_data["author"]
            song_file = song_form.cleaned_data["file"]
            curr_album = Playlist.objects.get(pk=album_id)

            curr_song = Song.objects.create(name=song_name, author=song_author, file=song_file, album=curr_album)

            processed_file_name = helper_functions.remove_unwanted_symbols(str(song_file))

            filepath = os.path.join(settings.MEDIA_ROOT, 'song_files', "_".join(processed_file_name.split(" ")))

            song_length = helper_functions.get_song_length(filepath)
            song_length_in_seconds = helper_functions.get_song_length_in_seconds(filepath)

            print(song_length)
            print(song_length_in_seconds)
            curr_song.duration = song_length
            curr_song.duration_in_seconds = song_length_in_seconds
            curr_song.save()

            return redirect('song-page', album_id=album_id)
        else:
            messages.success(request, ('There was an error, try again!'))
            return redirect("song-page", album_id=album_id)

    else:
        song_form = SongForm()

        context = {
            'form': song_form
        }

        return render(request, 'song_creation/create-song-page.html', context=context)
    
def edit_song(request, album_id, song_id):

    needed_song_instance = Song.objects.get(pk=song_id)

    if request.method == "POST":
        if "edit" in request.POST:
            song_form = SongForm(request.POST or None, instance=needed_song_instance)

            if song_form.is_valid():
                song_form.save()

                return redirect("song-page", album_id=album_id)
        elif "delete" in request.POST:

            needed_song_instance.delete()

            return redirect("song-page", album_id=album_id)

    else:
        song_form = SongForm(request.POST or None, instance=needed_song_instance)

        context = {
            "form": song_form
        }

        return render(request, 'song_creation/edit-song-page.html', context=context)