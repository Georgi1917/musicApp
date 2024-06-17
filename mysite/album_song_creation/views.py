from django.shortcuts import render, redirect
from django.contrib import messages
from album_song_creation.forms import PlaylistForm
from album_song_creation.models import Playlist
from django.contrib.auth.models import User

# Create your views here.

def show_album_creation_page(request, user_id):
    if request.method == "POST":
        form = PlaylistForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data["name"]
            desc = form.cleaned_data["description"]
            logo = form.cleaned_data["logo"]

            curr_user = User.objects.get(id=user_id)
            Playlist.objects.create(name=name, description=desc, logo=logo, user=curr_user)

            return redirect("main-page", user_id=user_id)

        else:
            messages.success(request, ("There was an error, please try again"))
            return redirect("album", user_id=user_id)

    else:
        form = PlaylistForm()

        context = {
            "form": form
        }

        return render(request, 'create-album.html', context)