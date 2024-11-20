from django.shortcuts import render, redirect
from django.contrib import messages
from album_creation.forms import PlaylistForm
from album_creation.models import Playlist
from django.contrib.auth.models import User
from django.http import HttpResponse
from song_creation.models import Song

# Create your views here.

def show_album_creation_page(request):
    if request.method == "POST":
        form = PlaylistForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data["name"]
            desc = form.cleaned_data["description"]
            logo = form.cleaned_data["logo"]

            curr_user = User.objects.get(id=request.user.id)
            Playlist.objects.create(name=name, description=desc, logo=logo, user=curr_user)

            return redirect("main-page")

        else:
            messages.success(request, ("There was an error, please try again"))
            return redirect("album", user_id=request.user.id)

    else:
        form = PlaylistForm()

        context = {
            "form": form
        }

        return render(request, 'album_song_creation/create-album.html', context)
    
def show_album_edit_page(request, album_id):
    chosen_album = Playlist.objects.get(pk=album_id)

    album_form = PlaylistForm(request.POST or None, instance=chosen_album)

    context = {
        "form": album_form,
    }

    if request.method == "POST":

        if "edit" in request.POST:

            if album_form.is_valid():
                album_form.save()

                return redirect("main-page")
        
        else:
            needed_songs = Song.objects.filter(album_id=album_id)

            for song in needed_songs:
                song.delete()

            chosen_album.delete()
            
            return redirect("main-page")

    return render(request, 'album_song_creation/edit_album.html', context)