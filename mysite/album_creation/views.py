from django.shortcuts import render, redirect
from album_creation.forms import PlaylistForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required


@login_required(login_url=settings.LOGIN_URL)
def playlist_page(request):

    context = {
        "user_playlists": request.user.playlists.all(),
        "followed_playlists": request.user.followed_playlists.all()
    }

    return render(request, "album_creation/playlist-page.html", context)


@login_required(login_url=settings.LOGIN_URL)
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


@login_required(login_url=settings.LOGIN_URL)
def show_album_edit_page(request, album_id):
    
    try:

        chosen_album = request.user.playlists.get(id=album_id)

    except ObjectDoesNotExist:

        raise Http404

    album_form = PlaylistForm(instance=chosen_album)

    if request.method == "POST":

        album_form = PlaylistForm(request.POST, request.FILES, instance=chosen_album)

        if album_form.is_valid():
            album_form.save()

            return redirect("playlist-page")
        
    context = {
        "form": album_form,
    }

    return render(request, 'album_creation/edit_album.html', context)


@login_required(login_url=settings.LOGIN_URL)
def delete_playlist(request, playlist_id):

    try:

        playlist = request.user.playlists.get(id=playlist_id)

    except ObjectDoesNotExist:

        raise Http404

    if playlist:

        songs = playlist.songs.all()

        for song in songs:
            song.delete()

        playlist.delete()

    return redirect("playlist-page")


@login_required(login_url=settings.LOGIN_URL)
def unfollow_playlist(request, playlist_id):

    try:

        playlist = request.user.followed_playlists.get(id=playlist_id)

    except ObjectDoesNotExist:

        raise Http404

    playlist.delete()

    return redirect("playlist-page")
