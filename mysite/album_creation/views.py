from django.shortcuts import render, redirect
from album_creation.forms import PlaylistForm
from album_creation.models import Playlist
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView


class PlaylistPage(LoginRequiredMixin, TemplateView):

    template_name = "album_creation/playlist-page.html"
    login_url = settings.LOGIN_URL

    def get_context_data(self, **kwargs):

        context =  super().get_context_data(**kwargs)

        context["user_playlists"] = self.request.user.playlists.all()
        context["followed_playlists"] = self.request.user.followed_playlists.all()

        return context


class CreatePlaylist(LoginRequiredMixin, CreateView):
    
    model = Playlist
    form_class = PlaylistForm
    template_name = "album_creation/create-album.html"
    login_url = settings.LOGIN_URL
    success_url = reverse_lazy("playlist-page")

    def form_valid(self, form):

        form.instance.user = self.request.user
        return super().form_valid(form)


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
