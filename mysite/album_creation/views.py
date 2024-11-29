from django.shortcuts import render, redirect
from django.contrib import messages
from album_creation.forms import PlaylistForm
from album_creation.models import Playlist
from django.contrib.auth.models import User
from django.http import HttpResponse
from song_creation.models import Song

# Create your views here.


def playlist_page(request):

    context = {
        "user_playlists": request.user.playlists.all(),
        "followed_playlists": request.user.followed_playlists.all()
    }

    return render(request, "album_creation/playlist-page.html", context)


def show_album_creation_page(request):

    if request.method == "POST":
        form = PlaylistForm(request.POST, request.FILES)

        if form.is_valid():
            playlist = form.save(commit=False)

            playlist.user = request.user

            playlist.save()

            return redirect("playlist-page")


    else:
        form = PlaylistForm()

    context = {
        "form": form
    }

    return render(request, 'album_creation/create-album.html', context)
    
def show_album_edit_page(request, album_id):
    
    chosen_album = request.user.playlists.get(id=album_id)

    album_form = PlaylistForm(request.POST or None, instance=chosen_album)

    if request.method == "POST":

        if album_form.is_valid():
            album_form.save()

            return redirect("playlist-page")
        
    context = {
        "form": album_form,
    }

    return render(request, 'album_creation/edit_album.html', context)


def delete_playlist(request, playlist_id):

    playlist = request.user.playlists.filter(id=playlist_id).first()

    if playlist:

        songs = playlist.songs.all()

        for song in songs:
            song.delete()

        playlist.delete()

    return redirect("playlist-page")


def unfollow_playlist(request, playlist_id):

    playlist = request.user.followed_playlists.filter(id=playlist_id).first()

    if playlist:

        playlist.delete()

    return redirect("playlist-page")


def followed_playlist_songs(request, playlist_id):

    pass