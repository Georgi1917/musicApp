from django.shortcuts import render, redirect
from album_song_creation.models import Playlist
from song_creation.models import Song
from song_creation.forms import SongForm
from django.contrib import messages

# Create your views here.

def show_songs_page(request, user_id, album_id):
    needed_songs = Song.objects.filter(album__pk=album_id)

    context = {
        'songs': needed_songs,
        'album_id': album_id
        }

    return render(request, 'song-page.html', context=context)

def create_song(request, user_id, album_id):
    song_form = SongForm()

    context = {
        'form': song_form
    }

    if request.method == "POST":
        if song_form.is_valid():
            song_form.save()
            return redirect('main-page', user_id=user_id)
        else:
            messages.success(request, ('There was an error, try again!'))
            return redirect("song-page", user_id=user_id, album_id=album_id)

    else:

        return render(request, 'create-song-page.html', context=context)