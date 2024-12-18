from django.contrib import admin
from album_creation.models import Playlist
from song_creation.models import Song


class SongInline(admin.TabularInline):

    model = Song
    fields = ("name", "author", "duration", "file")
    extra = 1


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):

    inlines = (SongInline, )
