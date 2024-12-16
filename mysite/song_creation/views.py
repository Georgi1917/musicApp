from django.shortcuts import render, redirect, get_object_or_404
from song_creation.models import Song
from song_creation.forms import SongForm, SongEditForm
from album_creation.models import Playlist
import os
from django.conf import settings
from song_creation import helper_functions
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

# Create your views here.

def show_songs_page(request, album_id):
    needed_songs = Song.objects.filter(album__pk=album_id)

    album = get_object_or_404(Playlist, id=album_id)

    if album not in request.user.playlists.all():

        raise Http404

    context = {
        'songs': needed_songs,
        'album_id': album_id
        }

    return render(request, 'song_creation/song-page.html', context=context)

def create_song(request, album_id):

    album = get_object_or_404(Playlist, id=album_id)

    if album not in request.user.playlists.all():

        raise Http404

    if request.method == "POST":
        song_form = SongForm(request.POST, request.FILES)

        if song_form.is_valid():

            song_name = song_form.cleaned_data["name"]
            song_author = song_form.cleaned_data["author"]
            song_file = song_form.cleaned_data["file"]

            curr_album = request.user.playlists.get(id=album_id)

            curr_song = Song.objects.create(name=song_name, author=song_author, file=song_file, album=curr_album)

            processed_file_name = helper_functions.remove_unwanted_symbols(str(song_file))

            filepath = os.path.join(settings.MEDIA_ROOT, 'song_files', "_".join(processed_file_name.split(" ")))

            song_length = helper_functions.get_song_length(filepath)
            song_length_in_seconds = helper_functions.get_song_length_in_seconds(filepath)

            curr_song.duration = song_length
            curr_song.duration_in_seconds = song_length_in_seconds
            curr_song.save()

            return redirect('song-page', album_id=album_id)

    else:
        song_form = SongForm()

    context = {
        'form': song_form
    }

    return render(request, 'song_creation/create-song-page.html', context=context)
    
def edit_song(request, album_id, song_id):

    try:

        needed_song_instance = request.user.playlists.get(id=album_id).songs.get(id=song_id)

    except ObjectDoesNotExist:

        raise Http404

    if request.method == "POST":
        
        song_form = SongEditForm(request.POST, instance=needed_song_instance)

        if song_form.is_valid():

            song_form.save()

            return redirect("song-page", album_id=album_id)

    else:
        
        song_form = SongEditForm(instance=needed_song_instance)

    context = {
        "form": song_form
    }

    return render(request, 'song_creation/edit-song-page.html', context=context)
    

def delete_song(request, album_id, song_id):

    try:

        song = request.user.playlists.get(id=album_id).songs.get(id=song_id)

    except ObjectDoesNotExist:

        raise Http404

    if song:

        song.delete()

    return redirect('song-page', album_id=album_id)
    

def followed_playlist_songs(request, playlist_id):

    try:

        songs = request.user.followed_playlists.get(id=playlist_id).playlist.songs.all()

    except ObjectDoesNotExist:

        raise Http404

    context = {
        "songs": songs
    }

    return render(request, "song_creation/followed-song-page.html", context)